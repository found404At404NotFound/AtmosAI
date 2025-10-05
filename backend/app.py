from EmailOtp import sendOTP 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime
from google import genai
from flask import Flask, abort, request, send_file, redirect, render_template, session, flash, jsonify
from werkzeug.security import generate_password_hash as gph, check_password_hash as cph
import pymysql
import requests
from dotenv import load_dotenv 
import xml.etree.ElementTree as ET
import os
import tarfile
import io
import pdfplumber
import re 
import time

load_dotenv()

app = Flask(__name__)

pymysql.install_as_MySQLdb()

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.secret_key = os.getenv('SECRET_KEY')
#client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
app.permanent_session_lifetime = timedelta(days=7) 
origin = ['http://127.0.0.1:5501','https://progress-schools-mediterranean-heart.trycloudflare.com'] # Fixed: Removed trailing space
CORS(app, resources={r"/*": {"origins": origin}}, supports_credentials=True)
db = SQLAlchemy(app)
class Listings(db.Model):
    ID = db.Column(db.Integer, primary_key = True, autoincrement =True)
    NAME = db.Column(db.Text, nullable =False)
    URL = db.Column(db.Text, nullable = False)
    
    def __init__(seld):
        pass

    def getPMC(self):
        """Extracts the PMC ID from the instance's URL."""
        if self.URL:
            match = re.search(r'PMC(\d+)', self.URL, re.IGNORECASE)
            if match:
                return match.group(0)
        return None

    def getID(self,query):
        from rapidfuzz import process, fuzz
        name_url_pairs = [(n[0],n[1]) for  n in db.session.query(Listings.NAME, Listings.URL).all()] 
        from rapidfuzz import process, fuzz
        # Perform fuzzy search on names
        best_matches_with_indices = process.extract(
            query,
            [pair[0] for pair in name_url_pairs],
            scorer=fuzz.token_set_ratio,
            limit=10
        )

        # Fetch a single background image once
        try:
            bg_image = GETBG(random_image=True)
        except Exception as e:
            print(f"Warning: failed to get APOD background: {e}")
            bg_image = bg_image  # fallback - Fixed: Removed trailing space

        # Build JSON-compatible results
        json_compatible = []
        for match_name, score, index in best_matches_with_indices:
            if score > 57:
                corresponding_url = name_url_pairs[index][1]
                temp_instance = Listings()
                temp_instance.URL = corresponding_url
                pmc_id = temp_instance.getPMC()

                json_compatible.append({
                    "match": match_name,
                    "score": score,
                    "index": index,
                    "image-bg": GETBG(random_image=True),  # same image for all results
                    "pmcid": pmc_id
                })

        return json_compatible    

NASA_API_KEY = os.getenv('NASA_API_KEY')
NCBI_DELAY = 3
def GETBG(random_image=True):
    """
    Fetch a NASA APOD image URL.
    If random_image=True, it fetches a random APOD image.
    Otherwise, it fetches today's image.
    """
    url = "https://api.nasa.gov/planetary/apod"  # Fixed: Removed trailing space
    params = {"api_key": NASA_API_KEY}

    if random_image:
        # Request 1 random image
        params["count"] = 1
    else:
        # Fetch today's APOD
        params["date"] = datetime.now().strftime("%Y-%m-%d")

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching APOD: {response.status_code} {response.text}")

    data = response.json()
    # data will be a list if count is specified, or a dict if date
    if isinstance(data, list):
        apod = data[0]
    else:
        apod = data

    # Only take image URLs (ignore videos)
    if apod.get("media_type") == "image":
        return apod["url"]
    elif apod.get("media_type") == "video":
        # Use thumbnail if available or skip
        return apod.get("thumbnail_url", None)
    else:
        return None    

##############################CAPTAIN ADD YOUR FUNCTION HERE##############################
def getPMC(s): 
    a=s.split('/')
    for i in a:
       if 'PMC'in i:
           return i
##########################################################################################









def GETPMCFOLDER(pmc_id, start_path='.'):
    PMCNUM = pmc_id.upper().replace("PMC", "")
    for root, dirs, files in os.walk(start_path):
        # Check if PMCNUM is in the directories
        for dir_name in dirs:
            if PMCNUM == dir_name.upper().replace("PMC", ""):  # Handle case where dir might have "PMC" prefix
                full_path = os.path.join(root, dir_name)
                return os.path.abspath(full_path)  # Convert to absolute path
    return None


def DOWNLOADARTICLE(pmc_id, start_path='.'):
    """
    Downloads the PMC package for a given PMC ID,
    extracts PDFs into a local folder,
    and returns the absolute path to the *subdirectory* containing the first found PDF.
    Includes delays and robust error handling to manage NCBI blocks.
    """
    pmc_id_clean = pmc_id.upper().replace("PMC", "")
    OA_BASE = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi"  # Removed trailing space

    try:
        print(f"Attempting to fetch package link for {pmc_id_clean} from {OA_BASE}")
        # Introduce a delay *before* the request to be respectful
        time.sleep(NCBI_DELAY)

        # Step 1: Fetch package link with timeout
        params = {"id": pmc_id_clean}
        response = requests.get(OA_BASE, params=params, timeout=30)

        
        # Check status code first
        if response.status_code != 200:
            print(f"NCBI responded with status {response.status_code}.")
            # Check for common block indicators in the response text even on non-200
            if "temporarily blocked" in response.text.lower() or \
               "abuse situation" in response.text.lower() or \
               "info@ncbi.nlm.nih.gov" in response.text.lower():
                print("Block message detected in non-200 response!")
                return None, "NCBI has temporarily blocked access (status code + block message)."
            # If status is not 200 but no clear block message, still return an error
            return None, f"NCBI responded with status {response.status_code}."

        # Check for block message in a 200 response (likely HTML block page)
        if "temporarily blocked" in response.text.lower() or \
           "abuse situation" in response.text.lower() or \
           "info@ncbi.nlm.nih.gov" in response.text.lower():
            print("Block message detected in 200 OK response body (likely an HTML block page).")
            # Check content type as an extra check
            content_type = response.headers.get('content-type', '')
            if 'text/html' in content_type:
                 print("Confirmed: Block page is HTML.")
            return None, "NCBI has temporarily blocked access (HTML block page returned)."

        # --- End Block Detection ---

        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        # Attempt to parse the response as XML
        try:
            root = ET.fromstring(response.content)
        except ET.ParseError:
            print("Failed to parse response as XML. Likely an NCBI block page or unexpected response.")
            # Check content type as an extra check before assuming block
            content_type = response.headers.get('content-type', '')
            if 'text/html' in content_type:
                 print("Response content-type is HTML, strongly suggesting a block page.")
            return None, "NCBI returned an unexpected response (possibly a block page). Cannot parse."

        link = root.find(".//link")
        if link is None:
            return None, "No OA package available according to NCBI response."

        package_url = link.attrib["href"]
        if package_url.startswith("ftp://"):
            package_url = package_url.replace("ftp://", "https://")

        # Step 2: Download package with timeout and streaming
        print(f"Downloading package from {package_url}")
        # Introduce a delay *before* the download request too
        time.sleep(NCBI_DELAY)
        
        response_pkg = requests.get(package_url, stream=True, timeout=60)
        response_pkg.raise_for_status()

        # Step 3: Extract package into a specific folder
        save_dir = f"pdf/PMC_{pmc_id_clean}_full"
        os.makedirs(save_dir, exist_ok=True)
        print(f"Extracting package to directory: {save_dir}")

        with tarfile.open(fileobj=io.BytesIO(response_pkg.content), mode="r:gz") as tar:
            tar.extractall(path=save_dir)

        # Step 4: Find the directory containing the *first* PDF efficiently
        # Use os.walk with a flag to break out early once found
        first_pdf_dir = None
        for root_dir, dirs, files in os.walk(save_dir):
            for file in files:
                if file.lower().endswith(".pdf"):
                    first_pdf_dir = os.path.abspath(root_dir) # Get the absolute path of the directory containing the PDF
                    print(f"Found first PDF: {file} in directory: {first_pdf_dir}")
                    break # Break inner loop
            if first_pdf_dir: # Break outer loop if found
                break

        if not first_pdf_dir:
            return None, "No PDFs found in the extracted package."

        # Return the absolute path of the subdirectory containing the first PDF
        print(f"First PDF directory path: {first_pdf_dir}")
        return first_pdf_dir, None # Return the subdirectory path and no error

    # --- More Specific Exception Handling ---
    except requests.exceptions.Timeout:
        print(f"Request timed out for PMC ID {pmc_id}.")
        return None, f"Request timed out while fetching data for PMC ID {pmc_id}."
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error for PMC ID {pmc_id}: {e}")
        return None, f"Connection error: {str(e)}. This often indicates a block or network issue."
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error for PMC ID {pmc_id}: {e}")
        # This handles status codes 4xx/5xx raised by raise_for_status()
        if response.status_code == 429: # Too Many Requests
             print("Received 429 Too Many Requests error.")
             return None, "NCBI returned 429 Too Many Requests. Rate limit likely exceeded."
        return None, f"HTTP error: {str(e)}"
    except requests.exceptions.RequestException as e: # General request error
        print(f"Network error downloading/extracting PDFs for {pmc_id}: {e}")
        return None, f"Network error: {str(e)}"
    except ET.ParseError as e:
        print(f"Error parsing XML response for {pmc_id}: {e}")
        content_type = response.headers.get('content-type', '') # Access response from the scope where it was defined
        if 'text/html' in content_type:
             print("Response content-type is HTML, strongly suggesting a block page.")
        return None, f"Error parsing NCBI response (likely an HTML block page): {str(e)}"
    except tarfile.ReadError as e: # Specific error for tarfile issues
        print(f"Error extracting tar.gz package for {pmc_id}: {e}")
        return None, f"Error extracting the downloaded package: {str(e)}"
    except Exception as e: # General error handling as a fallback
        print(f"Unexpected error downloading/extracting PDFs for {pmc_id}: {e}")
        return None, f"Unexpected error: {str(e)}"
    



@app.route('/',methods=["GET", "POST"])
def root():
    for i in db.session.query(Listings).all():
        pmc = i.getPMC()

        DOWNLOADARTICLE(pmc)
@app.route('/search',methods=["GET", "POST"])
def search():
    if request.method == 'POST':

        query = request.args.get('query')
        lists = Listings()
        results = lists.getID(query)

        return jsonify(results)

    return jsonify("SEND POST REQUEST TO /search")









if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


import random
from EmailOtp import sendOTP 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime
from rapidfuzz import fuzz
import google.generativeai as genai
from flask import Flask, abort, make_response, request, send_file, redirect, render_template, session, flash, jsonify
from werkzeug.security import generate_password_hash as gph, check_password_hash as cph
from werkzeug.wrappers import response
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


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.secret_key = os.getenv('SECRET_KEY')
#client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
app.permanent_session_lifetime = timedelta(days=7) 
"""origin = ["http://127.0.0.1:5500",'http://[::1]:5500','http://%5B::1%5D:5500',"http://127.0.0.1:5500",'http://127.0.0.1:5501','https://grams-vehicle-payment-canberra.trycloudflare.com'] # Fixed: Removed trailing space
CORS(app, resources={r"/*": {"origins": origin}}, supports_credentials=True)"""

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
db = SQLAlchemy(app)


NASA_API_KEY = os.getenv('NASA_API_KEY')

############################### SPANDANA CODE PASTE ######################################
def path(filepaths, filename):
    for f in filepaths:
        if filename in f:
            return f[filename]  
        else
             return "File not found"


###########################################################################################




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
            limit=607
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


NCBI_DELAY = 3
def GETBG(random_image=True):
    """
    Fetch a NASA APOD image URL.
    If random_image=True, it fetches a random APOD image.
    Otherwise, it fetches today's image.
    """
    img_list = [
  "https://apod.nasa.gov/apod/image/0103/hubblemir_praymundo.jpg",
  "https://apod.nasa.gov/apod/image/1810/IC59IC63crawford.jpg",
  "https://apod.nasa.gov/apod/image/1307/m104_hale200_933.jpg",
  "https://apod.nasa.gov/apod/image/0207/everest_mackenzie.jpg",
  "https://apod.nasa.gov/apod/image/1310/NGC7789CarolinesRose_barr.jpg",
  "https://apod.nasa.gov/apod/image/1102/moonvenus_kaplan_1804.jpg",
  "https://apod.nasa.gov/apod/image/1407/iridescentmountain_bartunov_1268.jpg",
  "https://apod.nasa.gov/apod/image/1706/CarinaNebulaWide_Kamble_2575.jpg",
  "https://apod.nasa.gov/apod/image/9808/horsehead_iso_big.jpg",
  "https://apod.nasa.gov/apod/image/0203/llori_hstheritage_big.jpg",
  "https://apod.nasa.gov/apod/image/2006/ngc7027_HubbleKastner_1764.jpg",
  "https://apod.nasa.gov/apod/image/2402/cone_hubbleschmidt_4048.jpg",
  "https://apod.nasa.gov/apod/image/2203/ArcoCircumzenitale.jpg",
  "https://apod.nasa.gov/apod/image/0004/m7_noao_big.jpg",
  "https://apod.nasa.gov/apod/image/0606/skylens_turtainen.jpg",
  "https://apod.nasa.gov/apod/image/2012/S147_GeorgesAttard.jpg",
  "https://apod.nasa.gov/apod/image/1411/catseye4_hubble_1417.jpg",
  "https://apod.nasa.gov/apod/image/9707/aldebaranhb_cat_big.jpg",
  "https://apod.nasa.gov/apod/image/9701/lagoonclose_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/0604/n6727_noao_big.jpg",
  "https://apod.nasa.gov/apod/image/0101/sky_concam_annotated.jpg",
  "https://apod.nasa.gov/apod/image/2007/noctilucentNeowisePaoly.jpg",
  "https://apod.nasa.gov/apod/image/1812/OrionFalls_Wu_1828.jpg",
  "https://apod.nasa.gov/apod/image/1207/M101_nasaMultiW.jpg",
  "https://apod.nasa.gov/apod/image/1601/BrightBoom_JinMa_3000.jpg",
  "https://apod.nasa.gov/apod/image/1808/AroundSadrNarduzziColombari.jpg",
  "https://apod.nasa.gov/apod/image/0412/prometheus_cassini_f.jpg",
  "https://apod.nasa.gov/apod/image/0205/vla006_nrao_big.jpg",
  "https://apod.nasa.gov/apod/image/0910/moonjupiter_hackmann.jpg",
  "https://apod.nasa.gov/apod/image/2402/CaesarCoin_Wikipedia_960.jpg",
  "https://apod.nasa.gov/apod/image/2006/catseye2_not_2048.jpg",
  "https://apod.nasa.gov/apod/image/1010/ngc2170_vista.jpg",
  "https://apod.nasa.gov/apod/image/vela_rosat_big.gif",
  "https://apod.nasa.gov/apod/image/2504/GalaxiesLens_Webb_1146.jpg",
  "https://apod.nasa.gov/apod/image/9806/sohoneb_mhorn_big.jpg",
  "https://apod.nasa.gov/apod/image/1209/seasons_tezel_1080.jpg",
  "https://apod.nasa.gov/apod/image/0901/icepillar_truhin_big.jpg",
  "https://apod.nasa.gov/apod/image/2209/FairyPillar_Hubble_3857.jpg",
  "https://apod.nasa.gov/apod/image/2406/Comet12P_Ligustri_1601.jpg",
  "https://apod.nasa.gov/apod/image/1506/sh308_simon_2088.jpg",
  "https://apod.nasa.gov/apod/image/hyakutake_usno_rs.gif",
  "https://apod.nasa.gov/apod/image/1212/YosemiteWinterNightPacholka950.jpg",
  "https://apod.nasa.gov/apod/image/2109/RedSquare_Tuthill_960.jpg",
  "https://apod.nasa.gov/apod/image/1312/coldestplace_landsat8_960.jpg",
  "https://apod.nasa.gov/apod/image/1203/Earthshine_Ghouchkanlu.jpg",
  "https://apod.nasa.gov/apod/image/2411/Orion_Lorand_1992.jpg",
  "https://apod.nasa.gov/apod/image/ganysurf_gal_big.jpg",
  "https://apod.nasa.gov/apod/image/0905/M106_KC2048.jpg",
  "https://apod.nasa.gov/apod/image/2110/ngc2080_hubble_1348.jpg",
  "https://apod.nasa.gov/apod/image/9803/ngc1808_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/2203/PIA20727PlutoNight.jpg",
  "https://apod.nasa.gov/apod/image/0301/bhr71_vlt_big.jpg",
  "https://apod.nasa.gov/apod/image/0007/usanight_dmsp_big.gif",
  "https://apod.nasa.gov/apod/image/9708/universe_gc3_big.jpg",
  "https://apod.nasa.gov/apod/image/9909/lasco_merc2_big.jpg",
  "https://apod.nasa.gov/apod/image/luna3pix.gif",
  "https://apod.nasa.gov/apod/image/0404/vm45_cortner_800.jpg",
  "https://apod.nasa.gov/apod/image/0710/izwicky18_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/2102/AuroraTree_Wallace_2048.jpg",
  "https://apod.nasa.gov/apod/image/1607/MagCloudsDeep_BeletskyEtAl_1800.jpg",
  "https://apod.nasa.gov/apod/image/9701/ngc2359_cfa_big.jpg",
  "https://apod.nasa.gov/apod/image/2310/2P_Encke_2023_08_24JuneLake_California_USA_DEBartlett.jpg",
  "https://apod.nasa.gov/apod/image/0303/peopleearth94_usda_big.gif",
  "https://apod.nasa.gov/apod/image/0707/rcw79_spitzer_medf.jpg",
  "https://apod.nasa.gov/apod/image/1909/K218b_ESAKornmesser_6000.jpg",
  "https://apod.nasa.gov/apod/image/1710/MirachNGC404KentWood.jpg",
  "https://apod.nasa.gov/apod/image/2209/CallanishAnalemma_Petricca_1280.jpg",
  "https://apod.nasa.gov/apod/image/1012/StartrailsViking_heden.jpg",
  "https://apod.nasa.gov/apod/image/2307/EtaCarinae_HubbleSchmidt_1764.jpg",
  "https://apod.nasa.gov/apod/image/0111/dusttrk_stardust.jpg",
  "https://apod.nasa.gov/apod/image/0411/n2683matthews_f.jpg",
  "https://apod.nasa.gov/apod/image/1605/IMG_5214_SONGandersen2048.JPG",
  "https://apod.nasa.gov/apod/image/0608/ic410_leshin_f.jpg",
  "https://apod.nasa.gov/apod/image/0501/rcw38_chandra_full.jpg",
  "https://apod.nasa.gov/apod/image/0008/xallsky_rosat110.jpg",
  "https://apod.nasa.gov/apod/image/0903/solar-scenic-portara-03-800x600pixels.jpg",
  "https://apod.nasa.gov/apod/image/0910/VDB152_LRGB_leshin.jpg",
  "https://apod.nasa.gov/apod/image/vela_roe.gif",
  "https://apod.nasa.gov/apod/image/2307/Prawn_Stern_3800.jpg",
  "https://apod.nasa.gov/apod/image/1605/HB-G-1254amToM.jpg",
  "https://apod.nasa.gov/apod/image/1606/horseheadir_hubble_1225.jpg",
  "https://apod.nasa.gov/apod/image/0109/barnard68_vlt_big.jpg",
  "https://apod.nasa.gov/apod/image/9908/he2-104_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/0504/einsteinNAS_piepol_full.jpg",
  "https://apod.nasa.gov/apod/image/1803/HH-HST-ESO-LLgendler.jpg",
  "https://apod.nasa.gov/apod/image/2211/earthset-snap00.png",
  "https://apod.nasa.gov/apod/image/0009/marsdonut_mpf_big.jpg",
  "https://apod.nasa.gov/apod/image/0710/vdB142_lula.jpg",
  "https://apod.nasa.gov/apod/image/2401/22466-22467anaVantuyne.jpg",
  "https://apod.nasa.gov/apod/image/0008/kemblescascade_macdonald_big.jpg",
  "https://apod.nasa.gov/apod/image/2411/LDN1471_HubbleSchmidt_1024.jpg",
  "https://apod.nasa.gov/apod/image/9703/dwingeloo1_int_big.jpg",
  "https://apod.nasa.gov/apod/image/1405/abell36Block.jpg",
  "https://apod.nasa.gov/apod/image/0810/enceladus8_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/9705/m84bh_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/0103/equinoxp1_orman.jpg",
  "https://apod.nasa.gov/apod/image/1805/ESO325-Pestana.jpg",
  "https://apod.nasa.gov/apod/image/2103/Abell21-Drudis.jpg",
  "https://apod.nasa.gov/apod/image/0109/ngc6992_mandel_big.jpg",
  "https://apod.nasa.gov/apod/image/1203/angrysun_friedman_1080.jpg",
  "https://apod.nasa.gov/apod/image/0303/IridescentCloud_danielsen_big.jpg",
  "https://apod.nasa.gov/apod/image/grandcanal.gif",
  "https://apod.nasa.gov/apod/image/2102/rosette_BlockPuckett_2918.jpg",
  "https://apod.nasa.gov/apod/image/1004/ant_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/0401/crab_cfht_big.jpg",
  "https://apod.nasa.gov/apod/image/2508/CrabRecreation_2_1054Sky1024.jpg",
  "https://apod.nasa.gov/apod/image/9806/ori2mass_big.jpg",
  "https://apod.nasa.gov/apod/image/0903/crescentmoonvenus_sullivan_big.jpg",
  "https://apod.nasa.gov/apod/image/9707/success_pathfinder_big.jpg",
  "https://apod.nasa.gov/apod/image/1111/butterfly2_hst_3017.jpg",
  "https://apod.nasa.gov/apod/image/0511/itokawa2_hayabusa_big.jpg",
  "https://apod.nasa.gov/apod/image/0509/boomerang_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/ganymede_vg.gif",
  "https://apod.nasa.gov/apod/image/0003/fullerene_beardmore_big.gif",
  "https://apod.nasa.gov/apod/image/0603/pojmanski_schur_big.jpg",
  "https://apod.nasa.gov/apod/image/1206/lunareclipse_frost_3000.jpg",
  "https://apod.nasa.gov/apod/image/1607/Prawn_Sidonio_2070.jpg",
  "https://apod.nasa.gov/apod/image/2203/DuelingBands_Dai_2000.jpg",
  "https://apod.nasa.gov/apod/image/2107/AM0644-741Full.jpg",
  "https://apod.nasa.gov/apod/image/0804/m55_cfht_big.jpg",
  "https://apod.nasa.gov/apod/image/0505/lighthouse_landolfi_big.jpg",
  "https://apod.nasa.gov/apod/image/1204/tungurahua_taschler_1600.jpg",
  "https://apod.nasa.gov/apod/image/1601/aurora_vetter_2000.jpg",
  "https://apod.nasa.gov/apod/image/9709/solprom1_eit_big.jpg",
  "https://apod.nasa.gov/apod/image/1206/M65-66-LRGB-snyder.jpg",
  "https://apod.nasa.gov/apod/image/0503/moon8_mandel_big.jpg",
  "https://apod.nasa.gov/apod/image/1608/CarinaClouds_Hubble_2292.jpg",
  "https://apod.nasa.gov/apod/image/hyakutake_26Mar_vw_big.gif",
  "https://apod.nasa.gov/apod/image/1512/Arp87_Gardner_2770.jpg",
  "https://apod.nasa.gov/apod/image/1708/Heart_Jenkins_3280.jpg",
  "https://apod.nasa.gov/apod/image/1105/shuttleplume_sts134_2502.jpg",
  "https://apod.nasa.gov/apod/image/9803/europaclose_gal_big.jpg",
  "https://apod.nasa.gov/apod/image/1408/VenusJupiterIsoladElba_DeRosa.jpg",
  "https://apod.nasa.gov/apod/image/0712/clouds_aguirre_big.jpg",
  "https://apod.nasa.gov/apod/image/1504/67Pcrescent_RosettaConzo_7267.jpg",
  "https://apod.nasa.gov/apod/image/1203/MoonlightGrandCanyon_MPark.jpg",
  "https://apod.nasa.gov/apod/image/0405/mvms_042304_richard_f1.jpg",
  "https://apod.nasa.gov/apod/image/0801/jupiterio_newhorizons_big.jpg",
  "https://apod.nasa.gov/apod/image/2008/NGC6814_HubbleSchmidt_3970.jpg",
  "https://apod.nasa.gov/apod/image/9704/suncme_soho_big.gif",
  "https://apod.nasa.gov/apod/image/1406/CenAwide_colombari_1824.jpg",
  "https://apod.nasa.gov/apod/image/1401/ngc2207_hubble_2907.jpg",
  "https://apod.nasa.gov/apod/image/0009/leavitt_aavso_sml.jpg",
  "https://apod.nasa.gov/apod/image/0504/planeteclipse_spitzer_big.jpg",
  "https://apod.nasa.gov/apod/image/0610/suncme_soho_big.gif",
  "https://apod.nasa.gov/apod/image/1108/ptf11kly_howell_1524.jpg",
  "https://apod.nasa.gov/apod/image/sagneb_aat.gif",
  "https://apod.nasa.gov/apod/image/0603/Rosette_ballauer_2400.jpg",
  "https://apod.nasa.gov/apod/image/1301/tychoCentralPeaks_lro.jpg",
  "https://apod.nasa.gov/apod/image/0007/m57ring_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/1708/WardPartiaLunar2017.jpg",
  "https://apod.nasa.gov/apod/image/1704/ManDogSun_Hackmann_1600.jpg",
  "https://apod.nasa.gov/apod/image/0405/rhooph_noao_big.jpg",
  "https://apod.nasa.gov/apod/image/0704/pantheonEarthMoon_dalsgaard.jpg",
  "https://apod.nasa.gov/apod/image/1209/airglow120824_ladanyi_1800px.jpg",
  "https://apod.nasa.gov/apod/image/0611/m42_christensen_big.jpg",
  "https://apod.nasa.gov/apod/image/1203/auroraiceland_lopez_2000.jpg",
  "https://apod.nasa.gov/apod/image/bh_rjn.gif",
  "https://apod.nasa.gov/apod/image/1205/snowtrees_bonfadini_960.jpg",
  "https://apod.nasa.gov/apod/image/1904/scorpio_guisard_1328.jpg",
  "https://apod.nasa.gov/apod/image/0805/retrogrademars_tezel_big.jpg",
  "https://apod.nasa.gov/apod/image/9808/beehive_milan_big.jpg",
  "https://apod.nasa.gov/apod/image/1009/tadpole_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/9807/millisec_pulsar_big.jpg",
  "https://apod.nasa.gov/apod/image/1001/lrg_gabany_m94.jpg",
  "https://apod.nasa.gov/apod/image/0906/enceladusstripes_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/1901/2019_01_21_ZM_Single_crop.jpg",
  "https://apod.nasa.gov/apod/image/0203/marse_odythemis.jpg",
  "https://apod.nasa.gov/apod/image/sirius_rosat.gif",
  "https://apod.nasa.gov/apod/image/0611/paranalMoonset_gillet_f.jpg",
  "https://apod.nasa.gov/apod/image/0204/trifid_aao_big.jpg",
  "https://apod.nasa.gov/apod/image/9802/miranda_vg2mos1_full.jpg",
  "https://apod.nasa.gov/apod/image/2507/ISSMeetsSaturn3.jpg",
  "https://apod.nasa.gov/apod/image/9901/pegdsph_grebel_big.gif",
  "https://apod.nasa.gov/apod/image/1508/CometCatalina_Sharp_1200.jpg",
  "https://apod.nasa.gov/apod/image/1907/Chandrayaan2Launch.jpg",
  "https://apod.nasa.gov/apod/image/1607/BeyondEarth_Unknown_3000.jpg",
  "https://apod.nasa.gov/apod/image/0412/m33_hammar_big.jpg",
  "https://apod.nasa.gov/apod/image/0506/mvs062505_gabany_sm.jpg",
  "https://apod.nasa.gov/apod/image/0711/rocketOrion_kodama.jpg",
  "https://apod.nasa.gov/apod/image/1105/ioprometheus_galileo_1000.jpg",
  "https://apod.nasa.gov/apod/image/0810/17P-Holmes_cook.jpg",
  "https://apod.nasa.gov/apod/image/1507/CometTree_Kamble_2048.jpg",
  "https://apod.nasa.gov/apod/image/0609/earth2_cassini.jpg",
  "https://apod.nasa.gov/apod/image/0702/ioprometheus_galileo_big.jpg",
  "https://apod.nasa.gov/apod/image/1407/MoonSaturn_dinallo_1200.jpg",
  "https://apod.nasa.gov/apod/image/0809/anthearc_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/1309/fires_mccolgan_960.jpg",
  "https://apod.nasa.gov/apod/image/9709/hotbh_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/1701/FirstMoonset-SHonda.jpg",
  "https://apod.nasa.gov/apod/image/2205/RhoLunarEclipse_Dascalu_1920.jpg",
  "https://apod.nasa.gov/apod/image/1409/M16M17M18M24M25RGBHa_5panel_Hancock.jpg",
  "https://apod.nasa.gov/apod/image/2112/M3Leonard_Bartlett_3843.jpg",
  "https://apod.nasa.gov/apod/image/1709/aurora-boat-090717ChrisCook.jpg",
  "https://apod.nasa.gov/apod/image/0212/orineb2_gendler_full.jpg",
  "https://apod.nasa.gov/apod/image/1405/cone_hubbleschmidt_4048.jpg",
  "https://apod.nasa.gov/apod/image/2407/LeopardSpots_Perseverance_1648.jpg",
  "https://apod.nasa.gov/apod/image/9709/grbfades_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/1202/sn1987a_hst_850.jpg",
  "https://apod.nasa.gov/apod/image/2110/Helix_Oxygen_crop2.jpg",
  "https://apod.nasa.gov/apod/image/0107/cwleonis_swas_big.jpg",
  "https://apod.nasa.gov/apod/image/2412/LeonidsWoodcut_Vollmy_1293.jpg",
  "https://apod.nasa.gov/apod/image/1608/PerseidsMAGIC_DLopez.jpg",
  "https://apod.nasa.gov/apod/image/9709/aeromgs_jpl.gif",
  "https://apod.nasa.gov/apod/image/1506/PolarisLovejoy_RBA_2048.jpg",
  "https://apod.nasa.gov/apod/image/2407/NGC7789_difusco2048.jpg",
  "https://apod.nasa.gov/apod/image/0504/ngc6751_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/0603/zmachine_sandia_big.jpg",
  "https://apod.nasa.gov/apod/image/1405/ISSCamelopardalidsLMalcolmPark.jpg",
  "https://apod.nasa.gov/apod/image/1107/Parkes_Shuttle-ISS_20110720sarkissian.jpg",
  "https://apod.nasa.gov/apod/image/1812/M100_HubbleWfc3_3679.jpg",
  "https://apod.nasa.gov/apod/image/0404/columbiahills_spirit_full.jpg",
  "https://apod.nasa.gov/apod/image/0909/startrails_bury_big.jpg",
  "https://apod.nasa.gov/apod/image/0002/comets_soho_big.jpg",
  "https://apod.nasa.gov/apod/image/9708/europa_imp_gal_big.jpg",
  "https://apod.nasa.gov/apod/image/9901/jupovalrot_gal_big.gif",
  "https://apod.nasa.gov/apod/image/0512/cone_gabany_big.jpg",
  "https://apod.nasa.gov/apod/image/2502/RainbowFan_Eiguren_3228.jpg",
  "https://apod.nasa.gov/apod/image/2508/Wispit4b_eso_960.jpg",
  "https://apod.nasa.gov/apod/image/1408/mwyellowstone_lane_1800.jpg",
  "https://apod.nasa.gov/apod/image/2302/enceladus12_cassini_960.jpg",
  "https://apod.nasa.gov/apod/image/0009/sun_sts68_big.jpg",
  "https://apod.nasa.gov/apod/image/2507/noirlab2522a_3i.jpg",
  "https://apod.nasa.gov/apod/image/1904/Quadrantids_Duparc_1830.jpg",
  "https://apod.nasa.gov/apod/image/1906/LDN1773-Jupiter.jpg",
  "https://apod.nasa.gov/apod/image/0411/jupven_tezel_big.jpg",
  "https://apod.nasa.gov/apod/image/0203/catseye_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/1308/wave_earth_mosaic_1920.jpg",
  "https://apod.nasa.gov/apod/image/0811/hillpan_apollo15_big.jpg",
  "https://apod.nasa.gov/apod/image/2409/Comet23A3_LucyHu_3000.jpg",
  "https://apod.nasa.gov/apod/image/0602/n44_eso_big.jpg",
  "https://apod.nasa.gov/apod/image/0707/sagclouds_laveder.jpg",
  "https://apod.nasa.gov/apod/image/xray_skyview.gif",
  "https://apod.nasa.gov/apod/image/1912/Orava_Duskova_WinterHexagon_0.png",
  "https://apod.nasa.gov/apod/image/1707/ic342_rector2048.jpg",
  "https://apod.nasa.gov/apod/image/2307/antikythera_wikipedia_960.jpg",
  "https://apod.nasa.gov/apod/image/9912/westjup_gal_big.jpg",
  "https://apod.nasa.gov/apod/image/0708/meteorsurprise_tezel_big.jpg",
  "https://apod.nasa.gov/apod/image/0610/sh2136_kpno_big.jpg",
  "https://apod.nasa.gov/apod/image/0409/eflat_spirit_big.jpg",
  "https://apod.nasa.gov/apod/image/0205/helixedge_hst_big.gif",
  "https://apod.nasa.gov/apod/image/1704/SaturnInsideOut2_cassini_960.jpg",
  "https://apod.nasa.gov/apod/image/0002/lmc_noao_big.jpg",
  "https://apod.nasa.gov/apod/image/1006/a2218_hstkelly_big.jpg",
  "https://apod.nasa.gov/apod/image/2106/IMG_1088_resize.jpg",
  "https://apod.nasa.gov/apod/image/9707/mars9_st_path_big.jpg",
  "https://apod.nasa.gov/apod/image/0309/auroraclouds_cantin_big.jpg",
  "https://apod.nasa.gov/apod/image/2005/ISS-Lighttrail-Reflection.jpg",
  "https://apod.nasa.gov/apod/image/1509/PickeringsTriangleDet5_metsavainio.jpg",
  "https://apod.nasa.gov/apod/image/2509/IrasDisk_Webb_2045.jpg",
  "https://apod.nasa.gov/apod/image/2409/NightTatra_Rosadzinski_5028.jpg",
  "https://apod.nasa.gov/apod/image/0301/etna_iss_big.jpg",
  "https://apod.nasa.gov/apod/image/0602/horseregion_ssro_big.jpg",
  "https://apod.nasa.gov/apod/image/1302/pointlake_curiosity_15338.jpg",
  "https://apod.nasa.gov/apod/image/1905/RSPuppis_Hubble_rba.jpg",
  "https://apod.nasa.gov/apod/image/spacewalk_sts41b_big.jpg",
  "https://apod.nasa.gov/apod/image/vela_roe.gif",
  "https://apod.nasa.gov/apod/image/cl0024_hst_big.gif",
  "https://apod.nasa.gov/apod/image/1806/CloudBowRed_Neff_1440.jpg",
  "https://apod.nasa.gov/apod/image/2001/IntoTheShadow_apod.jpg",
  "https://apod.nasa.gov/apod/image/0006/ganymede2_galileo_big.jpg",
  "https://apod.nasa.gov/apod/image/9910/triton2_vg2_big.gif",
  "https://apod.nasa.gov/apod/image/lightning_sts55_big.gif",
  "https://apod.nasa.gov/apod/image/arecibo_naic_big.gif",
  "https://apod.nasa.gov/apod/image/2406/Doodad_PughSung_9193.jpg",
  "https://apod.nasa.gov/apod/image/0004/m82_cxc_big.jpg",
  "https://apod.nasa.gov/apod/image/9904/lee_gg.jpg",
  "https://apod.nasa.gov/apod/image/9905/solarsystem_voyager_big.jpg",
  "https://apod.nasa.gov/apod/image/1411/PIA18434dione2400x1200.jpg",
  "https://apod.nasa.gov/apod/image/9612/mercury2_mariner10_big.gif",
  "https://apod.nasa.gov/apod/image/2303/PIA21923_fig1SeeingTitan2400.jpg",
  "https://apod.nasa.gov/apod/image/2001/IridescentClouds_Strand_1500.jpg",
  "https://apod.nasa.gov/apod/image/0108/perseids97_rickjoe_big.jpg",
  "https://apod.nasa.gov/apod/image/eclipse_albers.gif",
  "https://apod.nasa.gov/apod/image/1407/crab_xray_optical.jpg",
  "https://apod.nasa.gov/apod/image/2104/Polaris_Falls_3543.jpg",
  "https://apod.nasa.gov/apod/image/2507/LDN1251gualco2048.JPG",
  "https://apod.nasa.gov/apod/image/1007/mwbryce_cooper_big.jpg",
  "https://apod.nasa.gov/apod/image/2303/NGC3169LRGBrevFinalcropCDK1000_27Feb2023_2048.jpg",
  "https://apod.nasa.gov/apod/image/1804/NGC3344_hst2048.jpg",
  "https://apod.nasa.gov/apod/image/0204/viswine_integral.jpg",
  "https://apod.nasa.gov/apod/image/1409/rippledsky_dai_1000.jpg",
  "https://apod.nasa.gov/apod/image/0201/aurora_clausen.jpg",
  "https://apod.nasa.gov/apod/image/9909/corona99_espanek.jpg",
  "https://apod.nasa.gov/apod/image/2404/stsci-xNGC604NIRcam2048.png",
  "https://apod.nasa.gov/apod/image/2301/AUFSCHNAITER_Andreas_APOD_Bode_Cigare2048.jpg",
  "https://apod.nasa.gov/apod/image/1809/Saturn2018hd.jpg",
  "https://apod.nasa.gov/apod/image/0501/ngc6946_gemini_big.jpg",
  "https://apod.nasa.gov/apod/image/0504/orion_iras_big.jpg",
  "https://apod.nasa.gov/apod/image/1404/eclipsedsunbirds_wall_2500.jpg",
  "https://apod.nasa.gov/apod/image/1003/AuroraTrails_takasaka.jpg",
  "https://apod.nasa.gov/apod/image/1511/VenusArch_Horalek_1500.jpg",
  "https://apod.nasa.gov/apod/image/0209/dustdevil_mgs_big.gif",
  "https://apod.nasa.gov/apod/image/1106/2011may31planets_argerich.jpg",
  "https://apod.nasa.gov/apod/image/1801/CarinaLakeBallard_vrbasso_WebCrop2048.jpg",
  "https://apod.nasa.gov/apod/image/0002/chimney1_cgps_big.jpg",
  "https://apod.nasa.gov/apod/image/1102/SDO20110215_015332_2048_0193.jpg",
  "https://apod.nasa.gov/apod/image/2410/SteveFrance_leroux_2160.jpg",
  "https://apod.nasa.gov/apod/image/1605/MercuryTransit_3Dseip.jpg",
  "https://apod.nasa.gov/apod/image/2403/IM_Odysseus_landing-2048x1118.png",
  "https://apod.nasa.gov/apod/image/2204/MwMertola_Claro_2000.jpg",
  "https://apod.nasa.gov/apod/image/1607/BusySkyArgentina_Montefar_2800.jpg",
  "https://apod.nasa.gov/apod/image/0809/w5wide_spitzer_big.jpg",
  "https://apod.nasa.gov/apod/image/9911/siriusleonid98_pacholka.jpg",
  "https://apod.nasa.gov/apod/image/9702/moon_egret.jpg",
  "https://apod.nasa.gov/apod/image/southerncross_gb.gif",
  "https://apod.nasa.gov/apod/image/1408/MG_0098jacques_Dierick.jpg",
  "https://apod.nasa.gov/apod/image/0602/n44_gemini_big.jpg",
  "https://apod.nasa.gov/apod/image/9612/m3_cfa_big.jpg",
  "https://apod.nasa.gov/apod/image/1908/ElephantTrunk_Ayoub.jpg",
  "https://apod.nasa.gov/apod/image/1105/marsshadow_opportunity_1024.jpg",
  "https://apod.nasa.gov/apod/image/1708/Carina_Foucher_2695.jpg",
  "https://apod.nasa.gov/apod/image/9706/mathilde2_near_big.jpg",
  "https://apod.nasa.gov/apod/image/2010/GhostNebula_Jarzyna_960.jpg",
  "https://apod.nasa.gov/apod/image/1312/mb_2013-11-30_OrionsBelt.jpg",
  "https://apod.nasa.gov/apod/image/2011/marsglobalmap.jpg",
  "https://apod.nasa.gov/apod/image/2111/IMG_8522-1.png",
  "https://apod.nasa.gov/apod/image/1708/perseid_170812_ladanyi_web.jpg",
  "https://apod.nasa.gov/apod/image/0510/MoonVenusMars_espenak_full.jpg",
  "https://apod.nasa.gov/apod/image/2403/RocketSpiral_Yang_3024.jpg",
  "https://apod.nasa.gov/apod/image/9703/ngc604_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/1012/Geminid2010Fireball_abolfath.jpg",
  "https://apod.nasa.gov/apod/image/1406/dip_cobe_960.jpg",
  "https://apod.nasa.gov/apod/image/1101/pse2011novosibirsk_yuferev.jpg",
  "https://apod.nasa.gov/apod/image/0406/sst_venus_atmosphere_1759.jpg",
  "https://apod.nasa.gov/apod/image/1306/lineargullies_hirise_1457.jpg",
  "https://apod.nasa.gov/apod/image/1806/KilaueaSkyPanTezel.jpg",
  "https://apod.nasa.gov/apod/image/1203/conjunction1_perrot_633.jpg",
  "https://apod.nasa.gov/apod/image/0610/newrings_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/1912/NGC6744_FinalLiuYuhang.jpg",
  "https://apod.nasa.gov/apod/image/2304/Ma2022-3.jpg",
  "https://apod.nasa.gov/apod/image/0702/gcenter_spitzer_f40.jpg",
  "https://apod.nasa.gov/apod/image/1901/MeteorMountain_Roemmelt_1371.jpg",
  "https://apod.nasa.gov/apod/image/1711/happyla_jurasevich_2500.jpg",
  "https://apod.nasa.gov/apod/image/1002/GS-Trails2Tafreshi.jpg",
  "https://apod.nasa.gov/apod/image/9905/keyhole_noao_big.jpg",
  "https://apod.nasa.gov/apod/image/0307/phobos_mgs_big.gif",
  "https://apod.nasa.gov/apod/image/1801/PerseusCluster_DSSChandra_3600.jpg",
  "https://apod.nasa.gov/apod/image/2102/PIA24333_fig1.jpg",
  "https://apod.nasa.gov/apod/image/0704/ngc1672_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/9711/ionewvol_gal_big.jpg",
  "https://apod.nasa.gov/apod/image/1010/mooncabeus_lcross_big.jpg",
  "https://apod.nasa.gov/apod/image/2102/LunarHalo_Strand_1500.jpg",
  "https://apod.nasa.gov/apod/image/2009/M2D9_HubbleSchmidt_985.jpg",
  "https://apod.nasa.gov/apod/image/1812/M45-CaliNeb-46P-TomMasterson-GrandMesaObservatory.jpg",
  "https://apod.nasa.gov/apod/image/2104/ant_hubble_1072.jpg",
  "https://apod.nasa.gov/apod/image/0908/morninggloryclouds_petroff_big.jpg",
  "https://apod.nasa.gov/apod/image/2306/corona_aus.jpg",
  "https://apod.nasa.gov/apod/image/0803/halebopp5_aac_big.jpg",
  "https://apod.nasa.gov/apod/image/2111/67P_211107.jpg",
  "https://apod.nasa.gov/apod/image/1105/redspot_voyager1_3072.jpg",
  "https://apod.nasa.gov/apod/image/0103/smc4_uit_big.gif",
  "https://apod.nasa.gov/apod/image/9811/sextansa_kpno_big.jpg",
  "https://apod.nasa.gov/apod/image/9901/cl2244_vlt_big.jpg",
  "https://apod.nasa.gov/apod/image/1106/atlantisrollout_sts135_1800.jpg",
  "https://apod.nasa.gov/apod/image/9709/mycn18_hst_big.gif",
  "https://apod.nasa.gov/apod/image/0509/venus180hem_magellan_big.jpg",
  "https://apod.nasa.gov/apod/image/0910/FaithFullMoon090409_westlake.jpg",
  "https://apod.nasa.gov/apod/image/1510/Trifid_HubbleGendler_2400.jpg",
  "https://apod.nasa.gov/apod/image/2111/HorseFlame_Ayoub_4305.jpg",
  "https://apod.nasa.gov/apod/image/2406/DolphinNebulaHOO_2048.jpg",
  "https://apod.nasa.gov/apod/image/1408/m57_nasagendler_3000.jpg",
  "https://apod.nasa.gov/apod/image/0605/iss2_sts114_big.jpg",
  "https://apod.nasa.gov/apod/image/1710/Hverir_Vetter_1300.jpg",
  "https://apod.nasa.gov/apod/image/0704/io_walkerNH.jpg",
  "https://apod.nasa.gov/apod/image/0707/northpoleclouds_AIMData_lg.jpg",
  "https://apod.nasa.gov/apod/image/2111/astronomy101_hk_750.jpg",
  "https://apod.nasa.gov/apod/image/1205/merctrans_sohoeit_annotated_960.jpg",
  "https://apod.nasa.gov/apod/image/2405/AuroraStartrails_chiragupreti.jpg",
  "https://apod.nasa.gov/apod/image/1001/mynmareclipse_chin_big.jpg",
  "https://apod.nasa.gov/apod/image/0903/sunprom2_soho_big.gif",
  "https://apod.nasa.gov/apod/image/0805/gegenschein_eso_big.jpg",
  "https://apod.nasa.gov/apod/image/1801/PIA22089OrionValley.jpg",
  "https://apod.nasa.gov/apod/image/0709/lunation_ajc.gif",
  "https://apod.nasa.gov/apod/image/helixF_hst_big.gif",
  "https://apod.nasa.gov/apod/image/2101/Tse_2020_400mm_dmwa-rot.png",
  "https://apod.nasa.gov/apod/image/2205/CoiffeesMW_Barakat_6700.jpg",
  "https://apod.nasa.gov/apod/image/0111/m83center_hst_big.jpg ",
  "https://apod.nasa.gov/apod/image/1901/SH2-308Laubing2048.jpg",
  "https://apod.nasa.gov/apod/image/0006/sun3col_thompsoneit_big.jpg",
  "https://apod.nasa.gov/apod/image/2303/DolphinReef_Roig_5688.jpg",
  "https://apod.nasa.gov/apod/image/2109/GalaxySkyMirror_Egon_2048.jpg",
  "https://apod.nasa.gov/apod/image/9707/mars8_pathfinder_big.jpg",
  "https://apod.nasa.gov/apod/image/2310/M31_HubbleSpitzerGendler_2000.jpg",
  "https://apod.nasa.gov/apod/image/0903/sat4moons_hst.jpg",
  "https://apod.nasa.gov/apod/image/1305/thundercell_heavey_864.jpg",
  "https://apod.nasa.gov/apod/image/1308/ioplus_galileo_1817.jpg",
  "https://apod.nasa.gov/apod/image/0102/allsky_mellinger_big.jpg",
  "https://apod.nasa.gov/apod/image/vla_ss_big.gif",
  "https://apod.nasa.gov/apod/image/0612/spirit_mro_big.jpg",
  "https://apod.nasa.gov/apod/image/0301/m11_cfht_big.jpg",
  "https://apod.nasa.gov/apod/image/1201/aurora_voltmer_1920.jpg",
  "https://apod.nasa.gov/apod/image/0001/lunareclipse00_casado_big.jpg",
  "https://apod.nasa.gov/apod/image/satmoons_vg1_big.gif",
  "https://apod.nasa.gov/apod/image/0212/eclipse_eumetsat_big.gif",
  "https://apod.nasa.gov/apod/image/2406/MostDistantGalaxy_Webb_960.jpg",
  "https://apod.nasa.gov/apod/image/9710/europe_dmsp.gif",
  "https://apod.nasa.gov/apod/image/1111/w5_spitzer_5569.jpg",
  "https://apod.nasa.gov/apod/image/0607/titanlakes_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/2107/2020_07_23_NEOWISE_Klondik_Combine1_Samostatne_1500px.png",
  "https://apod.nasa.gov/apod/image/2012/AntennaeGpotw1345a_2048.jpg",
  "https://apod.nasa.gov/apod/image/1607/m2d9_hubble_985.jpg",
  "https://apod.nasa.gov/apod/image/0405/tadpole_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/0611/transit3d_piepol_f800.jpg",
  "https://apod.nasa.gov/apod/image/0412/rosette_crawford_big.jpg",
  "https://apod.nasa.gov/apod/image/2309/TheLargeMagellanicCloud.jpg",
  "https://apod.nasa.gov/apod/image/2307/PhobosMars_MarsExpress_1500.jpg",
  "https://apod.nasa.gov/apod/image/1512/20151221LulworthCove-reKotsiopoulos.jpg",
  "https://apod.nasa.gov/apod/image/0412/decMoonJup_westlake_f1.jpg",
  "https://apod.nasa.gov/apod/image/1706/StarGone_Hubble_1350.jpg",
  "https://apod.nasa.gov/apod/image/1505/MessierCrater3d_vantuyne.jpg",
  "https://apod.nasa.gov/apod/image/1005/m72_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/1702/WhiteOval_Juno_640.jpg",
  "https://apod.nasa.gov/apod/image/1904/AuroraPingvllir_Casado_1336.jpg",
  "https://apod.nasa.gov/apod/image/0603/pojmanski_tezel_20060302f.jpg",
  "https://apod.nasa.gov/apod/image/1602/Tarantula-HST-ESO-M.jpg",
  "https://apod.nasa.gov/apod/image/1603/NGC6188_Pugh_2195.jpg",
  "https://apod.nasa.gov/apod/image/2007/SGUNeuschwansteinNeowiseIMG2532-1920.jpg",
  "https://apod.nasa.gov/apod/image/0908/NGC4631_4656_poepsel.jpg",
  "https://apod.nasa.gov/apod/image/0011/bzcam_wiyn.gif",
  "https://apod.nasa.gov/apod/image/9801/earth_vg1.jpg",
  "https://apod.nasa.gov/apod/image/lmc_uks.gif",
  "https://apod.nasa.gov/apod/image/9904/challenger_apollo17_big.jpg",
  "https://apod.nasa.gov/apod/image/1512/etacarinae_hubble_900.jpg",
  "https://apod.nasa.gov/apod/image/0911/LeoSMCLMC6043_wulfen.jpg",
  "https://apod.nasa.gov/apod/image/0712/boomerang_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/2009/STScI-H-p2046b-m-1999x2000.jpg",
  "https://apod.nasa.gov/apod/image/1503/IC5067_vanvleet_3172.jpg",
  "https://apod.nasa.gov/apod/image/1602/hanford_ligo_575.jpg",
  "https://apod.nasa.gov/apod/image/1805/HyperionTrue_CassiniUgarkovic_1800.jpg",
  "https://apod.nasa.gov/apod/image/2302/C2022E3ZTFmeetsC2022U2Atlasbeschriftet.jpg",
  "https://apod.nasa.gov/apod/image/0804/Marathon8_abolfath.jpg",
  "https://apod.nasa.gov/apod/image/1809/NGC3628_GardnerRBA_2048.jpg",
  "https://apod.nasa.gov/apod/image/9803/asteroids3_neargal_big.jpg",
  "https://apod.nasa.gov/apod/image/1305/NGC4725-Subaru-HST-LL.jpg",
  "https://apod.nasa.gov/apod/image/1410/mwSunToMoon_lane_1800.jpg",
  "https://apod.nasa.gov/apod/image/2110/peg51_desmars.jpg",
  "https://apod.nasa.gov/apod/image/0808/AugMoon_mammana_laveder.jpg",
  "https://apod.nasa.gov/apod/image/0212/pleiades_aao_big.jpg",
  "https://apod.nasa.gov/apod/image/1610/HydrogenSky_HI4PI_2048.jpg",
  "https://apod.nasa.gov/apod/image/arp230_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/0809/rockyplanets_salway_big.jpg",
  "https://apod.nasa.gov/apod/image/0408/c2003k4_mfh_big.jpg",
  "https://apod.nasa.gov/apod/image/2411/NGC474_S1_Crop.jpg",
  "https://apod.nasa.gov/apod/image/2401/image-20240116164558_v1.jpg",
  "https://apod.nasa.gov/apod/image/1003/phobos1_marsexpress_big.jpg",
  "https://apod.nasa.gov/apod/image/2212/25BrightestStars_Jittasaiyapan_1500.jpg",
  "https://apod.nasa.gov/apod/image/1007/TSE2010Calafate_pyykko.jpg",
  "https://apod.nasa.gov/apod/image/0012/earthsp_gal_big.jpg",
  "https://apod.nasa.gov/apod/image/0608/m27HaOiii_krejci.jpg",
  "https://apod.nasa.gov/apod/image/1312/LRGBV6Melotte15_JWalker.jpg",
  "https://apod.nasa.gov/apod/image/0405/q4_schur_big.jpg",
  "https://apod.nasa.gov/apod/image/2112/NGC6822LRGB-1.jpg",
  "https://apod.nasa.gov/apod/image/1701/redaurora_cherney_1600.jpg",
  "https://apod.nasa.gov/apod/image/heao_fleet_big.gif",
  "https://apod.nasa.gov/apod/image/1105/barnard163_wiyn_2000.jpg",
  "https://apod.nasa.gov/apod/image/2401/SarArcNz_McDonald_2048.jpg",
  "https://apod.nasa.gov/apod/image/9810/north1_seawifs_big.jpg",
  "https://apod.nasa.gov/apod/image/1510/20151022GhostStartrails.jpg",
  "https://apod.nasa.gov/apod/image/2210/LDN43_SelbyHanson_3993.jpg",
  "https://apod.nasa.gov/apod/image/1109/m6_eguivar_1600.jpg",
  "https://apod.nasa.gov/apod/image/0505/ngc3314_keel_big.jpg",
  "https://apod.nasa.gov/apod/image/0809/seasons_tezel_big.jpg",
  "https://apod.nasa.gov/apod/image/1107/garradd_chumack_1800.jpg",
  "https://apod.nasa.gov/apod/image/1602/LightPillars_Libby_1115.jpg",
  "https://apod.nasa.gov/apod/image/2410/LDN43_SelbyHanson_3993.jpg",
  "https://apod.nasa.gov/apod/image/0305/ngc253_cfht_big.jpg",
  "https://apod.nasa.gov/apod/image/1309/IceNightPanTafreshi-s.jpg",
  "https://apod.nasa.gov/apod/image/9904/amdeepfield_boltwood_big.jpg",
  "https://apod.nasa.gov/apod/image/0605/redspot2_hst_f.jpg",
  "https://apod.nasa.gov/apod/image/1212/22466-22467anaVantuyne.jpg",
  "https://apod.nasa.gov/apod/image/2207/STScI-SMACS0723_webb.png",
  "https://apod.nasa.gov/apod/image/0008/coma_noao_big.jpg",
  "https://apod.nasa.gov/apod/image/0501/swarm_cxc_labelf.jpg",
  "https://apod.nasa.gov/apod/image/nyc_night_sts59.gif",
  "https://apod.nasa.gov/apod/image/2209/TarantulaNearIr_Webb_1396.jpg",
  "https://apod.nasa.gov/apod/image/0905/atlantisHST_2009may13_legault.jpg",
  "https://apod.nasa.gov/apod/image/2112/HUBBLE_NGC7318_PS2_CROP_INSIGHT3072.jpg",
  "https://apod.nasa.gov/apod/image/0702/alborzmountains_tafreshi.jpg",
  "https://apod.nasa.gov/apod/image/9705/cr61_polar_big.jpg",
  "https://apod.nasa.gov/apod/image/0008/halleynuc_giotto_big.gif",
  "https://apod.nasa.gov/apod/image/0808/LEumbralshadow_ayiomamitis.jpg",
  "https://apod.nasa.gov/apod/image/0502/v838monOct2004_hst_f.jpg",
  "https://apod.nasa.gov/apod/image/1210/ontario_vir_2012282_lrg.jpg",
  "https://apod.nasa.gov/apod/image/0806/circumhorizonarc_gitto_big.jpg",
  "https://apod.nasa.gov/apod/image/0704/heic0407a_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/9805/cena_wfpc2_big.jpg",
  "https://apod.nasa.gov/apod/image/1103/discovery_110307_ladanyi.jpg",
  "https://apod.nasa.gov/apod/image/0601/itokawa06_hayabusa_big.jpg",
  "https://apod.nasa.gov/apod/image/2505/mars10_st_path_big.jpg",
  "https://apod.nasa.gov/apod/image/0912/Geminid2009_pacholka850wp.jpg",
  "https://apod.nasa.gov/apod/image/1806/FermiCopia_1_2048.jpg",
  "https://apod.nasa.gov/apod/image/2004/NGC253_HstSubaruEsoNew_3500.jpg",
  "https://apod.nasa.gov/apod/image/1210/abell39_block_1200.jpg",
  "https://apod.nasa.gov/apod/image/1901/Cuadrantidas30estelasDLopez.jpg",
  "https://apod.nasa.gov/apod/image/0206/asteroids_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/0005/antrho_uks.jpg",
  "https://apod.nasa.gov/apod/image/2407/ssportrait_vg1_big.jpg",
  "https://apod.nasa.gov/apod/image/1208/ConjunctionColoursPhilHart.jpg",
  "https://apod.nasa.gov/apod/image/1710/greenmachine_nasa_4800.jpg",
  "https://apod.nasa.gov/apod/image/2103/C60-61_PS2_CROP_FULL.jpg",
  "https://apod.nasa.gov/apod/image/2110/teapotsirds_winfree_960.jpg",
  "https://apod.nasa.gov/apod/image/1710/3c75_chandraNRAO_576.jpg",
  "https://apod.nasa.gov/apod/image/0307/acidaliamars_mgs_full.jpg",
  "https://apod.nasa.gov/apod/image/1609/ASE2016Moser.jpg",
  "https://apod.nasa.gov/apod/image/1506/m5hst2048.jpg",
  "https://apod.nasa.gov/apod/image/0108/merc2_m10_big.gif",
  "https://apod.nasa.gov/apod/image/0110/bhspin_xmm_big.jpg ",
  "https://apod.nasa.gov/apod/image/2209/SnakingFilament_Friedman_960.jpg",
  "https://apod.nasa.gov/apod/image/9905/u10_vg2_big.jpg",
  "https://apod.nasa.gov/apod/image/0501/wiroshadow_bonnell_f.jpg",
  "https://apod.nasa.gov/apod/image/0601/pillarmaine_orloski_big.jpg",
  "https://apod.nasa.gov/apod/image/2311/Perseus_Euclid_4400.jpg",
  "https://apod.nasa.gov/apod/image/0808/bailysbeads_durman_big.jpg",
  "https://apod.nasa.gov/apod/image/1805/GumExpanseGleason.jpg",
  "https://apod.nasa.gov/apod/image/0212/raptor_vestrand1.jpg",
  "https://apod.nasa.gov/apod/image/0703/ering_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/1504/RBA_BlueTears1600.jpg",
  "https://apod.nasa.gov/apod/image/0205/saturn_herhst_big.jpg",
  "https://apod.nasa.gov/apod/image/1906/N00172886_92_beltramini.jpg",
  "https://apod.nasa.gov/apod/image/1704/halebopp_dimai_852.jpg",
  "https://apod.nasa.gov/apod/image/2206/Mercury_BepiColombo_2049.jpg",
  "https://apod.nasa.gov/apod/image/1406/catseye2_not_2048.jpg",
  "https://apod.nasa.gov/apod/image/9708/ngc3603_wb_big.jpg",
  "https://apod.nasa.gov/apod/image/0007/firstgrb_vela4.gif",
  "https://apod.nasa.gov/apod/image/1707/Tafreshi_NIK2197s.jpg",
  "https://apod.nasa.gov/apod/image/2404/EclipseWyoming_Cooper_960.jpg",
  "https://apod.nasa.gov/apod/image/2403/The_Dish_Tracking_IM-1_22February2024_04.jpg",
  "https://apod.nasa.gov/apod/image/9801/earthmoon_near_big.jpg",
  "https://apod.nasa.gov/apod/image/0103/astro2_sts67_big.jpg",
  "https://apod.nasa.gov/apod/image/bh_nasm_big.gif",
  "https://apod.nasa.gov/apod/image/9904/skimars_mgs_big.gif",
  "https://apod.nasa.gov/apod/image/hyakutake_eso_big.gif",
  "https://apod.nasa.gov/apod/image/0510/hyperion2_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/1201/PIA15254_LMC2048.jpg",
  "https://apod.nasa.gov/apod/image/0007/vlts_eso_big.jpg",
  "https://apod.nasa.gov/apod/image/1208/n5033block.jpg",
  "https://apod.nasa.gov/apod/image/2010/E_tag_aftermath.gif",
  "https://apod.nasa.gov/apod/image/0005/cmbsky_boomerang_big.jpg",
  "https://apod.nasa.gov/apod/image/9702/solwind_soho.gif",
  "https://apod.nasa.gov/apod/image/1209/shuttlelax_confer_3628.jpg",
  "https://apod.nasa.gov/apod/image/0709/Iapetus_pava_big.jpg",
  "https://apod.nasa.gov/apod/image/1301/mcnaught_guisard_881.jpg",
  "https://apod.nasa.gov/apod/image/0803/iss_sts122_big.jpg",
  "https://apod.nasa.gov/apod/image/1108/iridescent_havens_750.png",
  "https://apod.nasa.gov/apod/image/2504/GCenter_MeerKatWebb_7642.jpg",
  "https://apod.nasa.gov/apod/image/1104/cena_csiro_1063.jpg",
  "https://apod.nasa.gov/apod/image/copernicus_ap17_big.jpg",
  "https://apod.nasa.gov/apod/image/0207/everest_mackenzie.jpg",
  "https://apod.nasa.gov/apod/image/2101/Medulla_Croman_1200.jpg",
  "https://apod.nasa.gov/apod/image/9904/mimas_vg1_big.jpg",
  "https://apod.nasa.gov/apod/image/9801/prosp_ksc_big.jpg",
  "https://apod.nasa.gov/apod/image/1703/2017-03-17-0726_2-RGBdp.jpg",
  "https://apod.nasa.gov/apod/image/2403/leotripletasi294large.jpg",
  "https://apod.nasa.gov/apod/image/spiral_gallery_uit_big.gif",
  "https://apod.nasa.gov/apod/image/1008/VeMaSpicaDesert_tafreshi.jpg",
  "https://apod.nasa.gov/apod/image/1308/thundercloud_dyer_2000.jpg",
  "https://apod.nasa.gov/apod/image/0710/ngc2080_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/2004/WindmillStarTrails.jpg",
  "https://apod.nasa.gov/apod/image/1105/crabflare_fermi_3000.jpg",
  "https://apod.nasa.gov/apod/image/1001/magstream_nrao_big.jpg",
  "https://apod.nasa.gov/apod/image/1806/catseye4_hubble_1417.jpg",
  "https://apod.nasa.gov/apod/image/0410/magicnight_wagner_full.jpg",
  "https://apod.nasa.gov/apod/image/2103/IC1318_Pham_3200.jpg",
  "https://apod.nasa.gov/apod/image/0909/milkywaypan_brunier_2048.jpg",
  "https://apod.nasa.gov/apod/image/0010/omgcen_uit_big.gif",
  "https://apod.nasa.gov/apod/image/9707/marspan2_pf_big.jpg",
  "https://apod.nasa.gov/apod/image/1406/GS_20140514_FullMoon_5015_p1500.jpg",
  "https://apod.nasa.gov/apod/image/1105/sombrero_hst_3215.jpg",
  "https://apod.nasa.gov/apod/image/2205/Abell_7-2022-02-20-HOO-1600.jpg",
  "https://apod.nasa.gov/apod/image/2003/BhShredder_NASA_3482.jpg",
  "https://apod.nasa.gov/apod/image/1607/NGC1309Jeff_full.jpg",
  "https://apod.nasa.gov/apod/image/1511/ic410tadpoles_coates.jpg",
  "https://apod.nasa.gov/apod/image/1212/halebopp_dimai_852.jpg",
  "https://apod.nasa.gov/apod/image/0602/venuslemma_tezel_big.jpg",
  "https://apod.nasa.gov/apod/image/1603/sofi20mar15_floor2-b.jpg",
  "https://apod.nasa.gov/apod/image/1711/BeltStars_nouroozi2000.jpg",
  "https://apod.nasa.gov/apod/image/catseye_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/2006/SarsCov2_Niaid_4096.jpg",
  "https://apod.nasa.gov/apod/image/1601/ProximaCentauri_Hubble_2048.jpg",
  "https://apod.nasa.gov/apod/image/1511/AuroraClouds_Boffelli_2048.jpg",
  "https://apod.nasa.gov/apod/image/2104/CenA_SofiaPlusB_2480.jpg",
  "https://apod.nasa.gov/apod/image/0906/parthenon_ayiomamitis_big.jpg",
  "https://apod.nasa.gov/apod/image/9710/cass_titan_big.jpg",
  "https://apod.nasa.gov/apod/image/1201/Cherney_PlanetLovejoy.jpg",
  "https://apod.nasa.gov/apod/image/2312/OrionBetelgeuse_occultation.jpg",
  "https://apod.nasa.gov/apod/image/radiogal_hst.gif",
  "https://apod.nasa.gov/apod/image/1308/nova_del_labels_Alean.jpg",
  "https://apod.nasa.gov/apod/image/0910/ic10F_MSiniscalchi.jpg",
  "https://apod.nasa.gov/apod/image/io1.gif",
  "https://apod.nasa.gov/apod/image/sun_960515_big.gif",
  "https://apod.nasa.gov/apod/image/0112/m15_wiyn_big.gif",
  "https://apod.nasa.gov/apod/image/1806/heic1811a_ngc3256_2048.jpg",
  "https://apod.nasa.gov/apod/image/1107/NGC6188lorenzi2000.jpg",
  "https://apod.nasa.gov/apod/image/0010/grb000131v_vlt_big.gif",
  "https://apod.nasa.gov/apod/image/9910/30dor_details_big.jpg",
  "https://apod.nasa.gov/apod/image/0309/perseus_cxc2pan_full.jpg",
  "https://apod.nasa.gov/apod/image/0611/Messier76_seip_big.jpg",
  "https://apod.nasa.gov/apod/image/2408/CTA1_15_75_Lelu2048.jpg",
  "https://apod.nasa.gov/apod/image/0505/m20_cfht_big.jpg",
  "https://apod.nasa.gov/apod/image/2505/M63_HaLRGB_Apod2048.jpg",
  "https://apod.nasa.gov/apod/image/0212/caustics_jkw_big.gif",
  "https://apod.nasa.gov/apod/image/1310/sungrazer_soho_1024.gif",
  "https://apod.nasa.gov/apod/image/1811/Phobos_Viking1_1175.jpg",
  "https://apod.nasa.gov/apod/image/1903/HoughtonAurora_03_2019.jpg",
  "https://apod.nasa.gov/apod/image/0505/orion_cxo_ff.jpg",
  "https://apod.nasa.gov/apod/image/2509/Ngc6357_Webb_6357.jpg",
  "https://apod.nasa.gov/apod/image/0812/nemrutorion_tezel_big.jpg",
  "https://apod.nasa.gov/apod/image/0709/victoria3_opportunity_big.jpg",
  "https://apod.nasa.gov/apod/image/0203/qsohosts_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/m20_moo.gif",
  "https://apod.nasa.gov/apod/image/1809/Cocoon_Drechsler_4000.jpg",
  "https://apod.nasa.gov/apod/image/1807/BeltofVenus062718_Cullen.jpeg",
  "https://apod.nasa.gov/apod/image/0611/mtransit06_cortner_big.jpg",
  "https://apod.nasa.gov/apod/image/1101/47Tuc_DW.jpg",
  "https://apod.nasa.gov/apod/image/earth_1_apollo17_big.gif",
  "https://apod.nasa.gov/apod/image/gl105a_hst.gif",
  "https://apod.nasa.gov/apod/image/0803/endeavorlaunch_brown_big.jpg",
  "https://apod.nasa.gov/apod/image/0504/epim_cas_full.jpg",
  "https://apod.nasa.gov/apod/image/0911/m7_atalasidis_big.jpg",
  "https://apod.nasa.gov/apod/image/2508/MeteorBoom_vanderHoeven_750.gif",
  "https://apod.nasa.gov/apod/image/1112/zagorje-2Boris.jpg",
  "https://apod.nasa.gov/apod/image/0211/NightTrailsOfAfrica_zimmerman_c1.jpg",
  "https://apod.nasa.gov/apod/image/1203/m82_hubble_3000.jpg",
  "https://apod.nasa.gov/apod/image/1712/SpaceXLaunch_Bobchin_5407.jpg",
  "https://apod.nasa.gov/apod/image/2203/telescope_alignment_evaluation_image_labeled.jpg",
  "https://apod.nasa.gov/apod/image/9909/moon3_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/2209/Traful-Lake.jpg",
  "https://apod.nasa.gov/apod/image/1509/LabCartoon_IceCube_5760.jpg",
  "https://apod.nasa.gov/apod/image/0804/flightpatterns_koblin.mov",
  "https://apod.nasa.gov/apod/image/0510/mwcentre_eso_big.jpg",
  "https://apod.nasa.gov/apod/image/9808/cmecomp_soho_big.gif",
  "https://apod.nasa.gov/apod/image/1902/EtaCarinae_HubbleSchmidt_1764.jpg",
  "https://apod.nasa.gov/apod/image/1605/quivertrees_breuer_3000.jpg",
  "https://apod.nasa.gov/apod/image/0902/Lulin2_richins_big.jpg",
  "https://apod.nasa.gov/apod/image/0507/m106_block_full.jpg",
  "https://apod.nasa.gov/apod/image/1505/Horsehead_Colombari_2035.jpg",
  "https://apod.nasa.gov/apod/image/2401/VenusPhases_Gonzales_1280.jpg",
  "https://apod.nasa.gov/apod/image/0711/earthrise_kayuga_big.jpg",
  "https://apod.nasa.gov/apod/image/0712/2007_09_14-orion-lq_vanGorp1200.jpg",
  "https://apod.nasa.gov/apod/image/0509/enceladusstripes_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/1511/NGC5291_c80aSchedler.jpg",
  "https://apod.nasa.gov/apod/image/0012/candorlayers_mgs_big.jpg",
  "https://apod.nasa.gov/apod/image/9705/ngc4039_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/0312/lenticular_hawaii_big.gif",
  "https://apod.nasa.gov/apod/image/0901/4945dietmarfull.jpg",
  "https://apod.nasa.gov/apod/image/0104/auroraiceland_shs.jpg",
  "https://apod.nasa.gov/apod/image/0311/carina2_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/1611/M63_Hubble_1098.jpg",
  "https://apod.nasa.gov/apod/image/2006/NGC1300HSTfull.jpg",
  "https://apod.nasa.gov/apod/image/0002/carina_herhst_big.jpg",
  "https://apod.nasa.gov/apod/image/hyakutake_25marhst_big.gif",
  "https://apod.nasa.gov/apod/image/1611/Tafreshi_DSC8114Ps.jpg",
  "https://apod.nasa.gov/apod/image/9903/mars_nicmos_big.jpg",
  "https://apod.nasa.gov/apod/image/1305/blueberrysun_friedman_1296.jpg",
  "https://apod.nasa.gov/apod/image/1012/m33_konrad.jpg",
  "https://apod.nasa.gov/apod/image/1409/holometer_fnal_1600.jpg",
  "https://apod.nasa.gov/apod/image/2011/IMG_20201124052235_9280.jpg",
  "https://apod.nasa.gov/apod/image/0808/ngc6960_block_big.jpg",
  "https://apod.nasa.gov/apod/image/1710/FomalhautRing_ALMA_2064.jpg",
  "https://apod.nasa.gov/apod/image/0906/softsoil_spirit_big.jpg",
  "https://apod.nasa.gov/apod/image/1106/m64_hst_897.jpg",
  "https://apod.nasa.gov/apod/image/9705/grb970508_mw.jpg",
  "https://apod.nasa.gov/apod/image/0406/q4m44_westlake_big.jpg",
  "https://apod.nasa.gov/apod/image/1208/Ma2011-2Tezel.jpg",
  "https://apod.nasa.gov/apod/image/2009/SunsetMonths_Vanzella_2400.jpg",
  "https://apod.nasa.gov/apod/image/1902/DragonAurora_Zhang_2241.jpg",
  "https://apod.nasa.gov/apod/image/9901/jan8_sxt_big.gif",
  "https://apod.nasa.gov/apod/image/0909/NGC6888_Lopez.jpg",
  "https://apod.nasa.gov/apod/image/0702/mcnaught3_kemppainen.jpg",
  "https://apod.nasa.gov/apod/image/1308/tafreshiIMG_4098Trail-s.jpg",
  "https://apod.nasa.gov/apod/image/m82_moo.gif",
  "https://apod.nasa.gov/apod/image/0705/venusmoon_ouellet_big.jpg",
  "https://apod.nasa.gov/apod/image/gamma_crab.gif",
  "https://apod.nasa.gov/apod/image/0910/m42c217p_2panel.jpg",
  "https://apod.nasa.gov/apod/image/9911/crab_vlt_big.jpg",
  "https://apod.nasa.gov/apod/image/1504/N2903JewelofLeo_hallas_c.jpg",
  "https://apod.nasa.gov/apod/image/2011/M31Horizon_Ferrarino_2048.jpg",
  "https://apod.nasa.gov/apod/image/2502/ClusterRing_Euclid_2665.jpg",
  "https://apod.nasa.gov/apod/image/nepspot_voyager2_big.gif",
  "https://apod.nasa.gov/apod/image/0503/earthquake_usgs_big.gif",
  "https://apod.nasa.gov/apod/image/2204/DevilsWay_Kiczenski_1402.jpg",
  "https://apod.nasa.gov/apod/image/9809/cluster_fors1_big.jpg",
  "https://apod.nasa.gov/apod/image/1801/Tadpoles_Jimenez_3365.jpg",
  "https://apod.nasa.gov/apod/image/0902/eagle_kp09_big.jpg",
  "https://apod.nasa.gov/apod/image/0308/ic2944glob2_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/9703/ngc3242_bb_big.gif",
  "https://apod.nasa.gov/apod/image/0205/planets2_orman.jpg",
  "https://apod.nasa.gov/apod/image/1503/MMSLaunch_cooper_1050.jpg",
  "https://apod.nasa.gov/apod/image/1208/curiosity_curiosity_5341.jpg",
  "https://apod.nasa.gov/apod/image/1409/ligustri_SMCsidingspring1824.jpg",
  "https://apod.nasa.gov/apod/image/0111/sunpillar_kirkpatrick_big.jpg ",
  "https://apod.nasa.gov/apod/image/engine_sts51.gif",
  "https://apod.nasa.gov/apod/image/hyakutake_22Apr_kh.gif",
  "https://apod.nasa.gov/apod/image/1706/s2017_06_11picdp.jpg",
  "https://apod.nasa.gov/apod/image/1312/mandelbox077_leys_960.jpg",
  "https://apod.nasa.gov/apod/image/0107/ic1396ele_gendler_big.jpg",
  "https://apod.nasa.gov/apod/image/9703/sl9_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/0703/CIVA_Mars_30_H.jpg",
  "https://apod.nasa.gov/apod/image/2309/M13-totale-en-cours-crop8.jpg",
  "https://apod.nasa.gov/apod/image/1212/PIA14934_saturn.jpg",
  "https://apod.nasa.gov/apod/image/1304/earthterminator_iss002_full.jpg",
  "https://apod.nasa.gov/apod/image/0801/mercury02_messenger_big.jpg",
  "https://apod.nasa.gov/apod/image/2212/AS17-137-20979.jpg",
  "https://apod.nasa.gov/apod/image/1611/Arp299_NustarHubble_3000.jpg",
  "https://apod.nasa.gov/apod/image/0303/lagoon_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/2209/NGC3576_Willocks_3300_Starless.jpg",
  "https://apod.nasa.gov/apod/image/1612/M8_Colombari_1824.jpg",
  "https://apod.nasa.gov/apod/image/0004/localcloud_frisch_big.gif",
  "https://apod.nasa.gov/apod/image/0502/spotmorph_dot_big.gif",
  "https://apod.nasa.gov/apod/image/0811/NGC1532_gendler.jpg",
  "https://apod.nasa.gov/apod/image/0609/lmc_spitzer_big.jpg",
  "https://apod.nasa.gov/apod/image/9808/orioncolours_malin.jpg",
  "https://apod.nasa.gov/apod/image/2409/PIA11826.jpg",
  "https://apod.nasa.gov/apod/image/0510/etnaboom_fulle.jpg",
  "https://apod.nasa.gov/apod/image/0103/sunpillar_richard_big.jpg",
  "https://apod.nasa.gov/apod/image/mercury_ast.gif",
  "https://apod.nasa.gov/apod/image/2203/YearOfSky_Bassa_960.jpg",
  "https://apod.nasa.gov/apod/image/0905/IC4592_andreo.jpg",
  "https://apod.nasa.gov/apod/image/0202/coronahole_020108eit_big.jpg",
  "https://apod.nasa.gov/apod/image/1605/SpanishPeaksMW_Pugh_1676.jpg",
  "https://apod.nasa.gov/apod/image/0902/SwiftLulinDSS_comp.jpg",
  "https://apod.nasa.gov/apod/image/0406/nep2002_hst1pan_full.jpg",
  "https://apod.nasa.gov/apod/image/1110/saturn9_cassini_1018.jpg",
  "https://apod.nasa.gov/apod/image/0908/ttauri_noao_big.jpg",
  "https://apod.nasa.gov/apod/image/2404/M57Ring_HubbleGendler_3000.jpg",
  "https://apod.nasa.gov/apod/image/0507/tempel1_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/0109/borrelly_ds1_big.jpg",
  "https://apod.nasa.gov/apod/image/9611/cartcomp_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/2504/NGC_6164_r4_2048.jpg",
  "https://apod.nasa.gov/apod/image/0001/dwingeloo1_int_big.jpg",
  "https://apod.nasa.gov/apod/image/0008/filament_trace_big.gif",
  "https://apod.nasa.gov/apod/image/0601/mars_spirit_PIA03274_f.jpg",
  "https://apod.nasa.gov/apod/image/0803/dunes2_hirise_big.jpg",
  "https://apod.nasa.gov/apod/image/0208/voynich_schaefer_big.gif",
  "https://apod.nasa.gov/apod/image/1101/galaxygarden_lesage_big.jpg",
  "https://apod.nasa.gov/apod/image/9702/allsky1_egret_big.gif",
  "https://apod.nasa.gov/apod/image/1308/sunvenusuv3_dove_800.jpg",
  "https://apod.nasa.gov/apod/image/9709/mons2_jpl.gif",
  "https://apod.nasa.gov/apod/image/1611/mirandascarp_vg2_1016.jpg",
  "https://apod.nasa.gov/apod/image/1806/Milkyway_Musca_SPSackenheim2048.jpg",
  "https://apod.nasa.gov/apod/image/2212/GeminidoverBluemoonvalley-2000.jpg",
  "https://apod.nasa.gov/apod/image/2206/V838Mon_Hubble_2238.jpg",
  "https://apod.nasa.gov/apod/image/0911/HaloWinMoon48_claro.jpg",
  "https://apod.nasa.gov/apod/image/CrabC_hst_big.gif",
  "https://apod.nasa.gov/apod/image/0002/m45_uks_big.jpg",
  "https://apod.nasa.gov/apod/image/0606/NGC4038_4039_verschatse_f.jpg",
  "https://apod.nasa.gov/apod/image/marslander.gif",
  "https://apod.nasa.gov/apod/image/1411/ldn988franke2400.jpg",
  "https://apod.nasa.gov/apod/image/0805/ngc3256_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/9810/m27_vlt_big.jpg",
  "https://apod.nasa.gov/apod/image/0001/magnetarcobe_big.jpg",
  "https://apod.nasa.gov/apod/image/2008/AlienThrone_Zajac_3807.jpg",
  "https://apod.nasa.gov/apod/image/2108/PerseidRain2021_Luo_2042.jpg",
  "https://apod.nasa.gov/apod/image/0807/NGC7331Web4_goldman.jpg",
  "https://apod.nasa.gov/apod/image/0611/v838sep06_hst_f.jpg",
  "https://apod.nasa.gov/apod/image/9707/vega_dm.jpg",
  "https://apod.nasa.gov/apod/image/2204/CmbDipole_cobe_960.jpg",
  "https://apod.nasa.gov/apod/image/9809/sag_uks026.jpg",
  "https://apod.nasa.gov/apod/image/1105/mb_2011-05_LittleDipperAndreo.jpg",
  "https://apod.nasa.gov/apod/image/2102/SwissAlpsMartianSky.jpg",
  "https://apod.nasa.gov/apod/image/2011/GWaveSources2020Oct_LigoVIrgo_2977.jpg",
  "https://apod.nasa.gov/apod/image/1203/McMathPlanets_line.jpg",
  "https://apod.nasa.gov/apod/image/saturn_24Apr_hst_big.gif",
  "https://apod.nasa.gov/apod/image/0604/tse2006_03_29corona_vangorp_f1800.jpg",
  "https://apod.nasa.gov/apod/image/0505/radiosaturn_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/1306/hyperion_cassini_1024.jpg",
  "https://apod.nasa.gov/apod/image/1610/RingPeaks_Cassini_1014.jpg",
  "https://apod.nasa.gov/apod/image/9711/hbm31_jcc_big.jpg",
  "https://apod.nasa.gov/apod/image/2008/IC1396_Chad_Leader.png",
  "https://apod.nasa.gov/apod/image/0112/leavingiss_nasa_big.jpg",
  "https://apod.nasa.gov/apod/image/2004/MVP_Aspinall_2048.jpg",
  "https://apod.nasa.gov/apod/image/0904/venus26march2009-4-FINAL-1.jpg",
  "https://apod.nasa.gov/apod/image/1403/2012VP113_cis_494.gif",
  "https://apod.nasa.gov/apod/image/0310/cygnusha_mandel_full.jpg",
  "https://apod.nasa.gov/apod/image/0712/spiritpath_hirise_big.jpg",
  "https://apod.nasa.gov/apod/image/0101/europarotmovie_gal.gif",
  "https://apod.nasa.gov/apod/image/1608/PerseidsRadiant_Goldpaint_2500.jpg",
  "https://apod.nasa.gov/apod/image/2409/M13IFN_2048.jpg",
  "https://apod.nasa.gov/apod/image/2508/DoubleClusterBrechersmall.jpg",
  "https://apod.nasa.gov/apod/image/1708/NGC2442-HST-ESO-L.jpg",
  "https://apod.nasa.gov/apod/image/0004/hb97_orman_big.jpg",
  "https://apod.nasa.gov/apod/image/2106/neonsaturnaurora_cassini_2560.jpg",
  "https://apod.nasa.gov/apod/image/0702/NGC2685_crawford.jpg",
  "https://apod.nasa.gov/apod/image/0906/ngc6240_spitzerhubble.jpg",
  "https://apod.nasa.gov/apod/image/1303/blackholedisk_cfa_1056.jpg",
  "https://apod.nasa.gov/apod/image/9806/ngc4314_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/9703/sl9_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/neptune_vg2.gif",
  "https://apod.nasa.gov/apod/image/0506/casa_spitzer_big.jpg",
  "https://apod.nasa.gov/apod/image/1307/ar11785_peach_2320.jpg",
  "https://apod.nasa.gov/apod/image/2301/barnard68v2_vlt_4000.jpg",
  "https://apod.nasa.gov/apod/image/2505/Venus_Venera14_1705.jpg",
  "https://apod.nasa.gov/apod/image/1006/lunokhod_lavochkin_big.jpg",
  "https://apod.nasa.gov/apod/image/1806/DarkNebulas_POSS2Czernetz_2000.jpg",
  "https://apod.nasa.gov/apod/image/1604/FermiMoon7y_SigMap_hot_nogrid.png",
  "https://apod.nasa.gov/apod/image/1903/luna-marzo.jpg",
  "https://apod.nasa.gov/apod/image/0303/europesunset_livingearth_big.jpg",
  "https://apod.nasa.gov/apod/image/0511/M78_messner_f.jpg",
  "https://apod.nasa.gov/apod/image/0601/helix_spitzer_f50.jpg",
  "https://apod.nasa.gov/apod/image/2312/greyillusion_wikipedia_960.jpg",
  "https://apod.nasa.gov/apod/image/1712/2017AllEclipses_1800px.jpg",
  "https://apod.nasa.gov/apod/image/1702/NGC1316_MazlinKellerMenaker.jpg",
  "https://apod.nasa.gov/apod/image/0702/cometmeteorgalaxy_yoneto_big.jpg",
  "https://apod.nasa.gov/apod/image/1703/sn1987a_hubble_850.jpg",
  "https://apod.nasa.gov/apod/image/helixF_hst_big.gif",
  "https://apod.nasa.gov/apod/image/1005/M13_mtm.jpg",
  "https://apod.nasa.gov/apod/image/1206/MidnightSunTransit-2csTafreshi.jpg",
  "https://apod.nasa.gov/apod/image/1308/twolines_yen_2048.jpg",
  "https://apod.nasa.gov/apod/image/1602/BHmerger_LIGO_3600.jpg",
  "https://apod.nasa.gov/apod/image/1911/MercurySolarTransit_200mmF10_610nm_11112019.jpg",
  "https://apod.nasa.gov/apod/image/2312/BavarianHalos_Werner_1500.jpg",
  "https://apod.nasa.gov/apod/image/0503/horsehead_steinberg_big.jpg",
  "https://apod.nasa.gov/apod/image/0505/titan_huygens_big.jpg",
  "https://apod.nasa.gov/apod/image/0509/trumpler14_cxc_f.jpg",
  "https://apod.nasa.gov/apod/image/0511/sunspot_vtt_big.jpg",
  "https://apod.nasa.gov/apod/image/shapley1_aat.gif",
  "https://apod.nasa.gov/apod/image/1006/meteorwiggle_rendtel_big.jpg",
  "https://apod.nasa.gov/apod/image/1611/NGC891vsA347-2048CopyrightJuanLozano.jpg",
  "https://apod.nasa.gov/apod/image/0411/MoonVenus_karimi_full.jpg",
  "https://apod.nasa.gov/apod/image/2304/SuperBIT_tarantula.png",
  "https://apod.nasa.gov/apod/image/2412/CometCliffs_Rosetta_960.jpg",
  "https://apod.nasa.gov/apod/image/0708/a520_chandra_big.jpg",
  "https://apod.nasa.gov/apod/image/1106/NGC5139_mandell.jpg",
  "https://apod.nasa.gov/apod/image/9708/m101_wk_big.gif",
  "https://apod.nasa.gov/apod/image/0303/jupspot_cassini_frame58.jpg",
  "https://apod.nasa.gov/apod/image/0408/titanhaze_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/0312/helios_cthomas_big.jpg",
  "https://apod.nasa.gov/apod/image/1010/hubblemuseum_esa_big.jpg",
  "https://apod.nasa.gov/apod/image/9703/grb970228_sax_big.gif",
  "https://apod.nasa.gov/apod/image/1711/M33Nagy_tamed.jpg",
  "https://apod.nasa.gov/apod/image/0010/n81_heritage_big.jpg",
  "https://apod.nasa.gov/apod/image/0401/landerbags_mer.jpg",
  "https://apod.nasa.gov/apod/image/0906/cygx1bubble_cullen_raw_big.jpg",
  "https://apod.nasa.gov/apod/image/9806/unislice_virgo_big.gif",
  "https://apod.nasa.gov/apod/image/0112/trifid_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/magellan_sc.gif",
  "https://apod.nasa.gov/apod/image/1112/IMG_9800-GBLANCHARD.jpg",
  "https://apod.nasa.gov/apod/image/2507/HebesChasma_esa_960.jpg",
  "https://apod.nasa.gov/apod/image/1403/ElCapstackBolte.jpg",
  "https://apod.nasa.gov/apod/image/0205/doublecme_soho_big.jpg",
  "https://apod.nasa.gov/apod/image/2207/JupiterRing_WebbSchmidt_2429.jpg",
  "https://apod.nasa.gov/apod/image/1212/gegenschein_eso_1200.jpg",
  "https://apod.nasa.gov/apod/image/2005/MoonPlanetsMW_Minkov_1620.jpg",
  "https://apod.nasa.gov/apod/image/1808/21p-160818_85_santllop.jpg",
  "https://apod.nasa.gov/apod/image/9806/ngc6070_sloandss_big.jpg",
  "https://apod.nasa.gov/apod/image/0008/ngc2244_cfht_big.jpg",
  "https://apod.nasa.gov/apod/image/1904/M81salvatore.jpg",
  "https://apod.nasa.gov/apod/image/0503/tether_sts46_big.jpg",
  "https://apod.nasa.gov/apod/image/0108/ngc2440_hst4_big.jpg",
  "https://apod.nasa.gov/apod/image/1701/ab_moon_from_geo_orbit_med_res_jan_15_2017.jpg",
  "https://apod.nasa.gov/apod/image/9705/moonrise_sts35_big.jpg",
  "https://apod.nasa.gov/apod/image/1412/m71Franke1800.jpg",
  "https://apod.nasa.gov/apod/image/2308/M51_255hours.jpg",
  "https://apod.nasa.gov/apod/image/1704/blacksea_modis_6000.jpg",
  "https://apod.nasa.gov/apod/image/0204/lumiere_laveder_full.jpg",
  "https://apod.nasa.gov/apod/image/2403/EquinoxSunset_Dyer_1701.jpg",
  "https://apod.nasa.gov/apod/image/1010/LMC_gleason.jpg",
  "https://apod.nasa.gov/apod/image/2409/OrionOrange_Grelin_9371.jpg",
  "https://apod.nasa.gov/apod/image/0005/m51nuc_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/2309/E_tag_aftermath.gif",
  "https://apod.nasa.gov/apod/image/0003/orionA_noao_big.jpg",
  "https://apod.nasa.gov/apod/image/1102/mooncity_vanzella_2578.jpg",
  "https://apod.nasa.gov/apod/image/2305/pia23122c-16.jpg",
  "https://apod.nasa.gov/apod/image/hyakutake_soho.gif",
  "https://apod.nasa.gov/apod/image/0310/quiltlarge_ross_bright.jpg",
  "https://apod.nasa.gov/apod/image/9702/starngc664_whipple_big.gif",
  "https://apod.nasa.gov/apod/image/2506/MeteorSats_Moline_6512.jpg",
  "https://apod.nasa.gov/apod/image/2009/m31abtpmoon.jpg",
  "https://apod.nasa.gov/apod/image/1007/BeltOfVenusPan_ward.jpg",
  "https://apod.nasa.gov/apod/image/1211/TadpoleGalaxyPS1V9snyder.jpg",
  "https://apod.nasa.gov/apod/image/2505/Crab_Webb_998.jpg",
  "https://apod.nasa.gov/apod/image/2110/M8-Pipe_APOD_GabrielSantos_LG.jpg",
  "https://apod.nasa.gov/apod/image/9802/lyalpha_gc3_big.gif",
  "https://apod.nasa.gov/apod/image/1410/cometmars_peach_1336.jpg",
  "https://apod.nasa.gov/apod/image/0712/irsaturn_vims_f.jpg",
  "https://apod.nasa.gov/apod/image/9712/30dor_qdw_big.gif",
  "https://apod.nasa.gov/apod/image/0607/saturnrhea_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/2203/VisUni_WikiBudassi_2400.jpg",
  "https://apod.nasa.gov/apod/image/1903/F_JellyFish_FIN_APOD.jpg",
  "https://apod.nasa.gov/apod/image/0710/galaxies2_apm_big.gif",
  "https://apod.nasa.gov/apod/image/0405/tle_may2004_ayiomamitis.jpg",
  "https://apod.nasa.gov/apod/image/apod_v4.gif",
  "https://apod.nasa.gov/apod/image/2205/PyramidPlanets_Fatehi_8356.jpg",
  "https://apod.nasa.gov/apod/image/0707/m31-irac_f.jpg",
  "https://apod.nasa.gov/apod/image/1503/AuroraBackyardHeden.jpg",
  "https://apod.nasa.gov/apod/image/9903/m46_wilmilan_big.jpg",
  "https://apod.nasa.gov/apod/image/2310/PlaneEclipse_Slifer_1756.jpg",
  "https://apod.nasa.gov/apod/image/0511/pan_surveyor6_full.jpg",
  "https://apod.nasa.gov/apod/image/9612/stephan_bk.gif",
  "https://apod.nasa.gov/apod/image/0002/neptune_keck_big.gif",
  "https://apod.nasa.gov/apod/image/0105/obafgkm_noao_big.jpg",
  "https://apod.nasa.gov/apod/image/1403/M63_PS1V10snyder.jpg",
  "https://apod.nasa.gov/apod/image/1002/andromeda_wise2048.jpg",
  "https://apod.nasa.gov/apod/image/2001/22466-22467anaVantuyne.jpg",
  "https://apod.nasa.gov/apod/image/1906/JupiterAbyss_JunoEichstadt_1080.jpg",
  "https://apod.nasa.gov/apod/image/1707/LightningEclipse_Kotsiopoulos_960.jpg",
  "https://apod.nasa.gov/apod/image/0910/deviltrails_mro_big.jpg",
  "https://apod.nasa.gov/apod/image/0811/VenJpt_beletsky.jpg",
  "https://apod.nasa.gov/apod/image/0309/m3_noao_big.jpg",
  "https://apod.nasa.gov/apod/image/0302/neatcme_soho_big.jpg",
  "https://apod.nasa.gov/apod/image/9908/mars4storm_mgs_big.jpg",
  "https://apod.nasa.gov/apod/image/0802/blg109_kasi_big.jpg",
  "https://apod.nasa.gov/apod/image/0801/tu24_greenbank_big.jpg",
  "https://apod.nasa.gov/apod/image/1307/milkywaylightning_metallinos_1000.jpg",
  "https://apod.nasa.gov/apod/image/9906/hammer_tsikalas_big.gif",
  "https://apod.nasa.gov/apod/image/0803/barnard68_vlt_big.jpg",
  "https://apod.nasa.gov/apod/image/0102/eroslanding_near_big.jpg",
  "https://apod.nasa.gov/apod/image/1403/heic1404b1920.jpg",
  "https://apod.nasa.gov/apod/image/0408/blueberries2_opportunity_big.jpg",
  "https://apod.nasa.gov/apod/image/2306/abell2744_jwst.png",
  "https://apod.nasa.gov/apod/image/2303/M31_Alharbi_4822.jpg",
  "https://apod.nasa.gov/apod/image/1401/onepercent_boss_3975.jpg",
  "https://apod.nasa.gov/apod/image/2311/EagleRay_Chander_3277.jpg",
  "https://apod.nasa.gov/apod/image/virgocluster_uks.gif",
  "https://apod.nasa.gov/apod/image/1402/yuanyang_airglow.jpg",
  "https://apod.nasa.gov/apod/image/2406/LionNeb_Badr_3720.jpg",
  "https://apod.nasa.gov/apod/image/0106/tse1999_kobusch_big.jpg",
  "https://apod.nasa.gov/apod/image/0508/perseidMeteors_bruenjes_big.jpg",
  "https://apod.nasa.gov/apod/image/9611/408_allsky_big.gif",
  "https://apod.nasa.gov/apod/image/1912/ElectricMilkyWay_Pedretti_1920.jpg",
  "https://apod.nasa.gov/apod/image/2208/SaturnMoon_Sojuel_1824.jpg",
  "https://apod.nasa.gov/apod/image/2411/IslandMoai_Dury_2831.jpg",
  "https://apod.nasa.gov/apod/image/0711/cr_auger_big.jpg",
  "https://apod.nasa.gov/apod/image/0403/MoonVenus_pacholka_big.jpg",
  "https://apod.nasa.gov/apod/image/0805/carina07_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/0311/jupiterp_cassini_full.jpg",
  "https://apod.nasa.gov/apod/image/2504/final_0798443319_dec.png",
  "https://apod.nasa.gov/apod/image/0912/DoubleClusterSpiked_fleming.jpg",
  "https://apod.nasa.gov/apod/image/2008/PerseidBridge_Zhang_4032.jpg",
  "https://apod.nasa.gov/apod/image/9807/merctransit_yohkoh_big.gif",
  "https://apod.nasa.gov/apod/image/9801/richat_sts41g_big.jpg",
  "https://apod.nasa.gov/apod/image/0407/titaninfrared_cassini_big.jpg",
  "https://apod.nasa.gov/apod/image/1811/GibbousMoon_Strand_1500.jpg",
  "https://apod.nasa.gov/apod/image/2107/NGC7814withSN2021rhuChart32.jpg",
  "https://apod.nasa.gov/apod/image/0603/pillars_tape_big.jpg",
  "https://apod.nasa.gov/apod/image/0009/auroraperseid_price_big.jpg",
  "https://apod.nasa.gov/apod/image/2508/asperatus_priester_1024.jpg",
  "https://apod.nasa.gov/apod/image/2107/PIA24542_fig2.jpg",
  "https://apod.nasa.gov/apod/image/1101/n6946_block.jpg",
  "https://apod.nasa.gov/apod/image/0812/findastronaut_sts126_big.jpg",
  "https://apod.nasa.gov/apod/image/1602/NGC6357schedler_S2HaO3_60.jpg",
  "https://apod.nasa.gov/apod/image/9611/solarcme_soon_big.gif",
  "https://apod.nasa.gov/apod/image/1312/lovejoyruin_heden_1000.jpg",
  "https://apod.nasa.gov/apod/image/1905/m5sBlock.jpg",
  "https://apod.nasa.gov/apod/image/2201/NGC1566LRGBHa-Hanson-SelbyFinal2048.jpg",
  "https://apod.nasa.gov/apod/image/1301/NGC4945_Master23.jpg",
  "https://apod.nasa.gov/apod/image/2109/Irish_RC8_LHaRGB.png",
  "https://apod.nasa.gov/apod/image/2305/EagleDeep_Lacroce_2047.jpg",
  "https://apod.nasa.gov/apod/image/1105/3000_CC_BY-NC.jpg",
  "https://apod.nasa.gov/apod/image/2203/Medusa_Nebula_141_x_180s.jpg",
  "https://apod.nasa.gov/apod/image/0303/v838mon_hst_fulldec.jpg",
  "https://apod.nasa.gov/apod/image/0612/ngc6357a_hst_big.jpg",
  "https://apod.nasa.gov/apod/image/ring_moo.gif",
  "https://apod.nasa.gov/apod/image/9912/catspaw_ware_big.jpg",
  "https://apod.nasa.gov/apod/image/1111/IC59IC63crawford.jpg",
  "https://apod.nasa.gov/apod/image/lg_earthrise_apollo8.gif",
  "https://apod.nasa.gov/apod/image/9801/europaraft2_gal_big.jpg",
  "https://apod.nasa.gov/apod/image/merc2_m10_big.gif",
  "https://apod.nasa.gov/apod/image/0901/NGC1579WebF2_goldman.jpg",
  "https://apod.nasa.gov/apod/image/0011/auroct_wadeclark_big.jpg"
]
    
    return random.choice(img_list)    



def EXTRACTPAGESFROMPDF(filepath: str, query: str, threshold: int = 50):
    """
    Extract all pages from a PDF where a query or word is found.
    Returns a dict: {page_number: full_page_text}
    
    Args:
        filepath (str): Path to PDF file.
        query (str): Text to search for.
        threshold (int): Minimum similarity score for fuzzy matches (0-100).
    """
    query_lower = query.lower().strip()
    matched_pages = {}

    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            page_text = text.lower().replace('\n', ' ').strip()
            best_score = 0

            # Line-level matching
            for line in text.split('\n'):
                line_clean = line.lower().strip()
                if query_lower in line_clean:
                    best_score = 100
                    break  # exact match wins
                else:
                    scores = [
                        fuzz.partial_ratio(query_lower, line_clean),
                        fuzz.token_sort_ratio(query_lower, line_clean),
                        fuzz.token_set_ratio(query_lower, line_clean)
                    ]
                    max_line_score = max(scores)
                    if max_line_score > best_score:
                        best_score = max_line_score

            # Full-page fuzzy as backup
            if best_score < threshold:
                scores = [
                    fuzz.partial_ratio(query_lower, page_text),
                    fuzz.token_sort_ratio(query_lower, page_text),
                    fuzz.token_set_ratio(query_lower, page_text)
                ]
                max_page_score = max(scores)
                if max_page_score > best_score:
                    best_score = max_page_score

            if best_score >= threshold:
                # Return the **original page text** (with formatting)
                matched_pages[i] = text

    return matched_pages



def GETPMCPDFPATH(pmc_id, start_path='.'):
    """
    Search recursively for a folder matching the PMC ID
    and return all PDFs inside it.
    
    Returns:
        list of dict: [{filename: full_path}, ...] or empty list if none found
    """
    pmc_num = pmc_id.upper().replace("PMC", "")
    pdf_files = []

    for root, dirs, files in os.walk(start_path):
        for dir_name in dirs:
            # Check if directory matches PMC ID
            dir_clean = dir_name.upper().replace("PMC", "")
            if dir_clean == pmc_num:
                full_path = os.path.abspath(os.path.join(root, dir_name))
                # Find all PDFs in this folder
                for f in os.listdir(full_path):
                    if f.lower().endswith(".pdf"):
                        pdf_files.append({f: os.path.join(full_path, f)})
                return pdf_files  # Return immediately after first match

    return pdf_files
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
    



def AIHELP(doubt, context, question):
    """
    Get AI response using Gemini API based on doubt, context, and question.
    
    Args:
        doubt (str): User's doubt or concern
        context (str or dict): Context information (can be text or dictionary with page contents)
        question (str): The question to answer
    
    Returns:
        dict: Dictionary containing success status and response or error
    """
    try:
        # Configure Gemini API
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))  # Make sure to set this environment variable
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Convert context to string if it's a dictionary
        if isinstance(context, dict):
            context_str = str(context)
        else:
            context_str = str(context)
        
        # Prepare the prompt for Gemini
        prompt = f"""
You are an expert AI assistant that answers questions with accuracy, clarity, and context awareness.

### Instructions:
1. Prioritize using the information from the provided context.
2. If the context does not fully answer the question or doubt, use your own knowledge — but ensure the response remains closely related to the context, question, and user's doubt.
3. Never provide unrelated or speculative information.
4. Always explain the reasoning clearly and step-by-step.
5. Maintain a professional, helpful, and precise tone.

### Context:
{context_str}

### Question:
{question}

### User’s Doubt:
{doubt}

### Expected Output:
Provide a well-structured, detailed answer that:
- Resolves the user’s doubt.
- Uses the context wherever applicable.
- Incorporates your own knowledge only when necessary to clarify or complete the explanation.
- Stays directly relevant to the topic.
"""
        
        # Generate response using Gemini
        response = model.generate_content(prompt)
        ai_response = response.text
        
        return {
            'success': True,
            'response': ai_response
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error generating AI response: {str(e)}'
        }

def EXTRACTPAGES(pdf_path, page_number):
    """
    Extract text content from page n-1, n, and n+1 and return in dictionary format.
    
    Args:
        pdf_path (str): Path to the PDF file
        page_number (int): The target page number (1-indexed)
    
    Returns:
        dict: Dictionary with page numbers as keys and their content as values
              Format: {'page_{n-1}': content, 'page_{n}': content, 'page_{n+1}': content}
              Pages that don't exist will be omitted from the dictionary
    """
    content_dict = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        
        # Check and extract page n-1 (if exists)
        if page_number - 1 >= 1 and page_number - 1 <= total_pages:
            page_content = pdf.pages[page_number - 2].extract_text()  # -2 because 0-indexed
            if page_content:
                content_dict[f'page_{page_number - 1}'] = page_content
        
        # Check and extract page n (if exists)
        if page_number >= 1 and page_number <= total_pages:
            page_content = pdf.pages[page_number - 1].extract_text()  # -1 because 0-indexed
            if page_content:
                content_dict[f'page_{page_number}'] = page_content
        
        # Check and extract page n+1 (if exists)
        if page_number + 1 >= 1 and page_number + 1 <= total_pages:
            page_content = pdf.pages[page_number].extract_text()  # No -1 because we want n+1, which is index n (0-indexed)
            if page_content:
                content_dict[f'page_{page_number + 1}'] = page_content
    
    return content_dict





@app.route('/',methods=["GET", "POST"])
def root():
    return 'ROOT PAGE'
@app.route('/search',methods=["GET", "POST"])
def search():
    if request.method == 'POST':

        query = request.args.get('query')
        print(query)
        lists = Listings()
        results = lists.getID(query)
        time.sleep(0.69)
        return jsonify(results)

    return jsonify("SEND POST REQUEST TO /search")

@app.route('/article/<string:pmcid>',methods=["GET", "POST"])
def article(pmcid):
    if request.method == 'GET':
        DOWNLOADARTICLE(pmcid)
        pmc_id = pmcid.replace('PMC','')
        path_to_check = 'pdf/PMC_'+pmcid+'_full'
        
        if os.path.exists(path_to_check):
            pt = GETPMCPDFPATH(pmcid)
            print('pt = ',pt)
            print()
            return jsonify(pt)
        print(GETPMCPDFPATH(pmcid))
        return jsonify(GETPMCPDFPATH(pmcid))
    return jsonify("SEND POST REQUEST TO /article")


@app.route('/view/article', methods=["GET"])
def view_article():
    name = request.args.get('pdfname')
    pmc_id = request.args.get('pmcid')

    files = GETPMCPDFPATH(pmc_id)
    if files:
        for file_dict in files:
            # file_dict looks like {'filename.pdf': 'full_path_to_pdf'}
            for fname, fpath in file_dict.items():
                if fname == name and fpath.endswith('.pdf'):
                    # Create inline response
                    response = make_response(send_file(fpath, mimetype='application/pdf'))
                    response.headers['Content-Disposition'] = f'inline'
                    return response

        return jsonify("PDF NOT FOUND"), 404

    return jsonify("SEND GET REQUEST TO /view/article")
@app.route('/askai', methods=["POST"])
def askai():
    data = request.json
    intext = data.get('intext')       # highlighted text or query from PDF
    question = data.get('question')   # user’s question
    pdfname = data.get('pdfname')
    pmcid = data.get('pmcid')

    print(f"""
    In-text: {intext}
    Question: {question}
    PDF Name: {pdfname}
    PMCID: {pmcid}
    """)

    # Get PDF path(s) for the given PMCID
    paths = GETPMCPDFPATH(pmcid)
    if not paths:
        return jsonify({
            'success': False,
            'error': 'No PDF paths found for the given PMCID'
        })

    # Normalize to list for uniform iteration
    if isinstance(paths, dict):
        paths = [paths]

    for file_entry in paths:
        # Case 1: Dictionary entry → {filename: filepath}
        if isinstance(file_entry, dict):
            for filename, filepath in file_entry.items():
                if pdfname in filename or pdfname in filepath:
                    CONTEXT = EXTRACTPAGESFROMPDF(filepath, intext, threshold=70)
                    print("\n[Context Extracted]\n", CONTEXT, "\n")
                    response = AIHELP(intext, CONTEXT, question)
                    return jsonify(response)

        # Case 2: Direct string path
        elif isinstance(file_entry, str):
            if pdfname in file_entry:
                CONTEXT = EXTRACTPAGESFROMPDF(file_entry, intext, threshold=70)
                print("\n[Context Extracted]\n", CONTEXT, "\n")
                response = AIHELP(intext, CONTEXT, question)
                return jsonify(response)

    # If no matching PDF found
    return jsonify({
        'success': False,
        'error': 'No matching PDF file found or context could not be processed'
    })
if __name__ == '__main__':

    app.run(debug=False,host='0.0.0.0')


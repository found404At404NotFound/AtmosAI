# nasaspaceapps2025

# 🌌 **AtmosAI — Intelligent Explorer for NASA’s Open Space Data**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-black?logo=flask)](https://flask.palletsprojects.com/)
[![NASA Space Apps 2025](https://img.shields.io/badge/NASA%20Space%20Apps-2025-blueviolet?logo=nasa)](https://www.spaceappschallenge.org/)
[![AI Powered](https://img.shields.io/badge/AI-Powered%20by%20LLMs-orange?logo=openai)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🌠 Overview

**AtmosAI** — created by **Team 404Found** — is an AI-powered research assistant designed to **search, summarize, and interpret scattered scientific papers** from NASA’s open-access biological and environmental databases.

It allows researchers, students, and explorers to:
- 🔍 **Search across hundreds of NASA PDFs** intelligently  
- 🧠 **Ask context-based questions** directly about any text segment  
- 🗂️ **Automatically summarize** complex research findings  
- 🌍 **Discover patterns** across space biology experiments  

> **In short:** *AtmosAI transforms raw NASA research data into understandable, searchable, and interactive knowledge.*

---

## 🛰️ Features

✨ **Smart PDF Understanding**  
Reads and analyzes scientific PDFs from NASA’s archives using advanced fuzzy search and NLP.

🧩 **AI-Powered Question Answering**  
Ask natural questions about specific text — AtmosAI finds the most relevant context and gives you concise answers.

🪐 **Cross-Document Search**  
Search through hundreds of space biology documents (like PMC NASA datasets) in seconds.

📜 **Real-Time Summaries**  
Instantly summarize scientific papers or experimental findings.

🧬 **Adaptive Relevance Matching**  
Custom fuzzy-matching and semantic analysis ensure the right section of the paper is always found — even if wording differs.

⚙️ **Flask + AI Backend**  
Lightweight Flask backend seamlessly connects to an AI inference engine for context-based responses.

---

## 🧭 How It Works

1. **Crawl / Index NASA Open Access PDFs**  
   → Extracts document metadata and stores local references.  
2. **User Queries a Topic / Uploads PDF**  
   → The system runs a hybrid fuzzy + semantic search to locate the relevant section(s).  
3. **AI Model Responds Intelligently**  
   → Generates context-aware summaries, explanations, or answers.  
4. **Frontend Visualization (optional)**  
   → Integrates with PDF.js for in-browser viewing and interaction.  

---

## 🔬 Core Components

| Component | Description |
|------------|-------------|
| `extract_pages_with_query()` | Finds pages in PDFs that contain relevant text using fuzzy logic |
| `EXTRACTPAGESFROMPDF()` | Enhanced context extractor that returns full PDF if no match found |
| `/askai` Endpoint | Handles AI queries and returns context-based answers |
| `GETPMCPDFPATH()` | Resolves PMCID → local file path(s) |
| `AIHELP()` | Core LLM-based reasoning engine for Q&A and summarization |

---

## 🧩 Example Workflow

### 🔹 Step 1: User Query

```json
{
  "intext": "Seedling Growth Spaceflight Experiments",
  "question": "What does this experiment study?",
  "pdfname": "fpls-10-01529.pdf",
  "pmcid": "PMC6889863"
}




Always show details
text = """🔹 Step 2: Backend Processing

Finds relevant pages with EXTRACTPAGESFROMPDF()

Extracts contextual paragraphs

Sends to AI model for analysis

🔹 Step 3: AI Response
{
  "answer": "The Seedling Growth experiments study how gravity and light affect plant development in microgravity conditions aboard the ISS."
}

🧰 Tech Stack
Layer\tTechnology
Backend\tFlask (Python)
Data Processing\tpdfplumber, RapidFuzz
AI Integration\tOpenAI / Local LLM
Frontend\tPDF.js, HTML/CSS/JS
Data Source\tNASA’s PubMed Central (PMC) Open Access Biology Archive
👨‍🚀 About the Team
Team 404Found

“Finding meaning in the 404s of the universe.”

We are a passionate team of developers and space enthusiasts aiming to bridge the gap between open data and human understanding.

💡 Our Mission:
To simplify access to NASA’s vast biological experiment data through intelligent AI interfaces.

🌍 Impact & Future

Short-Term: Improve accessibility of NASA’s scattered open documents through intelligent search.

Mid-Term: Integrate semantic vector search and embeddings for even deeper relevance.

Long-Term: Expand AtmosAI into a complete AI space research companion — capable of hypothesis generation, data visualization, and cross-paper insights.

🧑‍💻 Installation
git clone https://github.com/WESKER-UC/AtmosAI.git
cd AtmosAI
python -m venv env
source env/bin/activate   # or .\\env\\Scripts\\activate on Windows
pip install -r requirements.txt
python app.py

🔗 Connect with Us

👨‍💻 James Jeshurun Giftson – GitHub | Email

👩‍💻 Nenavath Usha – GitHub | Email

🪙 License

This project is licensed under the MIT License — free to use, modify, and distribute with attribution.

🛰️ “Exploring the cosmos is humanity’s destiny — understanding it is ours.”
— Team 404Found | NASA Space Apps 2025 🌍
"""

with open("/mnt/data/AtmosAI_Project_Info.txt", "w", encoding="utf-8") as f:
    f.write(text)

"/mnt/data/AtmosAI_Project_Info.txt

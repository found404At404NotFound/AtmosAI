# nasaspaceapps2025
#DEMONSTRATION VIDEO :
https://youtu.be/f5-_gCJqw0I

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




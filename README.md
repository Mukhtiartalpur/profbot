# ProfBot – Fluid Mechanics Academic Assistant

ProfBot is an AI-powered academic assistant designed to support engineering students in the subject of Fluid Mechanics. It provides intelligent theory-based answers, interactive MCQ practice, assignment submission handling, and streamlined access to academic materials such as lecture slides and past exam papers. This assistant is tailored for use in educational institutions and can be extended to support various course-specific requirements.

## Project Purpose

The aim of ProfBot is to assist students with academic queries, reduce manual workload for teachers, and enhance learning engagement by making educational content more accessible through an intelligent interface.

## Key Features

- Theory Q&A: Ask fluid mechanics questions and receive concise, accurate, and context-aware answers retrieved from course material.
- MCQ Practice Mode: Practice multiple-choice questions extracted from official documents with immediate feedback and score tracking.
- Assignment Handling: Students can upload assignments. Teachers can upload result files for students to access individually.
- Resource Viewer: Download course materials such as lecture slides, syllabus, past papers, and grading criteria.
- Session Memory: Maintains one-session memory to preserve chat history for better conversational flow.

## Folder Structure

profbot/
├── agent.py                  # Manages LLM logic and theory answering
├── app.py                    # Streamlit frontend interface
├── rag.py                    # PDF loading, embedding, and vectorstore logic
├── mcq_handler.py            # Handles MCQ parsing, randomization, and feedback
├── assignment_handler.py     # File saving for assignments and teacher uploads
├── requirements.txt          # Project dependencies
├── .gitignore                # Excludes sensitive and auto-generated files
├── data/                     # Static documents like syllabus and mark mapping
├── past_papers/              # End semester exam PDFs
├── past_midterms/            # Midterm exam PDFs
├── vectorstore/              # FAISS vector index (excluded from Git tracking)
├── assignments/
│   ├── student_submissions/  # Assignment uploads by students (excluded)
│   └── results/              # Result PDFs uploaded by teachers (excluded)

## Tech Stack

- LangChain for RAG, memory, tools, and chains
- Groq LLM (LLaMA3-8B) for fast reasoning
- HuggingFace Sentence Transformers for embedding
- FAISS for vector similarity search
- PyPDF2 and PyMuPDF for PDF parsing
- Streamlit for the user-facing application
- Python for all backend logic

## Setup Instructions

1. Clone the repository:
   git clone https://github.com/Mukhtiartalpur/profbot.git
   cd profbot

2. Create and activate a virtual environment:
   python -m venv venv
   venv\Scripts\activate   (for Windows)

3. Install required packages:
   pip install -r requirements.txt

4. Create a .env file in the root directory and add:
   GROQ_API_KEY=your_groq_api_key

5. Launch the Streamlit app:
   streamlit run app.py

## Git Ignore Policy

To ensure a clean and secure repository, the following are excluded using .gitignore:
- .env file (contains API keys)
- vectorstore/ directory (contains large binary files)
- assignments/student_submissions/ and assignments/results/ folders (user-uploaded PDFs)
- __pycache__/ and compiled Python files

## Intended Users

- Undergraduate and postgraduate engineering students
- Course instructors and academic departments
- AI developers building education-specific tools

## Author and Credits

Developed by Engr. Mukhtiar Ali Talpur  
Mehran University of Engineering & Technology, Jamshoro  
Department of Petroleum and Natural Gas Engineering

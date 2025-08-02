# mcq_handler.py

import os
import fitz  # PyMuPDF
import random
import re

MCQ_PDF_PATH = "data/mcqs/mcqs.pdf"

class MCQHandler:
    def __init__(self):
        self.mcqs = self.extract_mcqs()

    def extract_mcqs(self):
        mcqs = []
        if not os.path.exists(MCQ_PDF_PATH):
            print(f"❌ MCQ file not found: {MCQ_PDF_PATH}")
            return mcqs

        doc = fitz.open(MCQ_PDF_PATH)
        text = ""
        for page in doc:
            text += page.get_text()

        # Look for patterns like: 1. Question\nA) Option\nB) Option...
        pattern = re.compile(r"\d+\.\s*(.*?)\nA\)(.*?)\nB\)(.*?)\nC\)(.*?)\nD\)(.*?)\n", re.DOTALL)
        matches = pattern.findall(text)

        for match in matches:
            question, A, B, C, D = [m.strip() for m in match]
            mcqs.append({
                "question": question,
                "options": {
                    "A": A,
                    "B": B,
                    "C": C,
                    "D": D
                },
                "answer": "B"  # Default correct answer placeholder (update if answer key available)
            })

        print(f"✅ Loaded {len(mcqs)} MCQs.")
        return mcqs

    def get_random_mcq(self):
        if not self.mcqs:
            return None
        return random.choice(self.mcqs)

    def check_answer(self, mcq, selected_option):
        correct_option = mcq["answer"]
        return selected_option == correct_option, correct_option

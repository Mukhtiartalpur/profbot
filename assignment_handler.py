# assignment_handler.py

import os
from datetime import datetime
import streamlit as st

# Folder paths
STUDENT_FOLDER = "assignments/student_submissions"
RESULTS_FOLDER = "assignments/results"

# 🧑‍🎓 Save student assignment
def save_student_assignment(uploaded_file, student_name):
    os.makedirs(STUDENT_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{student_name.replace(' ', '_')}_{uploaded_file.name}"
    filepath = os.path.join(STUDENT_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())
    
    return filename

# 👨‍🏫 Save teacher result file
def save_teacher_result(uploaded_file, target_student_name):
    os.makedirs(RESULTS_FOLDER, exist_ok=True)
    filename = f"{target_student_name.replace(' ', '_')}_Result.pdf"
    filepath = os.path.join(RESULTS_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())

    return filename

# 📥 Fetch result for student
def fetch_result(student_name):
    filename = f"{student_name.replace(' ', '_')}_Result.pdf"
    filepath = os.path.join(RESULTS_FOLDER, filename)

    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            st.download_button("📥 Download Your Result", f, file_name=filename)
    else:
        st.warning("❌ Result not found. Please check the name or try again later.")

# 🖥️ Student assignment UI
def handle_assignment_ui():
    st.subheader("Upload Your Assignment")
    student_name = st.text_input("Enter your full name:")
    uploaded_file = st.file_uploader("Upload your assignment (PDF)", type=["pdf"])

    if uploaded_file and student_name:
        filename = save_student_assignment(uploaded_file, student_name)
        st.success(f"✅ Assignment submitted successfully as: {filename}")

# 🧑‍🏫 Teacher result upload UI
def handle_result_ui():
    st.subheader("Upload Result for a Student")
    target_name = st.text_input("Enter student's full name:")
    uploaded_result = st.file_uploader("Upload result file (PDF)", type=["pdf"])

    if uploaded_result and target_name:
        filename = save_teacher_result(uploaded_result, target_name)
        st.success(f"✅ Result uploaded as: {filename}")

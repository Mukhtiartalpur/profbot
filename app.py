# app.py

import streamlit as st
import os
from agent import ProfBotAgent
from rag import create_or_load_vectorstore
from mcq_handler import MCQHandler
from assignment_handler import handle_assignment_ui, handle_result_ui, fetch_result

# Init vectorstore and agent
vectorstore = create_or_load_vectorstore()
agent = ProfBotAgent(vectorstore=vectorstore)
mcq_handler = MCQHandler()

st.set_page_config(page_title="ProfBot – Fluid Mechanics Assistant", layout="centered")

# Header
st.markdown("<h3 style='text-align: center;'>MEHRAN UNIVERSITY OF ENGINEERING AND TECHNOLOGY, JAMSHORO</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>INSTITUTE OF PETROLEUM AND NATURAL GAS ENGINEERING</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: right; font-size: 14px;'>Engr. Mukhtiar Ali</p>", unsafe_allow_html=True)

# Mode Selector
mode = st.sidebar.selectbox("Select Mode", [
    "Theory Q&A", 
    "Practice MCQs", 
    "Course Resources", 
    "Lecture Slides", 
    "Assignments",
    "Past Papers"   # ✅ Added this line
])

# =================== THEORY Q&A ===================
if mode == "Theory Q&A":
    st.header("📘 Ask a Theory Question")
    if "last_query" not in st.session_state:
        st.session_state.last_query = ""
    query = st.text_input("Enter your question:", key="theory_query")
    if query and query != st.session_state.last_query:
        with st.spinner("Thinking..."):
            answer = agent.answer_theory(query)
            st.session_state.last_query = query
            st.success("Answer:")
            st.write(answer)

# =================== MCQ PRACTICE ===================
elif mode == "Practice MCQs":
    st.header("🎯 MCQ Practice Mode")

    if "mcq" not in st.session_state or st.session_state.mcq is None:
        st.session_state.mcq = mcq_handler.get_random_mcq()
        st.session_state.score = 0
        st.session_state.count = 0
        st.session_state.quiz_complete = False

    if not st.session_state.quiz_complete:
        mcq = st.session_state.mcq
        st.write(f"**Q{st.session_state.count + 1}:** {mcq['question']}")
        for key, value in mcq["options"].items():
            if st.button(f"{key}) {value}"):
                correct, correct_option = mcq_handler.check_answer(mcq, key)
                if correct:
                    st.success("✅ Correct!")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ Incorrect. Correct answer is: {correct_option}")
                st.session_state.count += 1

                if st.session_state.count == 10:
                    st.session_state.quiz_complete = True
                else:
                    st.session_state.mcq = mcq_handler.get_random_mcq()
                st.rerun()
    else:
        st.info(f"🏁 Quiz Finished! Your Score: {st.session_state.score}/10")
        if st.button("🔁 Start New Quiz"):
            st.session_state.mcq = None
            st.session_state.score = 0
            st.session_state.count = 0
            st.session_state.quiz_complete = False
            st.rerun()

# =================== COURSE RESOURCES ===================
elif mode == "Course Resources":
    st.header("📂 Course Resources")
    folder = "data/resources"
    pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]
    selected_pdf = st.selectbox("Select a resource PDF:", pdf_files)
    if selected_pdf:
        with open(os.path.join(folder, selected_pdf), "rb") as f:
            st.download_button("📥 Download PDF", f, file_name=selected_pdf)

# =================== LECTURE SLIDES ===================
elif mode == "Lecture Slides":
    st.header("🧑‍🏫 Download Lecture Slides")
    folder = "data/lecture_slides"
    files = [f for f in os.listdir(folder) if f.endswith(".pdf")]
    selected_file = st.selectbox("Choose a lecture slide:", files)
    if selected_file:
        with open(os.path.join(folder, selected_file), "rb") as f:
            st.download_button("📥 Download Slide", f, file_name=selected_file)

# =================== ASSIGNMENTS ===================
elif mode == "Assignments":
    st.header("📝 Assignment Section")
    tab1, tab2, tab3 = st.tabs(["Student: Submit Assignment", "Teacher: Upload Result", "Student: Check Result"])

    with tab1:
        handle_assignment_ui()

    with tab2:
        handle_result_ui()

    with tab3:
        name_query = st.text_input("Enter your name to check result:")
        if name_query:
            fetch_result(name_query)

# =================== PAST PAPERS ===================
elif mode == "Past Papers":
    st.header("📄 Download Past Exam Papers")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📘 Final Term Papers")
        past_folder = "past_papers"
        if os.path.exists(past_folder):
            files = [f for f in os.listdir(past_folder) if f.endswith(".pdf")]
            if files:
                selected = st.selectbox("Select Final Paper", files, key="final_paper")
                with open(os.path.join(past_folder, selected), "rb") as f:
                    st.download_button("📥 Download Final Paper", f, file_name=selected)
            else:
                st.warning("No final term papers found.")

    with col2:
        st.subheader("📝 Midterm Papers")
        mid_folder = "past_midterms"
        if os.path.exists(mid_folder):
            mid_files = [f for f in os.listdir(mid_folder) if f.endswith(".pdf")]
            if mid_files:
                selected_mid = st.selectbox("Select Midterm", mid_files, key="midterm_paper")
                with open(os.path.join(mid_folder, selected_mid), "rb") as f:
                    st.download_button("📥 Download Midterm", f, file_name=selected_mid)
            else:
                st.warning("No midterm papers found.")

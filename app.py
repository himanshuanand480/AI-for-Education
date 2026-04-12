import streamlit as st
from pdf_loader import extract_text_from_pdf
from docx import Document
import re

# --- FILE READ FUNCTIONS
def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# ----PAGE SETUP
st.set_page_config(page_title="CV Analyzer", layout="wide")
st.title("📄 CV Analyzer & Job Recommendation")

# ----LAYOUT
col1, col2 = st.columns(2)

# --- LEFT SIDE (INPUT)
with col1:
    st.header("📥 Input Section")

    uploaded_files = st.file_uploader(
        "Upload CV(s)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    job_pref = st.text_input("Enter Job Preference (comma separated)")
    user_text = st.text_area("Or paste CV text here")

    st.markdown("---")

    all_text = ""

    if uploaded_files:
        st.subheader("🟡 Extracted Text Preview")

        for i, file in enumerate(uploaded_files):
            file_ext = file.name.split(".")[-1]
            file_path = f"temp_{i}.{file_ext}"

            with open(file_path, "wb") as f:
                f.write(file.read())

            # File handling
            if file_ext == "pdf":
                text = extract_text_from_pdf(file_path)
            elif file_ext == "docx":
                text = read_docx(file_path)
            elif file_ext == "txt":
                text = read_txt(file_path)
            else:
                text = ""

            all_text += text + "\n"

            st.write(f"📄 File {i+1} ({file_ext})")
            st.write(text[:300])

    if user_text:
        all_text += user_text

# ---RIGHT SIDE (OUTPUT)
with col2:
    st.header("📤 Output Section")

    if (uploaded_files or user_text) and job_pref:

        text_lower = all_text.lower()

        # 🔹 SKILL EXTRACTION (dynamic)
        skill_keywords = [
            "python", "machine learning", "sql", "excel",
            "data analysis", "java", "c++", "deep learning",
            "nlp", "pandas", "numpy", "tensorflow"
        ]

        extracted_skills = [skill for skill in skill_keywords if skill in text_lower]

        # 🔹 EXPERIENCE EXTRACTION
        experience = "Not Found"
        match = re.search(r'(\d+)\s+year', text_lower)
        if match:
            experience = match.group(0)

        # 🔹 OTHER INFO
        other_info = []
        if "b.tech" in text_lower:
            other_info.append("B.Tech")
        if "m.tech" in text_lower:
            other_info.append("M.Tech")
        if "phd" in text_lower:
            other_info.append("PhD")

        # 🔹 JOB MATCHING
        job_list = [j.strip() for j in job_pref.split(",")]

        jobs = []
        for job in job_list:
            jobs.extend([
                f"{job} - Company A",
                f"{job} - Company B",
                f"{job} - Startup XYZ"
            ])

        # OUTPUT

        # Box 1
        st.subheader("🟢 Skills & Experience")
        st.info(f"Skills: {', '.join(extracted_skills) if extracted_skills else 'Not Found'}")
        st.info(f"Experience: {experience}")

        # Box 2
        st.subheader("🟡 Other Information")
        st.write(other_info if other_info else "Not Found")

        # Box 3
        st.subheader("🔵 Jobs Available")
        for job in jobs:
            st.success(job)
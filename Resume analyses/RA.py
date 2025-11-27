#Required imports
import streamlit as st                       # Streamlit web app UI
from PyPDF2 import PdfReader                 # To extract text from PDF resumes
import google.generativeai as genai          # To interact with Gemini (Gemini Pro) model

# 🔑 Gemini API Key (paste your key here securely)
GEMINI_API_KEY = "AIzaSyAdgo7kwgYlvIZcwFGdsqratyBS-m1HvR8"

# 🔧 Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# 📄 Function to extract text from uploaded PDF
def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
    text = ""
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# 🤖 Function to analyze resume with Gemini
def analyze_resume_with_gemini(resume_text, job_role):
    prompt = f"""
    You are an expert resume analyzer.

    Based on the following resume text, do the following:
    1. Extract **Key Skills**
    2. Summarize **Work Experience**
    3. Rate alignment with job role: {job_role} (give a % match and explanation)

    Resume Text:
    {resume_text}
    """

    response = model.generate_content(prompt)
    return response.text

# 🖥️ Streamlit UI Setup
st.set_page_config(page_title="📄 Resume Analyzer", layout="centered")
st.title("📄 Resume Analyzer using Gemini")
st.write("Upload your resume and enter a job role. Gemini will analyze your resume and tell how well it matches.")

# 📤 Upload and Input
uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])
job_role = st.text_input("Enter Target Job Role (e.g., Software Engineer, Data Analyst)")

# ▶️ On Submit
if uploaded_file and job_role:
    with st.spinner("Extracting text from resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Analyzing resume using Gemini..."):
        result = analyze_resume_with_gemini(resume_text, job_role)

    st.success("✅ Analysis Complete!")
    st.markdown(result)

from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
import google.generativeai as genai

# 🔑 Gemini API Key
GEMINI_API_KEY = "AIzaSyAdgo7kwgYlvIZcwFGdsqratyBS-m1HvR8"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# 🧠 Resume text extract
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

# 🤖 Resume analysis using Gemini
def analyze_resume(resume_text, job_role):
    prompt = f"""
    You are a resume analysis expert.

    Based on this resume text, do the following:
    1. Extract **Key Skills**
    2. Summarize **Work Experience**
    3. Rate alignment with job role: {job_role}

    Resume:
    {resume_text}
    """
    response = model.generate_content(prompt)
    return response.text

# ⚙️ FastAPI app
app = FastAPI()

@app.post("https://sreevarshasj.app.n8n.cloud/webhook-test/f8b666ce-9c8a-490d-b438-4b49b43b88f3")
async def resume_webhook(
    resume: UploadFile = File(...),
    job_role: str = Form(...)
):
    # Read uploaded PDF file
    contents = await resume.read()
    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)

    try:
        resume_text = extract_text_from_pdf("temp_resume.pdf")
        analysis = analyze_resume(resume_text, job_role)
        return JSONResponse(content={"job_role": job_role, "analysis": analysis})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

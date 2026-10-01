import streamlit as st
import pdfplumber
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="AI Career Guidance & Resume Optimizer",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Career Guidance & Resume Optimizer")
st.write("Upload your resume and paste the target job description to get instant ATS match analysis and career recommendations.")

# Automatic API Key retrieval from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area("Paste Target Job Description", height=200)

def extract_pdf_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = "".join([page.extract_text() or "" for page in pdf.pages])
    return text

if st.button("🚀 Analyze & Optimize Resume"):
    if not api_key:
        st.error("API Key not found in Streamlit Secrets. Please configure GEMINI_API_KEY in App Settings.")
    elif not uploaded_file or not job_description:
        st.warning("Please upload a PDF resume and paste a job description.")
    else:
        try:
            genai.configure(api_key=api_key)
            llm = genai.GenerativeModel("gemini-3.8-flash")
            
            with st.spinner("Parsing resume text..."):
                resume_text = extract_pdf_text(uploaded_file)
            
            prompt = f"""
            You are an expert HR Applicant Tracking System (ATS) and Senior Career Coach.
            
            Candidate Resume:
            {resume_text}
            
            Target Job Description:
            {job_description}
            
            Provide a comprehensive, structured evaluation in Markdown format:
            
            ## 📊 ATS Match Score
            * Give an overall match score from **0% to 100%**.
            * Provide a brief 2-sentence rationale for this score.
            
            ## ⚠️ Missing Skills & Keyword Gaps
            * List key technical skills, tools, and soft skills present in the JD but missing from the resume.
            
            ## 📝 Resume Bullet Point Optimization
            * Pick 3 weak bullet points from the current resume and rewrite them using the **Action Verb + Task + Measurable Impact/Result** formula tailored specifically to this job description.
            
            ## 🗺️ 30-Day Skill Gap Learning Plan
            * Provide a structured 4-week learning roadmap for the candidate to bridge their top missing skill gaps.
            """
            
            with st.spinner("AI Engine is analyzing your profile..."):
                response = llm.generate_content(prompt)
                st.divider()
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error processing request: {e}")

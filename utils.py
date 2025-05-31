import base64
import json
import re
import streamlit as st
from PyPDF2 import PdfReader
from google import genai
from secretKey import gemini_api

client = genai.Client(api_key=gemini_api)
model = "gemini-2.0-flash"


@st.cache_data
def read_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


@st.cache_data
def analyze_cv(cv_text, softskills, hardskills, preference, experience):
    prompt = f"""
    You are an HR Manager/Talent Acquisition/Recruiters/CEO of a giant corporate company. You are
    very much experienced in evaluating thousands of resumes and CVs and your evaluation accuracy is too good.
    Based on the following resume text, rank the candidate resumes using the following metrics:

    Required Soft Skills (Give plus point if the candinate have certification on that skill): {', '.join(softskills)}
    Required Hard Skills (Give plus point if the candinate have certification on that skill): {', '.join(hardskills)}
    Custom Preference for choosing candinates (Optional, if empty then give 0 here): {preference}
    Minimum experience in Years (Including professional & personal project works): {experience}

    Only return the output in the following JSON format, nothing else should be printed:
    {{
        "Name": "Full Name (In FULL captial letters)",
        "SoftSkillScore": int (out of 30),
        "HardSkillScore": int (out of 40),
        "ExperienceScore": int (out of 20),
        "PreferenceScore": int (out of 10),
        "TotalScore": int (Make it in 100% and show the percentage value only),
        "Summary": "short reasoning for the score, make it short enough for a spreadsheet file cell"
    }}
    
    Here is the candinate's resume in plain text format:
    {cv_text}
    """
    try:
        response = client.models.generate_content(
            model=model, contents=prompt)
        match = re.search(r'\{[\s\S]*\}', response.text)
        data = json.loads(match.group())
        return data

    except Exception as e:
        return str(e)


def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

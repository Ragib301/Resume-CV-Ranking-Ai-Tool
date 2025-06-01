import streamlit as st
import pandas as pd
from utils import read_pdf, analyze_cv, set_background

# Streamlit App
st.title("CV & Resume Ranking Ai Tool")
st.subheader("Upload multiple resumes to select your preferred candidate.")
set_background("bg.png")

# File Uploader
uploaded_files = st.file_uploader(
    "Upload CV & Resume PDFs", type="pdf", accept_multiple_files=True)

# Skill Inputs
softskills_list = ["Communication", "Teamwork", "Leadership", "Problem-solving", "Adaptability", "Time Management", "Critical Thinking", "Creativity",
                   "Interpersonal Skills", "Emotional Intelligence", "Decision Making", "Conflict Resolution", "Negotiation", "Empathy", "Active Listening"]
softskills = st.multiselect("Select Required Soft Skills", softskills_list)

hardskills_list = ["Python", "Web Development", "Machine Learning", "Financial Analysis", "Cloud Computing", "DevOps", "Cybersecurity", "Database Management",
                   "Hardware Development", "Data Science", "UI/UX Design", "IoT", "Statistical Analysis", "Business Intelligence", "Microsoft Office"]
hardskills = st.multiselect("Select Required Hard Skills", hardskills_list)

preference = st.text_input("Custom Preference (Optional): ")
experience = st.slider("Experience in years: ", 0, 15, 1)

if st.button("Analyze & Rank CVs"):
    results = []
    with st.spinner("Analyzing CVs with Gemini AI..."):
        for file in uploaded_files:
            cv_text = read_pdf(file)
            result_dict = analyze_cv(cv_text, softskills, hardskills, preference, experience)
            results.append(result_dict)
    
    # Sort and Display
    sorted_results = sorted(results, key=lambda x: x.get('TotalScore', 0), reverse=True)
    st.subheader("Ranked Candidates")
    ranking_df = pd.DataFrame(sorted_results)
    
    # Assign Rankings
    ranking_df.index = ranking_df.index + 1
    ranking_df.index.name = "Rank"

    # Display the DataFrame
    st.dataframe(ranking_df, use_container_width=True)

    # Export in CSV format
    csv_df = ranking_df[['Name', 'TotalScore', 'SoftSkillScore',
                 'HardSkillScore', 'ExperienceScore', 'PreferenceScore', 'Summary']]
    csv = csv_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Ranking in CSV", data=csv,
                       file_name="ranking_result.csv", mime="text/csv")

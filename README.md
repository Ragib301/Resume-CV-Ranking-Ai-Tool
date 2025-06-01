# Resume-CV-Ranking-Ai-Tool
A professional-grade CV/Resume Ranking system built using **Python**, **Streamlit**, **PyPDF2**, **Json**, **Pandas**, and **Gemini API (Google's LLM)**. This tool enables automated evaluation of a hundred number of resumes based on customizable criteria including soft-skills, hard-skills, years of experience (including professional & project), and specific preferences provided by an HR manager or startup founder.

---

## 🔍 Features

* Upload and analyze multiple PDF resumes simultaneously
* Extract plain text from resumes using PyPDF2
* Use Gemini API (via prompt engineering) to score and summarize each candidate
* Customize ranking criteria:

  * Soft Skills (e.g., Communication, Leadership)
  * Hard Skills (e.g., Python, Web Development)
  * Experience (in years)
  * Any custom preferences (keywords or requirements)
* JSON response parsing to extract AI-generated evaluations
* Visualized rankings with Streamlit using Pandas DataFrame
* Downloadable CSV of all rankings and scores

---

## ⚙️ How It Works

1. **Upload CVs:**
   Multiple PDF files can be uploaded through the Streamlit interface.

2. **Extract Text:**

   ```python
   def read_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
   ```

   Text is extracted from each PDF for input to the AI model.

3. **Construct Prompt for Gemini API:**

   ```python
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
   ```

4. **Call Gemini API & Parse JSON Output:**

   ```python
    response = client.models.generate_content(model=model, contents=prompt)
    match = re.search(r'\{[\s\S]*\}', response.text)
    data = json.loads(match.group())
   ```

   The LLM evaluates and ranks each resume. Output is parsed and formatted.

5. **Display Results:**

   ```python
    # Sort and Convert into DataFrame
    sorted_results = sorted(results, key=lambda x: x.get('TotalScore', 0), reverse=True)
    st.subheader("Ranked Candidates")
    ranking_df = pd.DataFrame(sorted_results)
    
    # Assign Rankings
    ranking_df.index = ranking_df.index + 1
    ranking_df.index.name = "Rank"

    # Display the DataFrame
    st.dataframe(ranking_df, use_container_width=True)
   ```

   Results are ranked and shown with visual formatting. Hyperlinks to each original PDF are also included.

6. **Download CSV:**

   ```python
   # Export in CSV format
    csv_df = ranking_df[['Name', 'TotalScore', 'SoftSkillScore',
                 'HardSkillScore', 'ExperienceScore', 'PreferenceScore', 'Summary']]
    csv = csv_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Ranking in CSV", data=csv,
                       file_name="ranking_result.csv", mime="text/csv")
   ```

   You can export the analysis for external use or review.

---

## 📦 Tech Stack

* Python 3.10+
* Streamlit
* PyPDF2
* Pandas
* Json
* Gemini API (via `google`)

---

## 🚀 Getting Started

### Installation

```bash
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run main.py
```

---

## 📁 File Structure

```
├── main.py                 # Main Streamlit Cod
├── utils.py                # Main funtions of pdf reading and analyzing are stored here
├── secretKey.py            # Code that stores the Gemini API Key (For security purpose)
├── bg.png                  # Backgroud image for the app
├── ranking_result.csv      # Results in CSV file
├── requirements.txt        # Python dependencies
└── README.md               # This documentation
```

---

## 🧠 Limitations

* Gemini API rate limits apply.
* JSON output parsing requires clean formatting from LLM.
* Currently supports only PDF files.

---

## 📄 License
* MIT License. Use freely with attribution.
---

> Built as a side-project with love, curiosity, and coffee ☕. Contributions welcome!

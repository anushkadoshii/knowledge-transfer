import sys
import subprocess

try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import streamlit as st

# Ensure CrewAI is installed
try:
    import crewai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "crewai"])
    import crewai

from crewai import Crew, Process
from agents import (
    github_agent, email_agent, file_agent, document_agent, nlp_agent, knowledge_agent
)
from tasks import (
    github_task, email_task, file_task, document_task, nlp_task, knowledge_task
)
from io import BytesIO
from utils.file_utils import extract_text_from_file

st.title("Automated Knowledge Transfer")

github_username = st.text_input("Enter your GitHub Username")
github_token = None
if github_username.strip():
    github_token = st.text_input("Enter your GitHub Personal Access Token", type="password")
email = st.text_input("Enter your Email ID")
uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)

st.markdown("""
**Instructions:**  
- Enter your GitHub username, email, and upload relevant files.
- Relevant files include:
  1. Reports and documents written by you.
  2. Slides presented by you.
  3. Spreadsheets created by you.
- Click the button to start the knowledge transfer process.
- Results will appear below.
""")

if st.button("Start Knowledge Transfer"):
    if not github_username and not email and not uploaded_files:
        st.warning("Please provide at least one input.")
    else:
        with st.spinner("Processing your request..."):
            try:
                all_texts = []
                if uploaded_files:
                    for file in uploaded_files:
                        file_stream = BytesIO(file.getvalue())
                        text = extract_text_from_file(file.name, file_stream)
                        all_texts.append(text)
                # Prepare input dictionary for the crew
                inputs = {
                    "github_username": github_username,
                    "github_token": github_token,
                    "email": email,
                    "all_texts": all_texts
                }

                # Define the Crew
                crew = Crew(
                    agents=[github_agent, email_agent, file_agent, document_agent, nlp_agent, knowledge_agent],
                    tasks=[github_task, email_task, file_task, document_task, nlp_task, knowledge_task],
                    process=Process.sequential,  # or Process.hierarchical
                    verbose=True
                )

                # Run the entire workflow with CrewAI
                result = crew.kickoff(inputs=inputs)

                # Display results
                st.subheader("Results")
                st.json(result)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

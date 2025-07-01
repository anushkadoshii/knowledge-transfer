__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import streamlit as st
from crewai import Crew, Process
from agents import github_agent, email_agent, file_agent, document_agent, nlp_agent, knowledge_agent
from tasks import github_task, email_task, file_task, document_task, nlp_task, knowledge_task

# Set up the Streamlit app
st.title("Automated Knowledge Transfer")

# User inputs
github_username = st.text_input("GitHub Username")
email = st.text_input("Email")
uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)

# Button to start the workflow
if st.button("Start Knowledge Transfer"):
    if not github_username and not email and not uploaded_files:
        st.warning("Please provide at least one input.")
    else:
        with st.spinner("Processing your request..."):
            # Assemble the Crew
            crew = Crew(
                agents=[github_agent, email_agent, file_agent, document_agent, nlp_agent, knowledge_agent],
                tasks=[github_task, email_task, file_task, document_task, nlp_task, knowledge_task],
                process=Process.sequential,  # or Process.hierarchical
                verbose=True
            )

            # Prepare inputs for the crew
            inputs = {
                "github_username": github_username,
                "email": email,
                "uploaded_files": uploaded_files
            }

            # Kick off the crew
            result = crew.kickoff(inputs=inputs)

            # Display results
            st.subheader("Results")
            st.json(result)  # or use st.write(result) for a friendlier display

# Optional: Add instructions or help text
st.markdown("""
**Instructions:**  
- Enter your GitHub username, email, and upload relevant files.
- Relevant files include 
  1. Reports and documents written by you.
  2. Slides presented by you.
  3. Spreadsheets created by you.
- Click the button to start the knowledge transfer process.
- Results will appear below.
""")


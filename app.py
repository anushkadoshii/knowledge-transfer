import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3') 

import subprocess

import streamlit as st

# Ensure CrewAI is installed
try:
    import crewai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "crewai"])
    import crewai

from io import BytesIO

from agents import (
    github_agent, email_agent, file_agent, document_agent, nlp_agent, knowledge_agent
)
from tools import (
    GitHubCommitsTool, EmailProcessorTool, FileProcessorTool, DocumentTextExtractorTool, NLPAnalyzerTool, KnowledgeBaseBuilderTool
)
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
                # 1. GitHub Agent
                github_result = None
                if github_username:
                    github_tool = github_agent.tools[0]
                    github_result = github_tool._run(github_username, github_token)

                # 2. Email Agent
                email_result = None
                if email:
                    # You may want to ask for mapping and company_domain, else use defaults/demo
                    mapping = {email.split('@')[0]: email}
                    company_domain = email.split('@')[1] if '@' in email else "company.com"
                    email_tool = email_agent.tools[0]
                    email_result = email_tool._run(email.split('@')[0], mapping, company_domain)

                # 3. File Agent
                file_result = None
                if uploaded_files:
                    file_tool = file_agent.tools[0]
                    file_result = file_tool._run(uploaded_files)

                # 4. Document Agent
                document_result = None
                all_texts = []
                if uploaded_files:
                    document_tool = document_agent.tools[0]
                    document_result = document_tool._run(uploaded_files)
                    # Gather all text content for NLP
                    all_texts = [doc["content"] for doc in document_result if "content" in doc]

                # 5. NLP Agent
                nlp_result = None
                if all_texts:
                    nlp_tool = nlp_agent.tools[0]
                    nlp_result = nlp_tool._run(all_texts)

                # 6. Knowledge Base Agent
                knowledge_base_result = None
                if nlp_result:
                    kb_tool = knowledge_agent.tools[0]
                    knowledge_base_result = kb_tool._run(nlp_result)

                # Display results
                st.subheader("Results")
                if github_result is not None:
                    st.markdown("### GitHub Activity")
                    st.json(github_result[:3] if isinstance(github_result, list) else github_result)
                if email_result is not None:
                    st.markdown("### Email Insights")
                    st.json(email_result)
                if file_result is not None:
                    st.markdown("### Processed Files")
                    st.json(file_result)
                if document_result is not None:
                    st.markdown("### Extracted Document Text")
                    st.json(document_result)
                if nlp_result is not None:
                    st.markdown("### NLP Analysis")
                    st.json(nlp_result)
                if knowledge_base_result is not None:
                    st.markdown("### Knowledge Base")
                    st.json(knowledge_base_result)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


before2 = '''
import sys
import subprocess
import streamlit as st
from io import BytesIO

# Ensure CrewAI is installed
try:
    import crewai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "crewai"])
    import crewai

# Import agents and their tools directly
from agents import (
    github_agent, email_agent, file_agent,
    document_agent, nlp_agent, knowledge_agent
)
from utils.file_utils import extract_text_from_file

# For email tool, you'll need a mapping and company domain
# Example mapping (should be replaced with your actual mapping logic)
email_mapping = {"anushka doshi": "anushka.doshi@company.com"}
company_domain = "company.com"

st.title("Automated Knowledge Transfer (Agent-by-Agent)")

github_username = st.text_input("Enter your GitHub Username")
github_token = None
if github_username.strip():
    github_token = st.text_input("Enter your GitHub Personal Access Token", type="password")

person_name = st.text_input("Enter your Name (for email mapping)")
email = st.text_input("Enter your Email ID")

uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)

st.markdown("""
**Instructions:**
- Enter your GitHub username, email, and upload relevant files.
- Click the button to start the knowledge transfer process.
- Results will appear below, agent by agent.
""")

if st.button("Start Knowledge Transfer"):
    if not github_username and not email and not uploaded_files:
        st.warning("Please provide at least one input.")
    else:
        with st.spinner("Processing each agent..."):
            results = {}

            # --- GitHub Agent ---
            if github_username:
                try:
                    github_tool = github_agent.tools[0]
                    github_commits = github_tool._run(github_username, github_token)
                    results["GitHub Commits"] = github_commits
                    st.subheader("GitHub Commits")
                    st.json(github_commits[:5])  # show sample
                except Exception as e:
                    st.error(f"GitHub Agent Error: {e}")

            # --- Email Agent ---
            if person_name and email_mapping.get(person_name.lower()):
                try:
                    email_tool = email_agent.tools[0]
                    email_results = email_tool._run(person_name, email_mapping, company_domain)
                    results["Email Analysis"] = email_results
                    st.subheader("Email Analysis")
                    st.json(email_results)
                except Exception as e:
                    st.error(f"Email Agent Error: {e}")

            # --- File Agent ---
            if uploaded_files:
                try:
                    file_tool = file_agent.tools[0]
                    file_data = file_tool._run(uploaded_files)
                    results["File Metadata"] = file_data
                    st.subheader("File Metadata")
                    st.json(file_data)
                except Exception as e:
                    st.error(f"File Agent Error: {e}")

            # --- Document Agent ---
            if uploaded_files:
                try:
                    document_tool = document_agent.tools[0]
                    document_texts = document_tool._run(uploaded_files)
                    results["Extracted Document Texts"] = document_texts
                    st.subheader("Extracted Document Texts")
                    st.json(document_texts)
                except Exception as e:
                    st.error(f"Document Agent Error: {e}")

            # --- NLP Agent ---
            if uploaded_files:
                try:
                    nlp_tool = nlp_agent.tools[0]
                    # Collect all extracted text from previous step
                    texts = [doc['content'] for doc in results.get("Extracted Document Texts", []) if isinstance(doc, dict)]
                    nlp_results = nlp_tool._run(texts)
                    results["NLP Analysis"] = nlp_results
                    st.subheader("NLP Analysis")
                    st.json(nlp_results)
                except Exception as e:
                    st.error(f"NLP Agent Error: {e}")

            # --- Knowledge Base Agent ---
            if "NLP Analysis" in results:
                try:
                    kb_tool = knowledge_agent.tools[0]
                    kb_results = kb_tool._run(results["NLP Analysis"])
                    results["Knowledge Base"] = kb_results
                    st.subheader("Knowledge Base")
                    st.json(kb_results)
                except Exception as e:
                    st.error(f"Knowledge Base Agent Error: {e}")

            st.success("All agents have run. See results above.")
'''

before_prev = '''import sys
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
'''

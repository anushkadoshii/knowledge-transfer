import subprocess, sys

try:
  import crewai 
except ImportError:
  print("CrewAI not found. Installing...")
  try:
    # Use pip to install CrewAI
    subprocess.check_call([sys.executable, "-m", "pip", "install", "crewai"])
    from crewai import Task 
    print("CrewAI installed successfully")
  except subprocess.CalledProcessError as e:
    print(f"Installation failed: {e}")
    sys.exit(1)
 
from agents import (
    github_agent,
    email_agent,
    file_agent,
    document_agent,
    nlp_agent,
    knowledge_agent
) 

github_task = Task(
    description="""
    Thoroughly analyze the provided GitHub username to extract and summarize the user's commit history.
    Examine code changes, commit messages, and repository activity to identify patterns, contributions, and project involvement.
    Highlight significant commits, frequent collaborators, and notable trends in the user's development workflow.
    """,
    agent=github_agent,
    expected_output="""
    A comprehensive summary of the user's GitHub activity, including:
    - Overview of most active repositories
    - Key contributions and code changes
    - Notable patterns or trends in commit behavior
    - List of frequent collaborators (if available)
    """
)

email_task = Task(
    description="""
    Retrieve, parse, and analyze the user's emails to capture the essence of important communications.
    Identify main topics, action items, and key decisions discussed in the emails.
    Summarize conversations, highlight recurring themes, and note any critical information or attachments.
    """,
    agent=email_agent,
    expected_output="""
    A structured summary of the user's email communications, including:
    - Main topics and recurring themes
    - Important action items and decisions
    - Key conversations and notable attachments
    - Concise overview of each major thread
    """
)

file_task = Task(
    description="""
    Process and organize all files uploaded by the user.
    Verify file formats, extract metadata, and ensure files are ready for downstream analysis.
    Maintain data integrity and provide a clear inventory of available files.
    """,
    agent=file_agent,
    expected_output="""
    A detailed list of all processed files, including:
    - File names and types
    - Sizes and metadata
    - Status of processing (success/failure)
    - Notes on any issues encountered
    """
)

document_task = Task(
    description="""
    Extract and structure text from all uploaded documents, presentations, and spreadsheets.
    Convert diverse file formats into machine-readable text for further analysis.
    Ensure all content is accessible and ready for NLP processing.
    """,
    agent=document_agent,
    expected_output="""
    A collection of extracted text from each uploaded file, including:
    - Source file name
    - Extracted content as plain text
    - Notes on extraction quality or issues
    """
)

nlp_task = Task(
    description="""
    Perform advanced natural language processing on the extracted text.
    Identify named entities, summarize key points, and detect main topics.
    Highlight important information and prepare insights for knowledge base integration.
    """,
    agent=nlp_agent,
    expected_output="""
    A structured NLP analysis, including:
    - Named entities (people, organizations, dates, etc.)
    - Concise summaries of each document
    - Main topics and themes
    - Notable insights and patterns
    """
)

knowledge_task = Task(
    description="""
    Build, organize, and query a knowledge base using insights from all previous tasks.
    Integrate summaries, entities, and topics into a coherent, searchable structure.
    Ensure the knowledge base is actionable and supports efficient information retrieval.
    """,
    agent=knowledge_agent,
    expected_output="""
    A fully structured knowledge base, including:
    - Integrated summaries and entities from all sources
    - Searchable and categorized insights
    - Ready-to-use outputs for onboarding, reporting, or decision-making
    """
)


all_tasks = [github_task, email_task, file_task, document_task, nlp_task, knowledge_task]

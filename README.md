# knowledge-transfer

## File Structure

```
knowledge-transfer/
│
├── app.py                         # Main Streamlit app (UI & workflow orchestration)
│
├── agents.py                      # CrewAI agent definitions (roles, goals, tools)
├── tasks.py                       # CrewAI task definitions (descriptions, agents, outputs)
├── tools.py                       # CrewAI tool definitions (custom functions/APIs)
│
├── data/
│   ├── raw/                       # Raw uploaded files
│   ├── processed/                 # Processed/cleaned files
│   └── knowledge_base/            # Structured knowledge outputs
│
├── utils/
│   ├── auth.py                    # Authentication helpers
│   ├── github_utils.py            # GitHub API helpers
│   ├── email_utils.py             # Email API/parsing helpers
│   ├── file_utils.py              # File format detection, conversion
│   └── cache.py                   # Streamlit caching utilities
│
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables (API keys, secrets)
├── .gitignore
└── README.md

```

---

# Agents and Tasks Documentation

This document provides an overview of the agents and tasks defined in the CrewAI-powered knowledge transfer automation project.

## Agents


### 1. GitHub Data Specialist

Extracts and analyzes GitHub commit history to uncover development patterns and contributions.

### 2. Email Communication Analyst

Retrieves, parses, and summarizes email communications to capture key conversations and decisions.

### 3. File Management and Processing Specialist

Handles user-uploaded files, ensuring proper format detection, storage, and initial processing.

### 4. Document Content Extractor

Extracts and structures text from documents, presentations, and spreadsheets to enable knowledge extraction.

### 5. Natural Language Processing Specialist

Performs named entity recognition, summarization, and topic modeling to distill key insights from text data.

### 6. Knowledge Base Architect

Builds, maintains, and queries a structured knowledge base to support efficient information retrieval.


---


## Tasks

### 1. GitHub Task
- **Description:** Thoroughly analyze the provided GitHub username to extract and summarize the user's commit history, highlighting significant commits and development trends.
- **Expected Output:** A comprehensive summary of the user's GitHub activity including key contributions and notable patterns.

### 2. Email Task
- **Description:** Retrieve, parse, and analyze the user's emails to capture important communications, action items, and decisions.
- **Expected Output:** A structured summary of the user's email communications highlighting main topics and key conversations.

### 3. File Task
- **Description:** Process and organize all files uploaded by the user, verifying formats and extracting metadata.
- **Expected Output:** A detailed list of processed files with metadata and processing status.

### 4. Document Task
- **Description:** Extract and structure text from uploaded documents, presentations, and spreadsheets for further analysis.
- **Expected Output:** Extracted text content from each file with notes on extraction quality.

### 5. NLP Task
- **Description:** Perform advanced NLP on extracted text to identify entities, summarize content, and detect main topics.
- **Expected Output:** Structured NLP analysis including named entities, summaries, and notable insights.

### 6. Knowledge Task
- **Description:** Build and query a knowledge base integrating insights from all previous tasks to support efficient information retrieval.
- **Expected Output:** A fully structured knowledge base with integrated summaries and searchable insights.




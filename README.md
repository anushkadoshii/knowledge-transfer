# knowledge-transfer

## File Structure

```
knowledge_transfer_streamlit/
│
├── app.py                      # Main Streamlit app (UI & workflow)
│
├── agents/
│   ├── github_agent.py         # GitHub scraping logic
│   ├── email_agent.py          # Email fetching/parsing logic
│   ├── file_agent.py           # Handles file uploads & parsing
│   ├── document_agent.py       # Document/report/slides/sheets processing
│   ├── nlp_agent.py            # NER, summarization, topic modeling, etc.
│   ├── knowledge_agent.py      # Builds/queries knowledge graph or DB
│   └── orchestrator.py         # Coordinates agent workflows
│
├── utils/
│   ├── auth.py                 # Authentication helpers (OAuth, secrets)
│   ├── github_utils.py         # GitHub API helpers
│   ├── email_utils.py          # Email API/parsing helpers
│   ├── file_utils.py           # File format detection, conversion
│   └── cache.py                # Streamlit caching utilities
│
├── data/
│   ├── raw/                    # Raw uploaded files
│   ├── processed/              # Processed/cleaned files
│   └── knowledge_base/         # Structured knowledge outputs
│
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys, secrets)
├── .gitignore
└── README.md
```

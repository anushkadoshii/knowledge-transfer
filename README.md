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

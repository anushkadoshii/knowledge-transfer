# knowledge-transfer

## File Structure

```
knowledge-transfer/
│
├── app.py                      # Main Streamlit app (UI & workflow)
│
├── agents/
│   ├── github_agent.py         # GitHub agent logic (as CrewAI tool/agent)
│   ├── email_agent.py          # Email agent logic (as CrewAI tool/agent)
│   ├── file_agent.py           # File agent logic (as CrewAI tool/agent)
│   └── document_agent.py       # Document agent logic (as CrewAI tool/agent)
│
├── utils/
│   └── auth.py                 # Authentication helpers
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── knowledge_base/
│
├── requirements.txt
├── .env
└── README.md

```

# AI Impact Auditor Backend MVP

FastAPI + SQLite MVP for GitHub, Jira and CSV time tracking.

## Run
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs

Create a project, load demo evidence, or configure GITHUB_TOKEN / Jira credentials for live ingestion. Upload `sample_time_tracking.csv` to the time-tracking endpoint. The PDF endpoint generates a management/client report.

The calculation engine is deliberately deterministic. AI can later be added for classification/narrative, but it should not be trusted to calculate money or time.

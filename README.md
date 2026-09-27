# Churn Risk Estimator — Streamlit UI

🔗 **Live demo:** https://capstone-project-sk-churn-streamlit.onrender.com

🔗 **Main API & ML Backend:** [capstone-project-sk-churn-api](https://github.com/StanleyNeo/capstone-project-sk-churn-api)

🔗 **API docs:** https://capstone-project-sk-churn-api.onrender.com/docs

**Stack:** Streamlit · FastAPI (backend) · Render (hosting) · Python 3.11

> ⚠️ **Free tier:** The Render instance spins down after 15 minutes of inactivity. The first request may take up to 50 seconds while the backend cold-starts.

---

## About
This is the frontend interface for the Telco Customer Churn prediction model. It provides a simple form where a user can input a customer's profile and receive a churn probability + plain-English risk verdict. 

It communicates with the FastAPI backend via the `API_URL` environment variable.

## How to run locally
**Prereqs:** Python 3.11+, and the FastAPI backend running locally (or pointing to the live Render API).

```bash
# 1. Setup
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 2. Run Streamlit (ensure API_URL points to your local or remote backend)
$env:API_URL="http://localhost:5001" # Or use the live Render URL
streamlit run app.py

```

Open http://localhost:8501 — fill the form, click Estimate churn risk.

## Deployment (Render)
- Build Command: pip install -r requirements.txt
- Start Command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
- Environment Variable: API_URL=https://capstone-project-sk-churn-api.onrender.com
- Python Version: Pinned to 3.11.9 via .python-version for reproducible builds.
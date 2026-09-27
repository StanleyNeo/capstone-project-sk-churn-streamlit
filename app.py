import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:5001")

st.set_page_config(page_title="Churn Risk Estimator", page_icon="📉", layout="centered")

st.title("Churn Risk Estimator")
st.caption("LogisticRegression · ROC-AUC 0.84 · served via FastAPI")

with st.form("churn_form"):
    col1, col2 = st.columns(2)

    with col1:
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
        monthly = st.number_input("Monthly Charges ($)", min_value=0.0, value=70.35, step=0.01)
        total = st.number_input("Total Charges ($)", min_value=0.0, value=840.50, step=0.01)
        senior = st.selectbox("Senior Citizen", ["No", "Yes"])
        gender = st.selectbox("Gender", ["Female", "Male"])
        partner = st.selectbox("Partner", ["No", "Yes"])
        dependents = st.selectbox("Dependents", ["No", "Yes"])

    with col2:
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        payment = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check",
            "Bank transfer (automatic)", "Credit card (automatic)",
        ])
        tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        phone_service = st.selectbox("Phone Service", ["No", "Yes"])
        paperless = st.selectbox("Paperless Billing", ["No", "Yes"])

    submitted = st.form_submit_button("Estimate churn risk")

if submitted:
    payload = {
        "SeniorCitizen": 1 if senior == "Yes" else 0,
        "tenure": int(tenure),
        "MonthlyCharges": float(monthly),
        "TotalCharges": float(total),
        "gender": gender,
        "Partner": partner,
        "Dependents": dependents,
        "PhoneService": phone_service,
        "MultipleLines": "No",
        "InternetService": internet,
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": tech_support,
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
    }

    try:
        r = requests.post(f"{API_URL}/predict", json=payload, timeout=60)
        r.raise_for_status()
        body = r.json()
        if not body.get("success"):
            st.error(f"API error: {body.get('error', 'unknown')}")
        else:
            data = body["data"]
            prob = data["probability"]
            verdict = data["verdict"]
            st.metric("Churn probability", f"{prob * 100:.1f}%")
            color = {"high": "🔴", "medium": "🟠", "low": "🟢"}[verdict]
            st.subheader(f"{color} {verdict.upper()} RISK")
            st.progress(min(max(prob, 0.0), 1.0))
            st.caption(f"thresholds: {data['thresholds']}")
            st.caption(f"model: {data['model']} · v{data['version']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to reach API: {e}")

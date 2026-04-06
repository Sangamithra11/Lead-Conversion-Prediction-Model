# app.py
# ─────────────────────────────────────────────
# Lead Conversion Predictor - Simple Streamlit UI
# ─────────────────────────────────────────────
# WHAT THIS APP DOES:
#   You enter details about a lead (a potential customer),
#   and the app tells you HOW LIKELY that lead will convert
#   into an actual paying customer.
#
# INPUT  → Lead Source, Service, Follow-Up Count
# OUTPUT → Conversion Probability (%) + Lead Label (Hot/Warm/Cold)
# ─────────────────────────────────────────────

import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# ── Load the trained model ──────────────────────────────────────
# This is the XGBoost model you saved with pickle.dump() in your notebook
model = pickle.load(open("model.pkl", "rb"))

# ── App Title ───────────────────────────────────────────────────
st.title("Lead Conversion Predictor")
st.write("Fill in the lead details below and click **Predict** to see the result.")

st.divider()

# ── INPUT SECTION ───────────────────────────────────────────────
# These are the 6 features your model was trained on:
# LeadSource, ServiceInterested, FollowUpCount,
# IsHighFollowUp, IsReferral, ServiceCategory

# Input 1: Lead Source — where did this lead come from?
lead_source = st.selectbox(
    "Lead Source",
    ["Website", "Referral", "Cold Call", "Indeed", "Social Media", "Unknown"]
)

# Input 2: Service the lead is interested in
service = st.selectbox(
    "Service Interested",
    ["SEO", "Web Development", "Digital Marketing", "Consulting", "PPC", "Branding", "Unknown"]
)

# Input 3: How many times have you followed up with this lead?
follow_up = st.number_input("Follow Up Count", min_value=0, max_value=20, value=1)

st.divider()

# ── PREDICT BUTTON ──────────────────────────────────────────────
if st.button("Predict"):

    # ── Build the input the same way you did in your notebook ──

    # Encode LeadSource using the same categories from training
    LEAD_SOURCES = ["Website", "Referral", "Cold Call", "Indeed", "Social Media", "Unknown"]
    SERVICES     = ["SEO", "Web Development", "Digital Marketing", "Consulting", "PPC", "Branding", "Unknown"]

    le_source  = LabelEncoder().fit(LEAD_SOURCES)
    le_service = LabelEncoder().fit(SERVICES)

    # Engineered features (same as your notebook)
    is_high_follow_up = 1 if follow_up > 2 else 0       # IsHighFollowUp
    is_referral       = 1 if lead_source == "Referral" else 0  # IsReferral
    service_category  = le_service.transform([service])[0]     # ServiceCategory (numeric)
    lead_source_enc   = le_source.transform([lead_source])[0]  # LeadSource (numeric)
    service_enc       = le_service.transform([service])[0]     # ServiceInterested (numeric)

    # This must match EXACTLY the column order used during model.fit() in your notebook:
    # X = df[["LeadSource","ServiceInterested","FollowUpCount","IsHighFollowUp","IsReferral","ServiceCategory"]]
    input_df = pd.DataFrame({
        "LeadSource":        [lead_source_enc],
        "ServiceInterested": [service_enc],
        "FollowUpCount":     [follow_up],
        "IsHighFollowUp":    [is_high_follow_up],
        "IsReferral":        [is_referral],
        "ServiceCategory":   [service_category]
    })

    # ── Get prediction from model ──
    prob  = model.predict_proba(input_df)[:, 1][0]   # probability of converting (class = 1)
    score = int(prob * 100)                           # turn it into a 0-100 score

    # ── OUTPUT SECTION ──────────────────────────────────────────
    # Output 1: Probability as a progress bar
    st.subheader("Prediction Result")
    st.metric(label="Conversion Probability", value=f"{score}%")
    st.progress(score)  # visual bar from 0 to 100

    # Output 2: Lead Label based on score
    if score >= 70:
        st.success("🔥 Hot Lead — High chance of conversion. Follow up immediately!")
    elif score >= 40:
        st.warning("🌤️ Warm Lead — Moderate chance. Keep nurturing this lead.")
    else:
        st.error("❄️ Cold Lead — Low chance. Add to drip campaign.")

    # Output 3: Show what was sent to the model (useful for debugging / understanding)
    with st.expander("See model input (for debugging)"):
        st.dataframe(input_df)
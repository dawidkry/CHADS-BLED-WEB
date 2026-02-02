import streamlit as st

# --- 1. CLINICAL DATA TABLES ---
CHADS_RISK = {0: 0, 1: 1.3, 2: 2.2, 3: 3.2, 4: 4.0, 5: 6.7, 6: 9.8, 7: 9.6, 8: 6.7, 9: 15.2}
BLED_RISK = {0: 1.1, 1: 1.0, 2: 1.9, 3: 3.7, 4: 8.7, 5: 12.5}

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(page_title="CHADS-BLED Benefit Calc", page_icon="⚖️")

st.title("⚖️ CHADS-BLED Benefit Calc")
st.markdown("### Integrated Stroke vs. Bleed Risk Assessment")

# --- 3. SIDEBAR / EVIDENCE ---
with st.sidebar:
    st.header("Clinical Evidence")
    st.write("**CHA₂DS₂-VASc:** Lip GY, et al. (2010)")
    st.write("**HAS-BLED:** Pisters R, et al. (2010)")
    st.divider()
    st.caption("This tool is for clinical decision support and does not replace professional judgment.")

# --- 4. INPUT SECTION ---
age = st.slider("Patient Age", 18, 100, 65)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Stroke Factors")
    female = st.checkbox("Female Sex")
    htn = st.checkbox("Hypertension")
    hf = st.checkbox("Heart Failure History")
    dm = st.checkbox("Diabetes")
    stroke = st.checkbox("Stroke/TIA History")
    vasc = st.checkbox("Vascular Disease (MI/PAD)")

with col2:
    st.subheader("Bleed Factors")
    renal = st.checkbox("Renal Impairment")
    liver = st.checkbox("Liver Impairment")
    bleed = st.checkbox("Prior Major Bleed")
    drugs = st.checkbox("Antiplatelets / Alcohol")

# --- 5. CALCULATION LOGIC ---
chads = sum([age >= 75, age >= 65, female, htn, dm, stroke*2, hf, vasc])
has_bled = sum([htn, renal, liver, stroke, bleed, age >= 65, drugs])

stroke_risk = CHADS_RISK.get(chads, 15.2)
bleed_risk = BLED_RISK.get(has_bled, 12.5)
net_benefit = stroke_risk - bleed_risk

# --- 6. DISPLAY RESULTS ---
st.divider()
res_col1, res_col2 = st.columns(2)

res_col1.metric("CHA₂DS₂-VASc Score", f"{chads}", f"{stroke_risk}% risk/yr")
res_col2.metric("HAS-BLED Score", f"{has_bled}", f"{bleed_risk}% risk/yr")

if net_benefit > 1.5:
    st.success(f"**Net Benefit for Anticoagulation: +{net_benefit:.1f}%**")
elif net_benefit < 0:
    st.error(f"**Warning: Bleed risk exceeds stroke risk ({net_benefit:.1f}%)**")
else:
    st.warning(f"**Equivocal Benefit: {net_benefit:.1f}%**")

# --- 7. DOCUMENTATION GENERATOR ---
st.subheader("📋 Clinical Note (Copy/Paste)")
note = f"CHADS-BLED Calc: CHA2DS2-VASc {chads} ({stroke_risk}%/yr); HAS-BLED {has_bled} ({bleed_risk}%/yr). Net Benefit: {net_benefit:.1f}%."
st.code(note, language="text")

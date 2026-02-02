import streamlit as st

# --- 1. CLINICAL DATA TABLES ---
CHADS_RISK = {0: 0, 1: 1.3, 2: 2.2, 3: 3.2, 4: 4.0, 5: 6.7, 6: 9.8, 7: 9.6, 8: 6.7, 9: 15.2}
BLED_RISK = {0: 1.1, 1: 1.0, 2: 1.9, 3: 3.7, 4: 8.7, 5: 12.5}

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(page_title="CHADS-BLED Benefit", page_icon="🩺", layout="centered")

# --- 3. HEADER & RESET ---
st.title("⚖️ CHADS-BLED Benefit Calc")
st.markdown("### Integrated Stroke vs. Bleeding Risk")

if st.button("Clear / New Patient"):
    st.rerun()

# --- 4. INPUT SECTION ---
st.divider()
age = st.slider("Patient Age", 18, 100, 65)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Stroke Factors")
    female = st.checkbox("Female Sex")
    htn_chads = st.checkbox("Hypertension", help="History of HTN or on current therapy")
    hf = st.checkbox("Heart Failure History", help="Including LVD or EF < 40%")
    dm = st.checkbox("Diabetes Mellitus")
    stroke_chads = st.checkbox("Prior Stroke / TIA", help="Counts for 2 points")
    vasc = st.checkbox("Vascular Disease", help="Prior MI, PAD, or Aortic Plaque")

with col2:
    st.subheader("Bleeding Factors")
    # Immediate transparency for the Hypertension distinction
    htn_bled = st.checkbox("Uncontrolled HTN", help="Systolic BP > 160 mmHg")
    st.caption("*(Targeting SBP > 160 per HAS-BLED)*")
    
    renal = st.checkbox("Renal Impairment", help="Cr > 2.26 mg/dL, Dialysis, or Transplant")
    liver = st.checkbox("Liver Impairment", help="Cirrhosis or Bilirubin > 2x Normal")
    bleed = st.checkbox("Prior Major Bleed", help="Prior bleed or predisposition (e.g., anemia)")
    drugs = st.checkbox("NSAIDs / Alcohol", help="Antiplatelets/NSAIDs or >8 drinks/week")

# --- 5. CALCULATION LOGIC ---
# Points for Stroke: Stroke history counts as 2, Age >= 75 counts as 2 (1 point from slider, 1 extra here)
chads_score = sum([
    age >= 75, age >= 65, female, htn_chads, dm, 
    stroke_chads * 2, hf, vasc
])

# Points for Bleed: Stroke history counts as 1 point in HAS-BLED
bled_score = sum([
    htn_bled, renal, liver, stroke_chads, bleed, 
    age >= 65, drugs
])

s_risk = CHADS_RISK.get(chads_score, 15.2)
b_risk = BLED_RISK.get(bled_score, 12.5)
net_benefit = s_risk - b_risk

# --- 6. RESULTS DISPLAY ---
st.divider()
res1, res2 = st.columns(2)

res1.metric("CHA₂DS₂-VASc Score", f"{chads_score}", f"{s_risk}% Stroke Risk/yr")
res2.metric("HAS-BLED Score", f"{bled_score}", f"{b_risk}% Bleed Risk/yr")

if net_benefit > 1.5:
    st.success(f"**Net Benefit: +{net_benefit:.1f}%** (Favors Anticoagulation)")
elif net_benefit < 0:
    st.error(f"**Warning: Bleed risk exceeds stroke risk ({net_benefit:.1f}%)**")
else:
    st.warning(f"**Equivocal Benefit: {net_benefit:.1f}%**")

# --- 7. CLINICAL DOCUMENTATION ---
st.subheader("📋 Clinical Note")
clinical_note = f"CHADS-BLED: CHA2DS2-VASc {chads_score} ({s_risk}%/yr); HAS-BLED {bled_score} ({b_risk}%/yr). Net Benefit: {net_benefit:.1f}%."
st.code(clinical_note, language="text")

with st.expander("View Evidence"):
    st.write("**CHA₂DS₂-VASc:** Lip GY, et al. (2010)")
    st.write("**HAS-BLED:** Pisters R, et al. (2010)")

import streamlit as st

# --- 1. SESSION STATE INITIALIZATION (The Reset Logic) ---
if 'reset_key' not in st.session_state:
    st.session_state.reset_key = 0

def reset_callback():
    # Incrementing the key forces all widgets to re-render from scratch
    st.session_state.reset_key += 1

# --- 2. CLINICAL DATA TABLES ---
CHADS_RISK = {0: 0, 1: 1.3, 2: 2.2, 3: 3.2, 4: 4.0, 5: 6.7, 6: 9.8, 7: 9.6, 8: 6.7, 9: 15.2}
BLED_RISK = {0: 1.1, 1: 1.0, 2: 1.9, 3: 3.7, 4: 8.7, 5: 12.5}

# --- 3. PAGE CONFIGURATION ---
st.set_page_config(page_title="CHADS-BLED Benefit Calc", page_icon="🩺", layout="centered")

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🧰 MedCalc Menu")
    st.write("**Tool:** CHADS-BLED Benefit")
    st.divider()
    # The Reset Button calls the callback function
    st.button("Clear / New Patient", on_click=reset_callback)
    st.divider()
    st.header("Clinical Evidence")
    st.caption("CHA₂DS₂-VASc: Lip GY, et al. (2010)")
    st.caption("HAS-BLED: Pisters R, et al. (2010)")
    st.divider()
    st.caption("Decision Support Tool v2.1")

# --- 5. CHADS-BLED CALCULATOR ---
st.title("⚖️ Stroke vs. Bleed Risk")
st.markdown("### Integrated Assessment")

# Every input widget now has a unique 'key' tied to st.session_state.reset_key
age = st.slider("Patient Age", 18, 100, 65, key=f"age_{st.session_state.reset_key}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Stroke Factors")
    female = st.checkbox("Female Sex", key=f"fem_{st.session_state.reset_key}")
    htn_chads = st.checkbox("Hypertension", help="History of HTN or on therapy", key=f"htnc_{st.session_state.reset_key}")
    hf = st.checkbox("Heart Failure History", key=f"hf_{st.session_state.reset_key}")
    dm = st.checkbox("Diabetes", key=f"dm_{st.session_state.reset_key}")
    stroke_chads = st.checkbox("Stroke/TIA/TE History", key=f"str_{st.session_state.reset_key}")
    vasc = st.checkbox("Vascular Disease", help="Prior MI, PAD, or aortic plaque", key=f"vasc_{st.session_state.reset_key}")

with col2:
    st.subheader("Bleed Factors")
    htn_bled = st.checkbox("Uncontrolled HTN", help="Current SBP > 160 mmHg", key=f"htnb_{st.session_state.reset_key}")
    st.caption("↑ SBP > 160 per HAS-BLED")
    renal = st.checkbox("Renal Impairment", help="Cr > 2.26, dialysis, or transplant", key=f"ren_{st.session_state.reset_key}")
    liver = st.checkbox("Liver Impairment", help="Cirrhosis or Bilirubin > 2x upper limit", key=f"liv_{st.session_state.reset_key}")
    bleed = st.checkbox("Prior Major Bleed", key=f"bld_{st.session_state.reset_key}")
    drugs = st.checkbox("NSAIDs / Alcohol", help="Antiplatelets or >8 drinks/week", key=f"drg_{st.session_state.reset_key}")

# --- 6. CALCULATION LOGIC ---
chads = sum([age >= 75, age >= 65, female, htn_chads, dm, stroke_chads*2, hf, vasc])
has_bled = sum([htn_bled, renal, liver, stroke_chads, bleed, age >= 65, drugs])

s_risk = CHADS_RISK.get(chads, 15.2)
b_risk = BLED_RISK.get(has_bled, 12.5)
net = s_risk - b_risk

# --- 7. DISPLAY RESULTS ---
st.divider()
res_col1, res_col2 = st.columns(2)

res_col1.metric("CHA₂DS₂-VASc Score", f"{chads}", f"{s_risk}% risk/yr")
res_col2.metric("HAS-BLED Score", f"{has_bled}", f"{b_risk}% risk/yr")

if net > 1.5:
    st.success(f"**Net Benefit: +{net:.1f}% (Favors OAC)**")
elif net < 0:
    st.error(f"**Net Benefit: {net:.1f}% (Favors Observation)**")
else:
    st.warning(f"**Equivocal Benefit: {net:.1f}%**")

# --- 8. CLINICAL NOTE GENERATOR ---
st.subheader("📋 Clinical Note")
note = f"CHADS-BLED Calc: CHA2DS2-VASc {chads} ({s_risk}%/yr); HAS-BLED {has_bled} ({b_risk}%/yr). Net Benefit: {net:.1f}%."
st.code(note, language="text")

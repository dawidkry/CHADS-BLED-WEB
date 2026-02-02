import streamlit as st

# --- 1. SESSION STATE INITIALIZATION ---
# This ensures the "Reset" actually clears the checkboxes
if 'reset_key' not in st.session_state:
    st.session_state.reset_key = 0

def reset_callback():
    st.session_state.reset_key += 1

# --- 2. CLINICAL DATA TABLES ---
CHADS_RISK = {0: 0, 1: 1.3, 2: 2.2, 3: 3.2, 4: 4.0, 5: 6.7, 6: 9.8, 7: 9.6, 8: 6.7, 9: 15.2}
BLED_RISK = {0: 1.1, 1: 1.0, 2: 1.9, 3: 3.7, 4: 8.7, 5: 12.5}

# --- 3. PAGE CONFIGURATION ---
st.set_page_config(page_title="MedCalc Engine", page_icon="🩺", layout="centered")

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🧰 MedCalc Menu")
    app_mode = st.radio("Select Tool:", ["CHADS-BLED Benefit", "Sodium Engine (AM)"])
    st.divider()
    # The button now calls the reset function
    st.button("Clear / New Patient", on_click=reset_callback)
    st.divider()
    st.caption("Decision Support Tool v2.0")

# --- 5. UPDATED INPUT SECTION ---
# Add 'key' arguments to your checkboxes/sliders using the reset_key
# This forces them to re-render when the key changes.

if app_mode == "CHADS-BLED Benefit":
    st.title("⚖️ Stroke vs. Bleed Risk")
    
    # We add f"_{st.session_state.reset_key}" to every key
    age = st.slider("Patient Age", 18, 100, 65, key=f"age_{st.session_state.reset_key}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Stroke Factors")
        female = st.checkbox("Female Sex", key=f"fem_{st.session_state.reset_key}")
        htn_chads = st.checkbox("Hypertension", help="History of HTN", key=f"htnc_{st.session_state.reset_key}")
        hf = st.checkbox("Heart Failure History", key=f"hf_{st.session_state.reset_key}")
        dm = st.checkbox("Diabetes", key=f"dm_{st.session_state.reset_key}")
        stroke_chads = st.checkbox("Stroke/TIA/TE History", key=f"str_{st.session_state.reset_key}")
        vasc = st.checkbox("Vascular Disease", key=f"vasc_{st.session_state.reset_key}")

    with col2:
        st.subheader("Bleed Factors")
        htn_bled = st.checkbox("Uncontrolled HTN", key=f"htnb_{st.session_state.reset_key}")
        # ... apply the same key pattern to the rest of the inputs ...

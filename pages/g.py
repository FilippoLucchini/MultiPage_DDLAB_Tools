import streamlit as st

# Define reagent kits
REAGENT_KITS = {
    "Kit A": {
        "Reaction 1": {"Reagent 1": 10, "Reagent 2": 5},
        "Reaction 2": {"Reagent 3": 2, "Reagent 4": 1}
    },
    "Kit B": {
        "Prep": {"Reagent X": 8, "Reagent Y": 3},
        "Amplification": {"Reagent Z": 2, "Reagent W": 4}
    }
}

st.title("Select a Reagent Kit")

# Create buttons for each kit
for kit_name in REAGENT_KITS.keys():
    if st.button(kit_name):
        st.session_state.selected_kit = kit_name
        st.session_state.kit_data = REAGENT_KITS[kit_name]
        st.switch_page("pages/kit_calculator.py")  # Requires Streamlit >= 1.12

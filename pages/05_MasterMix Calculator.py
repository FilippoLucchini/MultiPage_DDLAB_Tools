import streamlit as st
import pandas as pd

# Define kits with multiple reactions
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

# Initialize session state
if "selected_kit" not in st.session_state:
    st.session_state.selected_kit = None

# Kit selection view
if st.session_state.selected_kit is None:
    st.title("Select a Reagent Kit")
    for kit_name in REAGENT_KITS.keys():
        if st.button(kit_name):
            st.session_state.selected_kit = kit_name
            st.session_state.kit_data = REAGENT_KITS[kit_name]

# Reaction calculator view
else:
    kit_name = st.session_state.selected_kit
    kit_data = st.session_state.kit_data
    st.title(f"Master Mix Calculator for {kit_name}")

    # Ask once for samples and excess
    num_samples = st.number_input("Number of samples", min_value=1, step=1)
    excess_pct = st.slider("Excess (%)", min_value=0, max_value=100, value=10)
    excess_factor = 1 + (excess_pct / 100)

 # Calculate button
if st.button("Calculate Reagents"):
    st.subheader(f"Calculated Reagent Amounts for {num_samples} samples")

    results = []
    reaction_names = list(kit_data.keys())
    columns = st.columns(len(reaction_names))  # One column per reaction

    for col, reaction_name in zip(columns, reaction_names):
        reagents = kit_data[reaction_name]
        reaction_results = []

        for reagent, per_sample in reagents.items():
            total = per_sample * num_samples * excess_factor
            reaction_results.append({
                "Reagent": reagent,
                "Amount": round(total, 2)
            })
            results.append({
                "Reaction": reaction_name,
                "Reagent": reagent,
                "Amount": round(total, 2)
            })

        # Display table in column
        with col:
            st.markdown(f"**{reaction_name}**")
            st.table(pd.DataFrame(reaction_results))

    # Export CSV
    df = pd.DataFrame(results)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download All Reagents as CSV", data=csv, file_name=f"{kit_name}_reagents.csv", mime="text/csv")


    # Back button
    if st.button("🔙 Back to Kit Selection"):
        st.session_state.selected_kit = None
        st.session_state.kit_data = None


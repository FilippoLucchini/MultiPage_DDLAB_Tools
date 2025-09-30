# pages/2_reagent_calculator.py
import streamlit as st

# Define reagent kits and their per-sample amounts (example values in mL)
REAGENT_KITS = {
    "Kit A": {"Reagent 1": 5, "Reagent 2": 3, "Reagent 3": 2},
    "Kit B": {"Reagent X": 2, "Reagent Y": 4, "Reagent Z": 1.5},
    "Kit C": {"Reagent M": 10, "Reagent N": 5},
}

st.title("Reagent Calculator")

st.write("Choose a reagent kit:")

# Step 1: Kit selection buttons
selected_kit = None
cols = st.columns(len(REAGENT_KITS))
for i, kit_name in enumerate(REAGENT_KITS.keys()):
    if cols[i].button(kit_name):
        selected_kit = kit_name

# Step 2: If a kit is selected, ask for number of samples and excess
if selected_kit:
    st.subheader(f"Selected Kit: {selected_kit}")
    num_samples = st.number_input("Number of samples", min_value=1, value=1, step=1)
    excess_percent = st.number_input("Excess percentage (%)", min_value=0.0, value=10.0, step=0.1)

    if st.button("Calculate reagents"):
        st.subheader("Reagent amounts (with excess)")
        kit = REAGENT_KITS[selected_kit]
        total_reagents = {}
        for reagent, amount_per_sample in kit.items():
            total_amount = amount_per_sample * num_samples * (1 + excess_percent / 100)
            total_reagents[reagent] = total_amount

        # Display the results
        for reagent, total_amount in total_reagents.items():
            st.write(f"{reagent}: {total_amount:.2f} mL")

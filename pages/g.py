import streamlit as st

# Define reagent kits and their per-sample reagent requirements
REAGENT_KITS = {
    "Kit A": {"Reagent 1": 10, "Reagent 2": 5},
    "Kit B": {"Reagent X": 8, "Reagent Y": 3, "Reagent Z": 2},
    "Kit C": {"Buffer": 15, "Enzyme": 1.5}
}

# Step 1: Select a reagent kit
st.title("Reagent Kit Calculator")
st.subheader("Choose a reagent kit")

selected_kit = st.radio("Available Kits", list(REAGENT_KITS.keys()))

# Step 2: Input sample count and excess percentage
st.subheader(f"Parameters for {selected_kit}")
num_samples = st.number_input("Number of samples", min_value=1, step=1)
excess_pct = st.slider("Excess (%)", min_value=0, max_value=100, value=10)

# Step 3: Calculate reagent amounts
if st.button("Calculate Reagents"):
    st.subheader("Required Reagent Amounts")
    reagents = REAGENT_KITS[selected_kit]
    excess_factor = 1 + (excess_pct / 100)

    for reagent, per_sample_amount in reagents.items():
        total_amount = per_sample_amount * num_samples * excess_factor
        st.write(f"{reagent}: {total_amount:.2f} units")


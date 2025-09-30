import streamlit as st

# Define reagent kits and their per-sample amounts
REAGENT_KITS = {
    "Kit A": {"Reagent 1": 5, "Reagent 2": 3, "Reagent 3": 2},
    "Kit B": {"Reagent X": 2, "Reagent Y": 4, "Reagent Z": 1.5},
    "Kit C": {"Reagent M": 10, "Reagent N": 5},
}

st.title("Reagent Calculator")

# Initialize session state
if "selected_kit" not in st.session_state:
    st.session_state.selected_kit = None

# Step 1: Kit selection buttons
st.write("Choose a reagent kit:")
cols = st.columns(len(REAGENT_KITS))
for i, kit_name in enumerate(REAGENT_KITS.keys()):
    if cols[i].button(kit_name):
        st.session_state.selected_kit = kit_name

# Step 2: If a kit is selected, show inputs and calculate
if st.session_state.selected_kit:
    kit_name = st.session_state.selected_kit
    st.subheader(f"Selected Kit: {kit_name}")

    # Inputs with session_state to preserve values
    if "num_samples" not in st.session_state:
        st.session_state.num_samples = 1
    if "excess_percent" not in st.session_state:
        st.session_state.excess_percent = 10.0

    st.session_state.num_samples = st.number_input(
        "Number of samples",
        min_value=1,
        value=st.session_state.num_samples,
        step=1
    )
    st.session_state.excess_percent = st.number_input(
        "Excess percentage (%)",
        min_value=0.0,
        value=st.session_state.excess_percent,
        step=0.1
    )

    if st.button("Calculate reagents"):
        st.subheader("Reagent amounts (with excess)")
        kit = REAGENT_KITS[kit_name]
        for reagent, amount_per_sample in kit.items():
            total_amount = amount_per_sample * st.session_state.num_samples * (1 + st.session_state.excess_percent / 100)
            st.write(f"{reagent}: {total_amount:.2f} mL")

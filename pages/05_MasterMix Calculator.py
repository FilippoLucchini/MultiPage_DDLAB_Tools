import streamlit as st
import pandas as pd

# Define kits with multiple reactions
REAGENT_KITS = {
    "Twist EF 1.0 Library Prep": {
        "Fragmentation, ER & AT": {"Water": 25, "10X Fragmentation Buffer": 5, "5X Fragmentation Enzyme": 10},
        "Ligation": {"Water": 15, "DNA Ligation Buffer": 20, "DNA Ligation Mix": 10}
    },
    "Kit B": {
        "Prep": {"Reagent X": 8, "Reagent Y": 3},
        "Amplification": {"Reagent Z": 2, "Reagent W": 4}
    }
}

# Handle back button early
if st.session_state.get("back_to_selection"):
    st.session_state.selected_kit = None
    st.session_state.kit_data = None
    st.session_state.back_to_selection = False

# Kit selection view
if "selected_kit" not in st.session_state or st.session_state.selected_kit is None:
    st.title("Select a Reagent Kit")
    for kit_name in REAGENT_KITS.keys():
        if st.button(kit_name):
            st.session_state.selected_kit = kit_name
            st.session_state.kit_data = REAGENT_KITS[kit_name]
else:
    kit_name = st.session_state.selected_kit
    kit_data = st.session_state.kit_data
    st.title(f"Reagent Calculator for {kit_name}")


    # Ask once for samples and excess
    num_samples = st.number_input("Number of samples", min_value=1, step=1)
    excess_pct = st.slider("Excess (%)", min_value=0, max_value=100, value=10)
    excess_factor = 1 + (excess_pct / 100)

    # Calculate button
    if st.button("Calculate Reagents"):
        st.subheader("Calculated Reagent Amounts")
        results = []
        reaction_names = list(kit_data.keys())
        columns = st.columns(len(reaction_names))

        for col, reaction_name in zip(columns, reaction_names):
            reagents = kit_data[reaction_name]
            reaction_results = []

            for reagent, per_sample in reagents.items():
                total = per_sample * num_samples * excess_factor
                reaction_results.append({
                    "Reagent": reagent,
                    "Amount (ul)": round(total, 2)
                })
                results.append({
                    "Reaction": reaction_name,
                    "Reagent": reagent,
                    "Amount (ul)": round(total, 2)
                })

            with col:
                st.markdown(f"**{reaction_name}**")
                st.table(pd.DataFrame(reaction_results))

        # Export CSV
        df = pd.DataFrame(results)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download All Reagents as CSV", data=csv, file_name=f"{kit_name}_reagents.csv", mime="text/csv")

    # Back button
    if st.button("🔙 Back to Kit Selection"):
        st.session_state.back_to_selection = True
        st.rerun()

        st.session_state.kit_data = None


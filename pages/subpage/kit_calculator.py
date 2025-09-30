import streamlit as st
import pandas as pd

if "selected_kit" not in st.session_state:
    st.warning("Please select a kit first.")
    st.stop()

kit_name = st.session_state.selected_kit
kit_data = st.session_state.kit_data

st.title(f"Reagent Calculator for {kit_name}")

results = []

for reaction_name, reagents in kit_data.items():
    st.subheader(f"{reaction_name}")
    samples = st.number_input(f"Samples for {reaction_name}", min_value=1, step=1, key=f"samples_{reaction_name}")
    excess = st.slider(f"Excess (%) for {reaction_name}", min_value=0, max_value=100, value=10, key=f"excess_{reaction_name}")
    factor = 1 + (excess / 100)

    for reagent, per_sample in reagents.items():
        total = per_sample * samples * factor
        st.write(f"{reagent}: {total:.2f} units")
        results.append({
            "Reaction": reaction_name,
            "Reagent": reagent,
            "Amount": round(total, 2)
        })

# Export all results
df = pd.DataFrame(results)
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download All Reagents as CSV", data=csv, file_name=f"{kit_name}_reagents.csv", mime="text/csv")

# Back button
if st.button("🔙 Back to Kit Selection"):
    st.switch_page("pages/kit_selector.py")

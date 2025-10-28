import streamlit as st
import pandas as pd
import io

st.title("🧮 DDLAB Calculators")
st.caption("Quick tools for common lab calculations — dilution, buffer scaling, and nucleic acid conversions.")

# Tabs for each tool
tab1, tab2, tab3, tab4 = st.tabs([
    "🔹 Dilution Calculator",
    "🧴 Buffer/Media Scaler",
    "🥣 Master Mix Calculator",
    "🧬 DNA/RNA Converter"
])

# --------------------------------------------------------------------
# 🔹 1. DILUTION CALCULATOR
# --------------------------------------------------------------------
with tab1:
    st.subheader("Dilution Calculator (C₁V₁ = C₂V₂)")
    st.markdown("Compute how to dilute a stock solution to a desired concentration.")

    col1, col2 = st.columns(2)
    with col1:
        C1 = st.number_input("Stock concentration (C₁)", value=10.0)
        C1_unit = st.selectbox("C₁ Unit", ["M", "mM", "µM", "ng/µL"], key="C1_unit")
        C2 = st.number_input("Desired concentration (C₂)", value=1.0)
        C2_unit = st.selectbox("C₂ Unit", ["M", "mM", "µM", "ng/µL"], key="C2_unit")
    with col2:
        V2 = st.number_input("Final total volume (µL)", value=1000.0)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Calculate Dilution"):
            try:
                V1 = (C2 / C1) * V2
                st.success(f"🧪 Take **{V1:.2f} µL** of stock and add **{V2 - V1:.2f} µL** of diluent.")
            except ZeroDivisionError:
                st.error("Stock concentration (C₁) must be greater than zero.")

    st.info("💡 Tip: You can extend this tool for serial dilutions or unit conversions later.")

# --------------------------------------------------------------------
# 🧴 2. BUFFER / MEDIA SCALER
# --------------------------------------------------------------------
with tab2:
    st.subheader("Buffer / Media Recipe Scaler")
    st.markdown("Scale recipes to prepare any desired volume, keeping ratios constant.")

    target_volume = st.number_input("Desired final volume (mL)", value=1000.0, min_value=1.0)
    base_volume = st.number_input("Original recipe volume (mL)", value=100.0, min_value=0.1)
    n = st.number_input("Number of components", min_value=1, value=3, step=1)

    st.divider()
    st.markdown("### Recipe Components")
    components = []

    for i in range(int(n)):
        c1, c2, c3 = st.columns([3, 2, 2])
        name = c1.text_input(f"Component {i+1} name", key=f"name_{i}")
        amount = c2.number_input(f"Amount", key=f"amt_{i}", value=1.0)
        unit = c3.selectbox("Unit", ["mL", "µL", "g", "mg"], key=f"unit_{i}")
        components.append((name, amount, unit))

    if st.button("Scale Recipe"):
        st.markdown("### 🧾 Scaled Recipe")
        for c in components:
            name, amount, unit = c
            if name:
                scaled_amt = amount * (target_volume / base_volume)
                st.write(f"• **{name}** → {scaled_amt:.2f} {unit}")
        st.success(f"✅ Scaled from {base_volume} mL → {target_volume} mL total.")

    st.info("💡 You can later connect this to your reagent database or export as CSV.")
# --------------------------------------------------------------------
# 🧴 3. MasterMix Claculator
# --------------------------------------------------------------------

with tab3:
    st.subheader("MasterMix Calculator")
    st.markdown("Choose the kit and calculate master mixes for your library prep.")

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
            st.download_button(
                "Download All Reagents as CSV",
                data=csv,
                file_name=f"{kit_name}_reagents.csv",
                mime="text/csv"
            )

    # Back button
        if st.button("🔙 Back to Kit Selection"):
            st.session_state.back_to_selection = True
            st.rerun()

# --------------------------------------------------------------------
# 🧬 4. DNA / RNA CONCENTRATION CONVERTER
# --------------------------------------------------------------------
with tab4:
    st.subheader("DNA/RNA Concentration Converter")
    st.markdown("Convert nucleic acid concentrations between ng/µL and nM based on molecule type and fragment length.")

    molecule = st.selectbox("Molecule type", ["dsDNA", "ssDNA", "RNA"])
    conversion = st.radio("Conversion direction", ["ng/µL → nM", "nM → ng/µL"])
    length = st.number_input("Fragment length (bp or nt)", value=1000.0, min_value=1.0)

    factor = 660 if molecule == "dsDNA" else 340  # dsDNA vs ssDNA/RNA

    if conversion == "ng/µL → nM":
        conc_ng = st.number_input("Concentration (ng/µL)", value=10.0)
        conc_nM = (conc_ng * 1e6) / (factor * length)
        st.success(f"📈 {conc_ng} ng/µL = **{conc_nM:.2f} nM**")
    else:
        conc_nM = st.number_input("Concentration (nM)", value=10.0)
        conc_ng = (conc_nM * factor * length) / 1e6
        st.success(f"📉 {conc_nM} nM = **{conc_ng:.2f} ng/µL**")

    st.caption("Assumptions: dsDNA MW ≈ 660 g/mol per bp, RNA ≈ 340 g/mol per nt.")

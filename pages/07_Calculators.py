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
    st.header("🥣 Master Mix Calculator")
    st.caption("Easily calculate and scale reagent mixes for multiple reactions or library prep kits.")

    # --- Example Kits ---
    REAGENT_KITS = {
        "Twist EF 1.0 Library Prep": {
            "Fragmentation, ER & AT": {"Water": 25, "10X Fragmentation Buffer": 5, "5X Fragmentation Enzyme": 10},
            "Ligation": {"Water": 15, "DNA Ligation Buffer": 20, "DNA Ligation Mix": 10}
        },
        "PCR Setup": {
            "Reaction Mix": {"Water": 14, "10X Buffer": 2, "dNTPs": 1, "Taq Polymerase": 0.5, "Primer Mix": 2.5}
        }
    }

    # --- Navigation State ---
    if "selected_kit" not in st.session_state:
        st.session_state.selected_kit = None

    # --- Kit Selection ---
    if st.session_state.selected_kit is None:
        st.subheader("Select a Reagent Kit")
        st.markdown("Choose from preset kits or create a custom one.")

        cols = st.columns(3)
        for i, kit_name in enumerate(REAGENT_KITS.keys()):
            with cols[i % 3]:
                if st.button(f"⚗️ {kit_name}"):
                    st.session_state.selected_kit = kit_name

        st.divider()
        with st.expander("➕ Create Custom Kit"):
            kit_name = st.text_input("Kit Name")
            n_reactions = st.number_input("Number of reactions", min_value=1, value=1, step=1)
            custom_kit = {}
            for i in range(int(n_reactions)):
                rxn_name = st.text_input(f"Reaction {i+1} name", key=f"rxn_{i}")
                n_reagents = st.number_input(f"Number of reagents in {rxn_name}", min_value=1, value=3, key=f"reag_{i}")
                reagents = {}
                for j in range(int(n_reagents)):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        rname = st.text_input(f"Reagent {j+1} name ({rxn_name})", key=f"rname_{i}_{j}")
                    with col2:
                        ramt = st.number_input("µL per sample", value=1.0, key=f"ramt_{i}_{j}")
                    if rname:
                        reagents[rname] = ramt
                if rxn_name:
                    custom_kit[rxn_name] = reagents

            if st.button("💾 Save Custom Kit") and kit_name:
                REAGENT_KITS[kit_name] = custom_kit
                st.session_state.selected_kit = kit_name
                st.success(f"✅ Custom kit '{kit_name}' added and selected!")

    # --- Kit View ---
    else:
        kit_name = st.session_state.selected_kit
        kit_data = REAGENT_KITS[kit_name]

        st.markdown(f"### 🧪 {kit_name}")
        st.caption("Enter the number of samples and extra volume percentage.")

        col1, col2 = st.columns(2)
        num_samples = col1.number_input("Number of samples", min_value=1, value=8)
        excess_pct = col2.slider("Excess (%)", min_value=0, max_value=100, value=10)
        excess_factor = 1 + (excess_pct / 100)

        if st.button("🔢 Calculate Master Mix"):
            st.divider()
            st.subheader("📋 Calculated Reagent Amounts")

            results = []
            for rxn_name, reagents in kit_data.items():
                with st.expander(f"🧫 {rxn_name}", expanded=True):
                    data = []
                    for reagent, per_sample in reagents.items():
                        total = per_sample * num_samples * excess_factor
                        tip = "⚠️ Add water to bring to volume" if total < 2 else ""
                        data.append({"Reagent": reagent, "Per Sample (µL)": per_sample, "Total (µL)": round(total, 2), "Note": tip})
                        results.append({
                            "Reaction": rxn_name,
                            "Reagent": reagent,
                            "Amount (µL)": round(total, 2)
                        })
                    st.table(pd.DataFrame(data))

            # Summary CSV
            df = pd.DataFrame(results)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="💾 Download All as CSV",
                data=csv,
                file_name=f"{kit_name.replace(' ', '_')}_MasterMix_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

        st.divider()
        if st.button("🔙 Back to Kit Selection"):
            st.session_state.selected_kit = None
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

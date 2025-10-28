# 📘 lab_calculators.py

import streamlit as st

st.title("🧮 DDLAB Calculators")
st.caption("Quick tools for common lab calculations — dilution, buffer scaling, and nucleic acid conversions.")

# Tabs for each tool
tab1, tab2, tab3 = st.tabs([
    "🔹 Dilution Calculator",
    "🧴 Buffer/Media Scaler",
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
# 🧬 3. DNA / RNA CONCENTRATION CONVERTER
# --------------------------------------------------------------------
with tab3:
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

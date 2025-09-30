import streamlit as st
import pandas as pd

# --- Configuration: Reagent Kit Specifications ---
# Volumes are defined in microliters (µL) per single sample
REAGENT_KITS = {
    "Kit A (DNA Library Prep)": {
        "Lysis Buffer": 100,
        "Binding Solution": 50,
        "Wash Buffer": 150,
        "Elution Buffer": 20,
    },
    "Kit B (RNA Sequencing)": {
        "Reverse Transcriptase": 5,
        "Primer Mix": 10,
        "PCR Mastermix": 75,
    },
    "Kit C (Custom Assay)": {
        "Detection Reagent R1": 15,
        "Diluent D2": 60,
    }
}

# Set up the initial state if not present
if 'kit_selected' not in st.session_state:
    st.session_state.kit_selected = None
if 'samples' not in st.session_state:
    st.session_state.samples = 1
if 'excess_percent' not in st.session_state:
    st.session_state.excess_percent = 10

def select_kit(kit_name):
    """Callback function to set the selected kit and reset results."""
    st.session_state.kit_selected = kit_name
    st.session_state.show_results = False # Ensure results are hidden initially
    st.session_state.samples = 1
    st.session_state.excess_percent = 10

def calculate_reagents(samples, excess_percent):
    """Performs the calculation and sets state to show results."""
    st.session_state.samples = samples
    st.session_state.excess_percent = excess_percent
    st.session_state.show_results = True

def reset_selection():
    """Resets the state back to kit selection."""
    st.session_state.kit_selected = None
    st.session_state.show_results = False


# --- Stage 1: Kit Selection ---
def display_kit_selection():
    """Displays the buttons for selecting a reagent kit."""
    st.header("1. Choose a Reagent Kit")
    st.markdown("Select the kit protocol you wish to calculate reagents for.")

    # Create two columns for the buttons for a cleaner layout
    cols = st.columns(len(REAGENT_KITS))

    for i, kit_name in enumerate(REAGENT_KITS.keys()):
        with cols[i]:
            st.button(
                kit_name,
                on_click=select_kit,
                args=(kit_name,),
                use_container_width=True,
                type="primary"
            )

    st.divider()
    st.info("After selection, you will proceed to enter sample details.")


# --- Stage 2 & 3: Input Form and Results ---
def display_input_and_results():
    """Displays the input form, performs calculations, and shows results."""
    kit_name = st.session_state.kit_selected
    st.header(f"2. Configure Calculation for: {kit_name}")

    # Use a form to group inputs and calculation button
    with st.form("reagent_form"):
        st.subheader("Input Parameters")
        
        # Input for Number of Samples
        samples_input = st.number_input(
            "Number of Samples (N)",
            min_value=1,
            value=st.session_state.samples,
            step=1,
            format="%d",
            key="samples_input",
            help="The total number of biological samples to be processed."
        )

        # Input for Excess Percentage
        excess_input = st.number_input(
            "Excess Volume (%)",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.excess_percent,
            step=0.5,
            key="excess_input",
            help="Percentage of extra reagent volume to include to account for pipetting errors, dead volume, etc."
        )

        # Calculation button
        submitted = st.form_submit_button("Calculate Reagents", type="primary")

    if submitted or st.session_state.get('show_results', False):
        st.subheader("3. Calculated Reagent Requirements")

        reagents_specs = REAGENT_KITS[kit_name]
        
        # Calculation logic
        data = []
        
        # Factor to apply excess: e.g., 10% excess means factor is 1.10
        excess_factor = 1 + (excess_input / 100)
        
        for reagent, vol_per_sample in reagents_specs.items():
            # Total volume required for N samples (without excess)
            total_vol_raw = samples_input * vol_per_sample
            
            # Total volume required with excess
            total_vol_excess = total_vol_raw * excess_factor
            
            data.append({
                "Reagent Name": reagent,
                "Volume per Sample (µL)": vol_per_sample,
                f"Total Volume Required (µL) (N={samples_input})": total_vol_raw,
                f"Total Volume Required (µL) (Excess={excess_input}%)": total_vol_excess,
                "Total Volume Required (mL)": total_vol_excess / 1000
            })

        df = pd.DataFrame(data)
        
        st.metric(
            label="Total Samples to Process",
            value=f"{samples_input} samples",
            delta=f"{excess_input}% Excess Included"
        )
        
        # Display results table
        st.dataframe(
            df.set_index("Reagent Name"),
            use_container_width=True,
            hide_index=False
        )
        
        st.caption("All calculations include the specified excess volume. Volumes are rounded to two decimal places.")
        
    st.divider()
    # Button to go back to kit selection
    st.button(
        "← Back to Kit Selection",
        on_click=reset_selection,
        type="secondary"
    )

# --- Main Logic Flow ---
st.title("🔬 Reagent Volume Calculator")
st.markdown("Easily calculate the required volumes for molecular biology kits based on sample number and excess percentage.")

if st.session_state.kit_selected is None:
    display_kit_selection()
else:
    display_input_and_results()

import streamlit as st

st.set_page_config(layout="wide")

st.title("Welcome to DDLAB Database Management Tools 👋")

# --- Inject Custom CSS for Bigger Buttons AND Container Border ---
st.markdown(
    """
    <style>
    /* 1. Styling for the buttons */
    div.stButton > button {
        font-size: 18px;
        padding: 10px 20px;
        height: auto;
        width: 100%;
    }

    /* 2. Styling for the container border */
    .database-group {
        border: 2px solid #4CAF50; /* A nice green border */
        border-radius: 10px; /* Optional: adds rounded corners */
        padding: 20px; /* Space inside the border */
        margin-top: 20px; /* Space above the box */
    }
    /* 3. Ensure Streamlit elements inside the box are properly styled */
    .database-group h2, .database-group p {
        padding-left: 0;
        padding-right: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Create a Container for the Databases Group ---
# This ensures that all components rendered within the 'with' block are visually grouped.
with st.container(border=true):
    
    # Start the custom HTML div (the box)
    st.markdown('<div class="database-group">', unsafe_allow_html=True)
    
    # --- Databases Section Content (Header and Description) ---
    # These must be inside the markdown div wrapper to be included in the border.
    st.header("Databases")
    st.write("Choose a database to manage:")

    # --- Use columns to place buttons side-by-side ---
    # Streamlit components must be used directly, but they are placed inside 
    # the container, which is itself wrapped in the custom div.
    col1, col2, col3 = st.columns(3)

    # --- Freezer ---
    with col1:
        if st.button("🧊 Freezer Database"):
            st.switch_page("pages/Freezer_Database.py")

    # --- Reagents ---
    with col2:
        if st.button("⚗️ Reagents Database"):
            st.switch_page("pages/Reagents_Database.py")

    # --- Plastics ---
    with col3:
        if st.button("🧪 Plastics Database"):
            st.switch_page("pages/Plastics_Database.py")

    # Close the custom div tag
    st.markdown('</div>', unsafe_allow_html=True)


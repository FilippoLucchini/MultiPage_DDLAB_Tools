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
    </style>
    """,
    unsafe_allow_html=True
)

# --- Create a Container for the Databases Group ---
# We use an empty container, then replace its contents with the HTML/CSS wrapper.
database_container = st.container()

with database_container:
    # Use st.markdown to wrap the content in a div with the custom class
    st.markdown('<div class="database-group">', unsafe_allow_html=True)
    
    # --- Databases Section Content ---
    st.header("Databases")
    st.write("Choose a database to manage:")

    # --- Use columns to place buttons side-by-side ---
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

# The content below the container will appear outside the box.

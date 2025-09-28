import streamlit as st

st.set_page_config(layout="wide")

st.title("Welcome to DDLAB Database Management Tools 👋")

# --- Use st.container() to define the group area ---
# The border CSS will be applied to the div associated with this container.
with st.container(border=True) as database_group:
    
    # Inject Custom CSS for Bigger Buttons AND Targeting the Container
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

        /* 2. Targeting the container itself to ensure the border is visible */
        /*
        Streamlit containers are wrapped in a div with role="region". 
        The border=True parameter on st.container() now reliably adds a border,
        but for further custom styling (like color/thickness), we can target 
        a known ancestor, though for simple borders, st.container(border=True) is best.
        */

        </style>
        """,
        unsafe_allow_html=True
    )
    
    # --- Databases Section Content ---
    # Everything here is now guaranteed to be inside the container.
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

# The content below this block will appear outside the box.

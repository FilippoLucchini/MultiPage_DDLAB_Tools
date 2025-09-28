import streamlit as st

st.set_page_config(layout="wide")

st.title("Welcome to DDLAB Database Management Tools 👋")

# --- Databases Section Header ---
st.header("Databases")

st.write("Choose a database to manage:")

# --- Inject custom CSS for bigger buttons ---
st.markdown(
    """
    <style>
    /* Target all Streamlit buttons */
    div.stButton > button {
        font-size: 18px; /* Increase font size */
        padding: 10px 20px; /* Increase padding for a bigger clickable area */
        height: auto; /* Allow height to adjust based on padding */
        width: 100%; /* Make buttons fill their column */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Use columns to place buttons side-by-side ---
# Create three columns of equal width
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


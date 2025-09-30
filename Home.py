import streamlit as st

st.set_page_config(
    page_title="DDLAB Tools",
    page_icon="🧬",   # emoji or path to .png/.ico
    layout="wide"     # "centered" or "wide"
)

st.title("Welcome to DDLAB Tools 👋")
st.markdown("Your hub for managing lab databases and analysis tools.")


# --- Databases Section Header ---
st.header("Databases")
st.write("Choose a database to manage:")

# --- Inject custom CSS for bigger buttons ---
st.markdown(
    """
    <style>
    div.stButton > button {
        font-size: 18px;
        padding: 10px 20px;
        height: auto;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Database buttons ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧊 Freezer Database"):
        st.switch_page("pages/01_Freezer_Database.py")

with col2:
    if st.button("⚗️ Reagents Database"):
        st.switch_page("pages/02_Reagents_Database.py")

with col3:
    if st.button("🧪 Plastics Database"):
        st.switch_page("pages/03_Plastics_Database.py")

# --- New Section Below ---
st.header("Analysis Tools")
st.write("Choose an analysis tool to run:")

col4, col5 = st.columns(2)

with col4:
    if st.button("🔎 Index7 Matching Tool"):
        st.switch_page("pages/04_Index7_Matching.py")

with col5:
    if st.button("📊 Another Tool (future)"):
        st.switch_page("pages/Other_Tool.py")












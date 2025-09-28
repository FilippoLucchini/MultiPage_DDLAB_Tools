import streamlit as st

st.set_page_config(layout="centered")

st.title("Welcome to DDLAB Tools 👋")

st.write("Choose a database to manage:")

# --- Freezer ---
if st.button("🧊 Freezer Database"):
    st.switch_page("pages/Freezer_Database.py")

# --- Reagents ---
if st.button("⚗️ Reagents Database"):
    st.switch_page("pages/Reagents_Database.py")

# --- Plastics ---
if st.button("🧪 Plastics Database"):
    st.switch_page("pages/Plastics_Database.py")

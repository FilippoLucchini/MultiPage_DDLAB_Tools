import streamlit as st

st.set_page_config(layout="centered")

st.title("Welcome to DDLAB Tools 👋")

st.write("Click below to access the Freezer Database:")

if st.button("❄️ Freezer Database"):
    st.switch_page("pages/Freezer_Database.py")  # Jump to database page



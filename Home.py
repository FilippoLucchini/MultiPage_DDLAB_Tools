import streamlit as st
import datetime

st.set_page_config(page_title="DDLAB Tools", page_icon="🧬", layout="wide")

# --- Hero Section ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("Images/Lab_Cartoon.png", width=240)  # replace with your logo path
with col_title:
    st.markdown(
        """
        <h1 style="margin-bottom:0;">Welcome to <span style="color:#2E86C1;">DDLAB Tools</span> 👋</h1>
        <p style="font-size:20px; color:gray; margin-top:0;">
        Manage databases and useful tools in one place.
        </p>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")  # horizontal divider

# --- Inject custom CSS for dark-theme cards ---
st.markdown(
    """
    <style>
    .card {
        background-color: #1e1e1e;  /* dark card */
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.6);
        transition: transform 0.2s ease-in-out, background-color 0.2s;
        cursor: pointer;
        border: 1px solid #333;
        margin-bottom: 20px;
    }
    .card:hover {
        transform: scale(1.02);
        background-color: #2a2a2a;  /* slightly lighter on hover */
        box-shadow: 0px 6px 16px rgba(0, 150, 255, 0.4);
    }
    .card h3 {
        margin: 10px 0 5px 0;
        font-size: 22px;
        color: #00c3ff;  /* bright cyan for titles */
    }
    .card p {
        color: #ccc;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- Databases Section ---
st.header("🗄️ Databases")
st.write("Choose a database to manage:")

db_col1, db_col2, db_col3 = st.columns(3)

with db_col1:
    if st.button("🧊 Freezer Database", use_container_width=True):
        st.switch_page("pages/01_Freezer_Database.py")
    st.markdown('<div class="card"><h3>🧊 Freezer</h3><p>Organize freezer samples and locations.</p></div>', unsafe_allow_html=True)

with db_col2:
    if st.button("⚗️ Reagents Database", use_container_width=True):
        st.switch_page("pages/02_Reagents_Database.py")
    st.markdown('<div class="card"><h3>⚗️ Reagents</h3><p>Track chemicals and consumables.</p></div>', unsafe_allow_html=True)

with db_col3:
    if st.button("🧪 Plastics Database", use_container_width=True):
        st.switch_page("pages/03_Plastics_Database.py")
    st.markdown('<div class="card"><h3>🧪 Plastics</h3><p>Manage lab plastics and inventory.</p></div>', unsafe_allow_html=True)

db_col1, db_col2, db_col3 = st.columns(3) 

with db_col1:
    if st.button("🧬 NovaseqX Runs Hystory", use_container_width=True):
        st.switch_page("pages/06_NovaseqX_Recap.py")
    st.markdown('<div class="card"><h3>🧬 NovaseqX Runs Hystory</h3><p>See runs with library types and production.</p></div>', unsafe_allow_html=True)

with db_col2:
    if st.button("More to Come", use_container_width=True):
        st.switch_page("pages")
    st.markdown('<div class="card"><h3>Future features to come</h3><p>Lets see what the future brings us!.</p></div>', unsafe_allow_html=True)

with db_col3:
    if st.button("Additional Features", use_container_width=True):
        st.switch_page("pages")
    st.markdown('<div class="card"><h3>Future Release</h3><p>Updates.</p></div>', unsafe_allow_html=True)

st.markdown("---")

# --- Analysis Tools Section ---
st.header("🛠️ Tools")
st.write("Choose a tool to run:")

tools_col1, tools_col2 = st.columns(2) 

with tools_col1:
    if st.button("🔎 Index Matching Tool", use_container_width=True):
        st.switch_page("pages/04_Index_Matching.py")
    st.markdown('<div class="card"><h3>🔎 Index Matching</h3><p>Check sequencing index overlaps.</p></div>', unsafe_allow_html=True)

with tools_col2:
    if st.button("🥣 Master Mix Calculator", use_container_width=True):
        st.switch_page("pages/05_MasterMix Calculator.py")
    st.markdown('<div class="card"><h3>🥣 Master Mix</h3><p>Calculate reagents mixes.</p></div>', unsafe_allow_html=True)

st.markdown("---")  # horizontal divider












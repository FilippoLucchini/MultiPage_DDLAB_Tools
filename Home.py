import streamlit as st

st.set_page_config(page_title="DDLAB Tools", page_icon="🧬", layout="wide")

# --- CSS for dark-theme cards ---
st.markdown(
    """
    <style>
    .card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.6);
        transition: transform 0.2s ease-in-out, background-color 0.2s;
        cursor: pointer;
        border: 1px solid #333;
        text-decoration: none;
        display: block;
    }
    .card:hover {
        transform: scale(1.02);
        background-color: #2a2a2a;
        box-shadow: 0px 6px 16px rgba(0, 150, 255, 0.4);
    }
    .card h3 {
        margin: 10px 0 5px 0;
        font-size: 22px;
        color: #00c3ff;
    }
    .card p {
        color: #ccc;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Hero Section ---
st.title("Welcome to DDLAB Database Management Tools 👋")
st.markdown("---")

# --- Databases Section ---
st.header("🗄️ Databases")

db_col1, db_col2, db_col3 = st.columns(3)

with db_col1:
    st.markdown(
        f"""
        <a href="/pages/01_Freezer_Database" target="_self" class="card">
            <h3>🧊 Freezer</h3>
            <p>Organize freezer samples and locations.</p>
        </a>
        """,
        unsafe_allow_html=True,
    )

with db_col2:
    st.markdown(
        f"""
        <a href="/pages/02_Reagents_Database" target="_self" class="card">
            <h3>⚗️ Reagents</h3>
            <p>Track chemicals and consumables.</p>
        </a>
        """,
        unsafe_allow_html=True,
    )

with db_col3:
    st.markdown(
        f"""
        <a href="/pages/03_Plastics_Database" target="_self" class="card">
            <h3>🧪 Plastics</h3>
            <p>Manage lab plastics and inventory.</p>
        </a>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# --- Analysis Section ---
st.header("🧬 Analysis Tools")

tools

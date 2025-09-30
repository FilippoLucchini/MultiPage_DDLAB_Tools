import streamlit as st

st.set_page_config(page_title="DDLAB Tools", page_icon="🧬", layout="wide")

# --- Hero Section ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("Sticker_DDLAB-removebg-preview.png", width=240)  # replace with your logo path
with col_title:
    st.markdown(
        """
        <h1 style="margin-bottom:0;">Welcome to <span style="color:#2E86C1;">DDLAB Tools</span> 👋</h1>
        <p style="font-size:20px; color:gray; margin-top:0;">
        Manage databases and run sequencing analysis in one place.
        </p>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")  # horizontal divider

# --- Inject custom CSS for card-style buttons ---
st.markdown(
    """
    <style>
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease-in-out;
        cursor: pointer;
    }
    .card:hover {
        transform: scale(1.02);
        background-color: #eef6fb;
    }
    .card h3 {
        margin: 10px 0 5px 0;
        font-size: 22px;
    }
    .card p {
        color: #666;
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

st.markdown("---")

# --- Analysis Tools Section ---
st.header("🧬 Analysis Tools")
st.write("Choose an analysis tool to run:")

tools_col1, tools_col2 = st.columns(2)

with tools_col1:
    if st.button("🔎 Index7 Matching Tool", use_container_width=True):
        st.switch_page("pages/04_Index7_Matching.py")
    st.markdown('<div class="card"><h3>🔎 Index7 Matching</h3><p>Check sequencing index overlaps.</p></div>', unsafe_allow_html=True)

with tools_col2:
    if st.button("📊 Another Tool (future)", use_container_width=True):
        st.switch_page("pages/Other_Tool.py")
    st.markdown('<div class="card"><h3>📊 Future Tool</h3><p>Reserved for upcoming analysis features.</p></div>', unsafe_allow_html=True)








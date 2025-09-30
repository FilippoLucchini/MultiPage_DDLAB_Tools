import streamlit as st

st.set_page_config(page_title="DDLAB Tools", page_icon="🧬", layout="wide")

# --- Hero Section ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("Images/Lab_Cartoon.png", width=120)  # replace with your logo path
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

st.markdown("---")

# --- Inject custom CSS to make buttons look like cards with subtitle ---
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #1e1e1e;  /* dark card style */
        color: #ccc;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 20px;
        border: 1px solid #333;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.6);
        transition: transform 0.2s ease-in-out, background-color 0.2s;
        width: 100%;
        height: auto;
        white-space: normal;  /* allow text to wrap */
        line-height: 1.4;     /* spacing for multi-line */
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        background-color: #2a2a2a;
        box-shadow: 0px 6px 16px rgba(0, 150, 255, 0.4);
        color: #fff;
    }
    div.stButton > button span {
        display: block;
        font-size: 16px;      /* subtitle font size */
        color: #aaa;          /* subtitle color */
        margin-top: 5px;
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
    if st.button("🧊 Freezer Database\nOrganize freezer samples and locations", use_container_width=True):
        st.switch_page("pages/01_Freezer_Database.py")

with db_col2:
    if st.button("⚗️ Reagents Database\nTrack chemicals and consumables", use_container_width=True):
        st.switch_page("pages/02_Reagents_Database.py")

with db_col3:
    if st.button("🧪 Plastics Database\nManage lab plastics and inventory", use_container_width=True):
        st.switch_page("pages/03_Plastics_Database.py")

st.markdown("---")

# --- Analysis Tools Section ---
st.header("🧬 Analysis Tools")
st.write("Choose an analysis tool to run:")

tools_col1, tools_col2 = st.columns(2)

with tools_col1:
    if st.button("🔎 Index7 Matching Tool\nCheck sequencing index overlaps", use_container_width=True):
        st.switch_page("pages/04_Index7_Matching.py")

with tools_col2:
    if st.button("📊 Another Tool (future)\nReserved for upcoming analysis features", use_container_width=True):
        st.switch_page("pages/Other_Tool.py")


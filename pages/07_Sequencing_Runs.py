import streamlit as st
import datetime
import plotly.express as px
import db

db.init_db()
year = datetime.datetime.now().year

st.title("Sequencing Runs Overview")

# --- Add new run ---
with st.form("add_run"):
    st.subheader("Add a new sequencing run")
    platform = st.selectbox("Platform", ["Illumina Novaseq X", "Illumina Novaseq 6000", "Illumina NextSeq2000", "ONT PromethION", "ONT MinION", "GeneMind", "Salus EVO", "Element Aviti", "MGI"])
    run_date = st.date_input("Date", datetime.date.today())
    submitted = st.form_submit_button("Add Run")

    if submitted:
        db.add_run(platform, run_date)
        st.success(f"Added run on {platform} ({run_date})")
        st.experimental_rerun()

# --- Show chart ---
runs_this_year = db.get_runs(year)

if runs_this_year:
    counts = {}
    for r in runs_this_year:
        counts[r["platform"]] = counts.get(r["platform"], 0) + 1

    fig = px.bar(
        x=list(counts.keys()), 
        y=list(counts.values()), 
        labels={"x": "Platform", "y": "Number of Runs"},
        title=f"Sequencing Runs by Platform in {year}"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info(f"No sequencing runs recorded yet for {year}.")

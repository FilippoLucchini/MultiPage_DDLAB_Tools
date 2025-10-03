import streamlit as st
import datetime
import plotly.express as px
import db

db.init_db()
year = datetime.datetime.now().year

st.title("Samples Overview")

# --- Add new sample ---
with st.form("add_sample"):
    st.subheader("Add a new sample")
    sample_type = st.selectbox("Sample type", ["WES", "WGS", "RNA-seq", "Other"])
    sample_date = st.date_input("Date", datetime.date.today())
    submitted = st.form_submit_button("Add Sample")

    if submitted:
        db.add_sample(sample_type, sample_date)
        st.success(f"Added {sample_type} sample on {sample_date}")
        st.experimental_rerun()

# --- Show chart ---
samples_this_year = db.get_samples(year)

if samples_this_year:
    counts = {}
    for s in samples_this_year:
        counts[s["type"]] = counts.get(s["type"], 0) + 1

    fig = px.bar(
        x=list(counts.keys()), 
        y=list(counts.values()), 
        labels={"x": "Sample Type", "y": "Count"},
        title=f"Samples by Type in {year}"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info(f"No samples recorded yet for {year}.")

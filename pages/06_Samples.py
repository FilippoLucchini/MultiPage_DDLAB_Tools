import streamlit as st
import datetime
import plotly.express as px
import pandas as pd
import db  # your existing db.py

db.init_db()
year = datetime.datetime.now().year

st.title("Samples Overview")

# --- Add new sample(s) ---
with st.form("add_sample"):
    st.subheader("Add new samples")
    sample_type = st.selectbox("Sample type", ["WES", "WGS", "RNA-seq", "Other"])
    sample_date = st.date_input("Date", datetime.date.today())
    sample_count = st.number_input("Number of samples", min_value=1, value=1, step=1)
    submitted = st.form_submit_button("Add Sample(s)")

    if submitted:
        for _ in range(sample_count):
            db.add_sample(sample_type, sample_date)
        st.success(f"Added {sample_count} sample(s) of type {sample_type} on {sample_date}")
        st.experimental_rerun()

# --- Show chart ---
samples_this_year = db.get_samples(year)

if samples_this_year:
    # Aggregate counts by type
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

    # Optional: show detailed table
    st.subheader("Detailed Samples")
    df = pd.DataFrame(samples_this_year)
    st.dataframe(df)
else:
    st.info(f"No samples recorded yet for {year}.")

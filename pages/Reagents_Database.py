import streamlit as st
import pandas as pd
import os

# Set app layout on wide
st.set_page_config(layout="wide")

st.title("⚗️ Reagents Database")

file_path = "Reagents_Database.xlsx"
COLUMNS = ["Reagent Name", "Lot Number", "Expiry Date", "Supplier", "Storage Location"]

if os.path.exists(file_path):
    df = pd.read_excel(file_path)
else:
    df = pd.DataFrame(columns=COLUMNS)
    df.to_excel(file_path, index=False)

# --- Search ---
st.header("🔍 Search Reagents")
with st.form("search_form"):
    field = st.selectbox("Choose field to search by:", COLUMNS, key="search_field")
    values = sorted(df[field].dropna().unique()) if not df.empty else []
    value = st.selectbox("Start typing to search:", values, key="search_value")
    submitted = st.form_submit_button("Search")
    if submitted:
        st.dataframe(df[df[field] == value])

# --- Add ---
st.header("➕ Add New Reagent")
with st.form("add_form"):
    new_data = {col: st.text_input(col) for col in COLUMNS}
    add_submit = st.form_submit_button("Add Reagent")
    if add_submit:
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_excel(file_path, index=False)
        st.success("✅ Reagent added!")
        st.rerun()

# --- Delete ---
st.header("❌ Delete Reagent")
with st.form("delete_form"):
    del_field = st.selectbox("Choose field:", COLUMNS, key="del_field")
    del_values = sorted(df[del_field].dropna().unique()) if not df.empty else []
    del_value = st.selectbox("Select value to delete:", del_values, key="del_value")
    del_submit = st.form_submit_button("Delete")
    if del_submit:
        df = df[df[del_field] != del_value]
        df.to_excel(file_path, index=False)
        st.success(f"✅ Deleted entries where {del_field} = {del_value}")
        st.rerun()

# --- Edit ---
st.header("✏️ Edit Reagent")
with st.form("edit_form"):
    edit_field = st.selectbox("Choose field:", COLUMNS, key="edit_field")
    edit_values = sorted(df[edit_field].dropna().unique()) if not df.empty else []
    edit_value = st.selectbox("Select value to edit:", edit_values, key="edit_value")
    new_values = {col: st.text_input(f"New {col}", value=df.loc[df[edit_field]==edit_value, col].iloc[0] if not df[df[edit_field]==edit_value].empty else "") for col in COLUMNS}
    edit_submit = st.form_submit_button("Update")
    if edit_submit:
        df.loc[df[edit_field]==edit_value, COLUMNS] = list(new_values.values())
        df.to_excel(file_path, index=False)
        st.success("✅ Reagent updated!")
        st.rerun()

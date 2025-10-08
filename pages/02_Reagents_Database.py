import streamlit as st
import pandas as pd
import os

# Set app layout on wide
st.set_page_config(layout="wide")

# File path
file_path = "Reagents_Database.xlsx"

# --- CACHE FUNCTION FOR DATA LOADING ---
@st.cache_data(show_spinner="Loading database...")
def load_data(path):
    if os.path.exists(path):
        return pd.read_excel(path, sheet_name="Template")
    else:
        # Create an empty DataFrame if the file doesn't exist
        columns = [
            "Reagent Type", "Supplier", "Reagent Name", "Lot Number", "Expiry Date",
            "Total Reactions", "Reactions Used", "Reactions Available",
            "Storage Location", "Cassette"
        ]
        df_new = pd.DataFrame(columns=columns)
        df_new.to_excel(path, sheet_name="Template", index=False)
        return df_new

# --- INITIAL DATA LOAD & SESSION STATE SETUP ---
if 'reagents_df' not in st.session_state:
    st.session_state['reagents_df'] = load_data(file_path)

df = st.session_state['reagents_df']

st.title("DDLAB Reagents Database Management Tool")

# ======================================================================
# --- MULTI-CRITERIA SEARCH ---
# ======================================================================
st.header("Search Reagents")

SEARCH_FIELDS = [
    "Reagent Type", "Supplier", "Reagent Name",
    "Lot Number", "Storage Location", "Cassette"
]
selected_search_criteria = {}

st.write("### Choose a combination of criteria to filter by:")
cols = st.columns(len(SEARCH_FIELDS))

for i, field in enumerate(SEARCH_FIELDS):
    unique_values = ['-- All --'] + sorted(df[field].dropna().astype(str).unique().tolist())
    with cols[i]:
        selected_value = st.selectbox(f"Select {field}:", unique_values, key=f"search_{field}")
        selected_search_criteria[field] = selected_value

combined_search_filter = pd.Series([True] * len(df))
for field, value in selected_search_criteria.items():
    if value != '-- All --':
        combined_search_filter &= (df[field].astype(str) == value)

search_results = df[combined_search_filter]

if st.button("Apply Search Filters"):
    if search_results.empty:
        st.warning("⚠️ No reagents matched the selected criteria.")
    else:
        st.success(f"🔍 Found **{len(search_results)}** matching reagent(s):")
        st.dataframe(search_results)

# ======================================================================
# --- ADD NEW ENTRY ---
# ======================================================================
st.header("Add New Reagent")

with st.form("add_form"):
    new_type = st.text_input("Reagent Type")
    new_supplier = st.text_input("Supplier")
    new_name = st.text_input("Reagent Name")
    new_lot = st.text_input("Lot Number")
    new_expiry = st.text_input("Expiry Date")
    new_total = st.number_input("Total Reactions", min_value=0, step=1)
    new_used = st.number_input("Reactions Used", min_value=0, step=1)
    new_left = new_total - new_used
    new_location = st.text_input("Storage Location")
    new_cassette = st.text_input("Cassette")

    submitted = st.form_submit_button("Add Reagent")

    if submitted:
        new_row = {
            "Reagent Type": new_type,
            "Supplier": new_supplier,
            "Reagent Name": new_name,
            "Lot Number": new_lot,
            "Expiry Date": new_expiry,
            "Total Reactions": new_total,
            "Reactions Used": new_used,
            "Reactions Available": new_left,
            "Storage Location": new_location,
            "Cassette": new_cassette
        }

        new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        st.session_state['reagents_df'] = new_df
        new_df.to_excel(file_path, sheet_name="Template", index=False)

        st.success("✅ Reagent added! Refreshing database...")
        st.rerun()

# ======================================================================
# --- DELETE ENTRY ---
# ======================================================================
st.header("Delete Reagent")

DEL_FIELDS = ["Reagent Type", "Supplier", "Reagent Name", "Lot Number"]
selected_criteria = {}
cols = st.columns(len(DEL_FIELDS))

for i, field in enumerate(DEL_FIELDS):
    unique_values = ['-- All --'] + sorted(df[field].dropna().astype(str).unique().tolist())
    with cols[i]:
        selected_value = st.selectbox(f"Select {field}:", unique_values, key=f"delete_{field}")
        selected_criteria[field] = selected_value

combined_filter = pd.Series([True] * len(df))
for field, value in selected_criteria.items():
    if value != '-- All --':
        combined_filter &= (df[field].astype(str) == value)

rows_to_delete = df[combined_filter]
num_rows_to_delete = len(rows_to_delete)

if num_rows_to_delete == 0:
    st.info("No records match the selected criteria.")
else:
    st.warning(f"⚠️ {num_rows_to_delete} record(s) will be deleted:")
    st.dataframe(rows_to_delete)

    if st.button("Confirm Deletion 🗑️"):
        new_df = df[~combined_filter]
        st.session_state['reagents_df'] = new_df
        new_df.to_excel(file_path, sheet_name="Template", index=False)
        st.success(f"✅ Deleted {num_rows_to_delete} record(s). Refreshing database...")
        st.rerun()

# ======================================================================
# --- EDIT ENTRY ---
# ======================================================================
st.header("Edit Reagent")

EDIT_FIELDS = ["Reagent Type", "Supplier", "Reagent Name", "Lot Number"]
selected_edit_criteria = {}
cols = st.columns(len(EDIT_FIELDS))

for i, field in enumerate(EDIT_FIELDS):
    unique_values = ['-- Select --'] + sorted(df[field].dropna().astype(str).unique().tolist())
    with cols[i]:
        selected_value = st.selectbox(f"Filter by {field}:", unique_values, key=f"edit_{field}")
        selected_edit_criteria[field] = selected_value

combined_edit_filter = pd.Series([True] * len(df))
for field, value in selected_edit_criteria.items():
    if value != '-- Select --':
        combined_edit_filter &= (df[field].astype(str) == value)

rows_to_edit = df[combined_edit_filter]

if len(rows_to_edit) == 1:
    st.success("✅ One record selected for editing.")
    edit_index = rows_to_edit.index[0]
    existing_row = rows_to_edit.iloc[0]

    with st.form("edit_form"):
        edit_type = st.text_input("Reagent Type", value=str(existing_row['Reagent Type']))
        edit_supplier = st.text_input("Supplier", value=str(existing_row['Supplier']))
        edit_name = st.text_input("Reagent Name", value=str(existing_row['Reagent Name']))
        edit_lot = st.text_input("Lot Number", value=str(existing_row['Lot Number']))
        edit_expiry = st.text_input("Expiry Date", value=str(existing_row['Expiry Date']))
        edit_total = st.number_input("Total Reactions", min_value=0, value=int(existing_row.get('Total Reactions', 0)), step=1)
        edit_used = st.number_input("Reactions Used", min_value=0, value=int(existing_row.get('Reactions Used', 0)), step=1)
        edit_left = edit_total - edit_used
        edit_location = st.text_input("Storage Location", value=str(existing_row['Storage Location']))
        edit_cassette = st.text_input("Cassette", value=str(existing_row.get('Cassette', '')))

        submitted = st.form_submit_button("Update Reagent")
        if submitted:
            updated_row = {
                "Reagent Type": edit_type,
                "Supplier": edit_supplier,
                "Reagent Name": edit_name,
                "Lot Number": edit_lot,
                "Expiry Date": edit_expiry,
                "Total Reactions": edit_total,
                "Reactions Used": edit_used,
                "Reactions Available": edit_left,
                "Storage Location": edit_location,
                "Cassette": edit_cassette
            }

            for key, value in updated_row.items():
                st.session_state['reagents_df'].at[edit_index, key] = value

            st.session_state['reagents_df'].to_excel(file_path, sheet_name="Template", index=False)
            st.success("✅ Record updated! Refreshing database...")
            st.rerun()

elif len(rows_to_edit) == 0:
    st.info("No record selected. Please refine your criteria.")
else:
    st.warning(f"⚠️ {len(rows_to_edit)} records match the criteria. Please refine to exactly one.")

import streamlit as st
import pandas as pd
import os

# Set app layout on wide
st.set_page_config(layout="wide")

# File path
file_path = "Plastics_Database.xlsx"

# --- CACHE FUNCTION FOR DATA LOADING ---
@st.cache_data(show_spinner="Loading database...")
def load_data(path):
    if os.path.exists(path):
        return pd.read_excel(path, sheet_name="Template")
    else:
        # Create an empty DataFrame if the file doesn't exist
        columns = ["Plastic Type", "Size", "Catalog Number", "Supplier", "Quantità", "Box 96", "Box Location"]
        df_new = pd.DataFrame(columns=columns)
        df_new.to_excel(path, sheet_name="Template", index=False)
        return df_new

# --- INITIAL DATA LOAD & SESSION STATE SETUP ---
if 'plastics_df' not in st.session_state:
    st.session_state['plastics_df'] = load_data(file_path)

df = st.session_state['plastics_df']

st.title("DDLAB Plastics Database Management Tool")

# ======================================================================
# --- MULTI-CRITERIA SEARCH ---
# ======================================================================
st.header("Search Plastics")

SEARCH_FIELDS = ["Plastic Type", "Size", "Catalog Number", "Supplier", "Box Location"]
selected_search_criteria = {}

st.write("### Choose a combination of criteria to filter by:")
cols = st.columns(len(SEARCH_FIELDS))

filtered_search_df = df.copy()  # DataFrame che si restringe dinamicamente
selected_search_criteria = {}

for i, field in enumerate(SEARCH_FIELDS):
    # Calcola i valori possibili in base alle scelte precedenti
    possible_values = sorted(filtered_search_df[field].dropna().astype(str).unique().tolist())
    possible_values = ['-- All Samples --'] + possible_values
    
    with cols[i]:
        selected_value = st.selectbox(
            f"Select {field}:",
            possible_values,
            key=f"search_filter_by_{field}"
        )
        selected_search_criteria[field] = selected_value
    
    # Restringi i valori per i campi successivi
    if selected_value != '-- All Samples --':
        filtered_search_df = filtered_search_df[filtered_search_df[field].astype(str) == selected_value]

# Dopo il ciclo, i risultati corrispondono al DataFrame filtrato
search_results = filtered_search_df

if st.button("Apply Search Filters"):
    if search_results.empty:
        st.warning("⚠️ No plastics matched the selected criteria.")
    else:
        st.success(f"🔍 Found **{len(search_results)}** matching record(s):")
        st.dataframe(search_results)

# ======================================================================
# --- ADD NEW ENTRY ---
# ======================================================================
st.header("Add New Plastic Item")

with st.form("add_form"):
    new_type = st.text_input("Plastic Type")
    new_size = st.text_input("Size")
    new_catalog = st.text_input("Catalog Number")
    new_supplier = st.text_input("Supplier")
    new_qty = st.text_input("Quantità")
    new_box = st.text_input("Box 96")
    new_location = st.text_input("Box Location")

    submitted = st.form_submit_button("Add Plastic")

    if submitted:
        new_row = {"Plastic Type": new_type,
                   "Size": new_size,
                   "Catalog Number": new_catalog,
                   "Supplier": new_supplier,
                   "Quantità": new_qty,
                   "Box 96": new_box,
                   "Box Location": new_location}

        new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        st.session_state['data_df'] = new_df
        new_df.to_excel(file_path, sheet_name="Template", index=False)

        st.success("✅ Plastic item added! Refreshing database...")
        st.rerun()

# ======================================================================
# --- DELETE ENTRY ---
# ======================================================================
st.header("Delete Plastic Item")

DEL_FIELDS = ["Plastic Type", "Catalog Number", "Supplier"]
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
        st.session_state['data_df'] = new_df
        new_df.to_excel(file_path, sheet_name="Template", index=False)
        st.success(f"✅ Deleted {num_rows_to_delete} record(s). Refreshing database...")
        st.rerun()

# ======================================================================
# --- EDIT ENTRY ---
# ======================================================================
st.header("Edit Plastic Item")

EDIT_FIELDS = ["Plastic Type", "Catalog Number", "Supplier"]
selected_edit_criteria = {}
edit_cols = st.columns(len(EDIT_FIELDS))

st.write("### 1. Select the single sample you wish to edit:")

filtered_df = df.copy()  # DataFrame dinamico che si restringe a ogni selezione

for i, field in enumerate(EDIT_FIELDS):
    # Calcola i valori validi per questo campo in base alle scelte precedenti
    possible_values = sorted(filtered_df[field].dropna().astype(str).unique().tolist())
    possible_values = ['-- Select a Value --'] + possible_values

    with edit_cols[i]:
        selected_value = st.selectbox(
            f"Filter by {field}:",
            possible_values,
            key=f"edit_filter_by_{field}"
        )
        selected_edit_criteria[field] = selected_value

    # Applica il filtro per restringere i valori per i campi successivi
    if selected_value != '-- Select a Value --':
        filtered_df = filtered_df[filtered_df[field].astype(str) == selected_value]

# Alla fine, le righe candidate da modificare sono quelle del DataFrame filtrato
rows_to_edit = filtered_df

if len(rows_to_edit) == 1:
    st.success("✅ One record selected for editing.")
    edit_index = rows_to_edit.index[0]
    existing_row = rows_to_edit.iloc[0]

    with st.form("edit_form"):
        edit_type = st.text_input("Plastic Type", value=str(existing_row['Plastic Type']))
        edit_size = st.text_input("Size", value=str(existing_row['Size']))
        edit_catalog = st.text_input("Catalog Number", value=str(existing_row['Catalog Number']))
        edit_supplier = st.text_input("Supplier", value=str(existing_row['Supplier']))
        edit_qty = st.text_input("Quantità", value=str(existing_row['Quantità']))
        edit_box = st.text_input("Box 96", value=str(existing_row['Box 96']))
        edit_location = st.text_input("Box Location", value=str(existing_row['Box Location']))

        submitted = st.form_submit_button("Update Plastic")
        if submitted:
            updated_row = {"Plastic Type": edit_type,
                           "Size": edit_size,
                           "Catalog Number": edit_catalog,
                           "Supplier": edit_supplier,
                           "Quantità": edit_qty,
                           "Box 96": edit_box,
                           "Box Location": edit_location}

            for key, value in updated_row.items():
                st.session_state['data_df'].at[edit_index, key] = value

            st.session_state['data_df'].to_excel(file_path, sheet_name="Template", index=False)
            st.success("✅ Record updated! Refreshing database...")
            st.rerun()

elif len(rows_to_edit) == 0:
    st.info("No record selected. Please refine your criteria.")
else:
    st.warning(f"⚠️ {len(rows_to_edit)} records match the criteria. Please refine to exactly one.")

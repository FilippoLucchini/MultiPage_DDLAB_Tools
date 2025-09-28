import streamlit as st
import pandas as pd
import os

# Set app layout on wide
st.set_page_config(layout="wide")

st.title("🧪 Plastics Database")

file_path = "Plastics_Database.xlsx"
COLUMNS = ["Plastic Type", "Size", "Catalog Number", "Supplier", "Quantità", "Box 96", "Box Location"]

if os.path.exists(file_path):
    df = pd.read_excel(file_path)
else:
    df = pd.DataFrame(columns=COLUMNS)
    df.to_excel(file_path, index=False)

# ======================================================================
# --- MULTI-CRITERIA SEARCH (NEW SECTION) ---
# ======================================================================
st.header("Search Item")

# Define the fields available for searching
SEARCH_FIELDS = ["Plastic Type", "Size", "Catalog Number", "Supplier", "Box Location"]

selected_search_criteria = {}

st.write("### Choose a combination of criteria to filter by:")
# Create columns to display the select boxes
cols = st.columns(len(SEARCH_FIELDS))

for i, field in enumerate(SEARCH_FIELDS):
    # Get unique values, ensuring no NaN values are passed to sort, and prepend a 'wildcard' option
    unique_values = ['-- All Items --'] + sorted(df[field].dropna().astype(str).unique().tolist())
    
    with cols[i]:
        # Use a unique key for each selectbox
        selected_value = st.selectbox(
            f"Select {field}:",
            unique_values,
            key=f"search_filter_by_{field}"
        )
        selected_search_criteria[field] = selected_value

# Filter the DataFrame based on the selected criteria
combined_search_filter = pd.Series([True] * len(df))

for field, value in selected_search_criteria.items():
    if value != '-- All Samples --':
        # Apply the filter. Note: astype(str) is used for consistency with selectbox options.
        combined_search_filter &= (df[field].astype(str) == value)

search_results = df[combined_search_filter]

# Display the search results
if st.button("Apply Search Filters"):
    if search_results.empty:
        st.warning("⚠️ No samples matched the selected criteria.")
    else:
        st.success(f"🔍 Found **{len(search_results)}** matching sample(s):")
        st.dataframe(search_results)

# ----------------------------------------------------------------------

# --- Add ---
st.header("➕ Add New Plastic Item")
with st.form("add_form"):
    new_data = {col: st.text_input(col) for col in COLUMNS}
    add_submit = st.form_submit_button("Add Plastic")
    if add_submit:
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_excel(file_path, index=False)
        st.success("✅ Plastic item added!")
        st.rerun()

# --- Delete ---
st.header("❌ Delete Plastic Item")
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
st.header("✏️ Edit Plastic Item")
with st.form("edit_form"):
    edit_field = st.selectbox("Choose field:", COLUMNS, key="edit_field")
    edit_values = sorted(df[edit_field].dropna().unique()) if not df.empty else []
    edit_value = st.selectbox("Select value to edit:", edit_values, key="edit_value")
    new_values = {col: st.text_input(f"New {col}", value=df.loc[df[edit_field]==edit_value, col].iloc[0] if not df[df[edit_field]==edit_value].empty else "") for col in COLUMNS}
    edit_submit = st.form_submit_button("Update")
    if edit_submit:
        df.loc[df[edit_field]==edit_value, COLUMNS] = list(new_values.values())
        df.to_excel(file_path, index=False)
        st.success("✅ Plastic item updated!")
        st.rerun()

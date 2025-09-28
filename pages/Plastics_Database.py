import streamlit as st
import pandas as pd
import os

# Set app layout on wide
st.set_page_config(layout="wide")

st.title("🧪 Plastics Database")

file_path = "Plastics_Database.xlsx"
COLUMNS = ["Plastic Type", "Catalog Number", "Supplier", "Box Location"]

if os.path.exists(file_path):
    df = pd.read_excel(file_path)
else:
    df = pd.DataFrame(columns=COLUMNS)
    df.to_excel(file_path, index=False)

# --- Define the Reset Callback Function ---
# This function is called when the search field selection changes.
def reset_search_value():
    """Clears the value selection when the field changes."""
    # Ensure the dynamic key for the value selectbox is defined in session state
    # and set it to None or the first value to force a reset.
    current_field = st.session_state.get("search_field", COLUMNS[0])
    value_key = f"search_value_{current_field}"
    
    # Try to delete the key from session state, forcing the component to re-render
    # with its default setting (usually the first option).
    if value_key in st.session_state:
        del st.session_state[value_key]

# ----------------------------------------
# --- Search ---
st.header("🔍 Search Plastics")
with st.form("search_form"):
    
    # 1. Use on_change callback with the field selection
    field = st.selectbox(
        "Choose field to search by:", 
        COLUMNS, 
        key="search_field", # Keep this key static for the callback to reference
        on_change=reset_search_value # Calls the function when field changes
    )
    
    # 2. Get the unique values for the currently selected field
    values = sorted(df[field].dropna().unique()) if not df.empty else []
    
    # 3. Use the dynamic key for the value selectbox
    value_key = f"search_value_{field}"
    
    # The default index is set to 0, which will be the first item in the new list.
    value = st.selectbox(
        "Start typing to search:", 
        options=values, 
        key=value_key, # Dynamic key
        index=0 if values else None # Ensures it selects the first item (resets to it)
    )
    
    submitted = st.form_submit_button("Search")
    if submitted:
        # Check if a value was actually selected before filtering
        if value:
            st.dataframe(df[df[field] == value])
        else:
            st.warning("Please select a value to search.")


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

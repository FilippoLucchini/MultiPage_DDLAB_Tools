import streamlit as st
import pandas as pd
import os

# Set app layout on wide
st.set_page_config(layout="wide")

# File path
file_path = "Freezer_Database.xlsx"

# --- CACHE FUNCTION FOR DATA LOADING ---
@st.cache_data(show_spinner="Loading database...")
def load_data(path):
    """
    Loads the DataFrame from the Excel file. 
    Streamlit uses the file's modification time (mtime) 
    to automatically bust the cache when the file is saved.
    """
    if os.path.exists(path):
        return pd.read_excel(path)
    else:
        # Create an empty DataFrame if the file doesn't exist
        columns = ["Freezer Name", "Freezer Location", "Cassetto", "Project", "Box_Number_If_Available", "Type_Of_Sample", "Sample Batch", "Samples_ID_In_Batch", "Throw_Away_Date_If_Available"]
        df_new = pd.DataFrame(columns=columns)
        df_new.to_excel(path, index=False)
        return df_new

# --- INITIAL DATA LOAD & SESSION STATE SETUP ---
if 'data_df' not in st.session_state:
    # Use the cached function to load the data.
    # The file's modification time is used as an implicit hash parameter by Streamlit.
    st.session_state['data_df'] = load_data(file_path)

# Always reference the live DataFrame from session state
df = st.session_state['data_df']

st.title("DDLAB Freezer Database Management Tool")

# ======================================================================
# --- MULTI-CRITERIA SEARCH (NEW SECTION) ---
# ======================================================================
st.header("Search Sample")

# Define the fields available for searching
SEARCH_FIELDS = ["Freezer Name", "Freezer Location", "Cassetto", "Project", "Type_Of_Sample", "Sample Batch", "Samples_ID_In_Batch"]

selected_search_criteria = {}

st.write("### Choose a combination of criteria to filter by:")
# Create columns to display the select boxes
cols = st.columns(len(SEARCH_FIELDS))

for i, field in enumerate(SEARCH_FIELDS):
    # Get unique values, ensuring no NaN values are passed to sort, and prepend a 'wildcard' option
    unique_values = ['-- All Samples --'] + sorted(df[field].dropna().astype(str).unique().tolist())
    
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

# --- ADD NEW ENTRY ---
# --- Manually define options based on the image data ---

# Freezer Name Options (Column 1 from image: A, B, C, D, E)
FREEZER_NAME_OPTIONS = sorted(['A', 'B', 'C', 'D', 'E', 'F'])
FREEZER_NAME_OPTIONS.insert(0, "-- Select Existing or Add New --")
FREEZER_NAME_OPTIONS.append("-- Add New Freezer Name --")

# Freezer Location Options (Column 2 from image: 1.63a, 2.01, Comune_1_Piano, Comune_2_Piano, Piramide)
FREEZER_LOCATION_OPTIONS = sorted(['1.63a', '2.01', 'Comune 1 Piano', 'Comune 2 Piano', 'Piramide'])
FREEZER_LOCATION_OPTIONS.insert(0, "-- Select Existing or Add New --")
FREEZER_LOCATION_OPTIONS.append("-- Add New Freezer Location --")

# Freezer Location Options (Column 3 from image: 1, 2, 3, 4, 5, 6, 7)
CASSETTO_OPTIONS = sorted(['1', '2', '3', '4', '5', '6', '7'])
CASSETTO_OPTIONS.insert(0, "-- Select Existing or Add New --")
CASSETTO_OPTIONS.append("-- Add New Cassetto --")

# Type_Of_Sample Options (Column 3 from image: gDNA, gDNA Dilution, Library, Capture, Reagents)
TYPE_OF_SAMPLE_OPTIONS = sorted(['gDNA', 'gDNA Dilution', 'Library', 'Capture', 'Reagents'])
TYPE_OF_SAMPLE_OPTIONS.insert(0, "-- Select Existing or Add New --")
TYPE_OF_SAMPLE_OPTIONS.append("-- Add New Type --")


st.header("Add New Sample")

# NOTE: The Project field selection is preserved from the previous response.
# You need to ensure 'project_options' and 'type_options' are still defined
# before this block if you want Project to remain a selectbox.

with st.form("add_form"):
    
    # --- FREEZER NAME (New Selectbox) ---
    selected_freezer = st.selectbox("Freezer Name:", FREEZER_NAME_OPTIONS, key="select_freezer")
    if selected_freezer == "-- Add New Freezer Name --":
        new_freezer = st.text_input("Enter New Freezer Name:", key="new_freezer_input")
    else:
        new_freezer = selected_freezer
    # ------------------------------------

    # --- FREEZER LOCATION (New Selectbox) ---
    selected_location = st.selectbox("Freezer Location:", FREEZER_LOCATION_OPTIONS, key="select_location")
    if selected_location == "-- Add New Freezer Location --":
        new_location = st.text_input("Enter New Freezer Location:", key="new_location_input")
    else:
        new_location = selected_location
    # ------------------------------------
    
      # --- CASSETTO (New Selectbox) ---
    selected_cassetto = st.selectbox("Cassetto:", CASSETTO_OPTIONS, key="select_cassetto")
    if selected_cassetto == "-- Add New Cassetto --":
        new_cassetto = st.text_input("Enter New Cassetto:", key="new_cassetto_input")
    else:
        new_cassetto = selected_cassetto
    # ------------------------------------
    
    # --- TYPE OF SAMPLE (Updated Selectbox) ---
    selected_type = st.selectbox("Type_Of_Sample:", TYPE_OF_SAMPLE_OPTIONS, key="select_type")
    if selected_type == "-- Add New Type --":
        new_type = st.text_input("Enter New Sample Type:", key="new_type_input")
    else:
        new_type = selected_type
    # ------------------------------------

    # Assuming Project remains a selectbox (replace with st.text_input if needed)
    # The variables 'new_project' should be defined similarly to 'new_type' above 
    # using 'project_options' if you want it to be a selectbox.
    # For simplicity, let's keep it as text_input if you didn't define its options list.
    new_project = st.text_input("Project", key="add_project_text") 
    
    # The rest remain as text input
    new_box = st.text_input("Box_Number_If_Available")
    new_batch = st.text_input("Sample Batch")
    new_id = st.text_input("Samples_ID_In_Batch")
    new_date = st.text_input("Throw_Away_Date_If_Available")
    
    submitted = st.form_submit_button("Add Sample")
    
    if submitted:
        # Check for placeholders or missing new entries
        if new_freezer in ["-- Select Existing or Add New --", "-- Add New Freezer Name --"] or \
           new_location in ["-- Select Existing or Add New --", "-- Add New Freezer Location --"] or \
           new_type in ["-- Select Existing or Add New --", "-- Add New Type --"] or \
           (new_freezer == "-- Add New Freezer Name --" and not st.session_state.get("new_freezer_input")) or \
           (new_location == "-- Add New Freezer Location --" and not st.session_state.get("new_location_input")) or \
           (new_type == "-- Add New Type --" and not st.session_state.get("new_type_input")):
            st.error("Please select an existing value or enter a name for all required fields (Freezer Name/Location/Type).")
            st.stop() 

        new_row = {"Freezer Name": new_freezer,
                   "Freezer Location": new_location,
                   "Project": new_project,
                   "Box_Number_If_Available": new_box,
                   "Type_Of_Sample": new_type,
                   "Sample Batch": new_batch,
                   "Samples_ID_In_Batch": new_id,
                   "Throw_Away_Date_If_Available": new_date}
                   
        # Update and save logic (assuming session state/caching is correctly set up)
        new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        st.session_state['data_df'] = new_df 

        new_df.to_excel(file_path, index=False)
        
        # load_data.clear() # Uncomment if using the cached function
        st.success("✅ Sample added! Refreshing database...")
        st.rerun()

# ----------------------------------------------------------------------

# --- DELETE ENTRY ---
st.header("Precise Sample Deletion")

DEL_FIELDS = ["Project", "Type_Of_Sample", "Sample Batch", "Samples_ID_In_Batch"]
selected_criteria = {}

st.write("### Choose the combination of criteria for deletion:")
cols = st.columns(len(DEL_FIELDS))

for i, field in enumerate(DEL_FIELDS):
    unique_values = ['-- All Samples --'] + sorted(df[field].dropna().astype(str).unique().tolist())
    with cols[i]:
        selected_value = st.selectbox(
            f"Select {field}:",
            unique_values,
            key=f"filter_by_{field}"
        )
        selected_criteria[field] = selected_value

# Apply filter to determine rows to delete
combined_filter = pd.Series([True] * len(df))
for field, value in selected_criteria.items():
    if value != '-- All Samples --':
        combined_filter &= (df[field].astype(str) == value) 
        
rows_to_delete = df[combined_filter]
num_rows_to_delete = len(rows_to_delete)

# Reset confirmation state if the filters change and the number of rows is different
if st.session_state.get('last_delete_count', 0) != num_rows_to_delete:
     st.session_state['delete_confirmation_needed'] = False
     st.session_state['last_delete_count'] = num_rows_to_delete

with st.form("precise_delete_form"):
    st.write("### Current Selection Filter")
    
    if rows_to_delete.empty:
        st.info("No samples match the selected criteria.")
        st.form_submit_button("Delete Sample", disabled=True)
        
    else:
        st.warning(f"⚠️ **{num_rows_to_delete} row(s)** will be deleted based on the criteria below:")
        st.dataframe(rows_to_delete)
        
        # --- CONFIRMATION LOGIC ---
        
        if st.session_state.get('delete_confirmation_needed', False) and st.session_state.get('last_delete_count', 0) == num_rows_to_delete:
            
            st.error(f"**ARE YOU SURE?** You are about to permanently delete **{num_rows_to_delete}** samples.")
            
            # Use two columns for the confirmation buttons
            confirm_col, cancel_col = st.columns(2)
            
            with confirm_col:
                final_confirm = st.form_submit_button("YES, CONFIRM PERMANENT DELETION 🗑️")
            
            with cancel_col:
                # The new "No" button
                cancel_delete = st.form_submit_button("NO, CANCEL DELETION ❌")
            
            if final_confirm:
                # Execution of delete
                new_df = df[~combined_filter]
                st.session_state['data_df'] = new_df
                new_df.to_excel(file_path, index=False)
                
                # Clear state and cache, then rerun
                st.session_state['delete_confirmation_needed'] = False
                st.session_state['last_delete_count'] = 0
                load_data.clear()
                st.success(f"✅ Successfully deleted {num_rows_to_delete} sample(s)! Refreshing database...")
                st.rerun()

            if cancel_delete:
                # Reset state variables to go back to the selection
                st.session_state['delete_confirmation_needed'] = False
                st.session_state['last_delete_count'] = 0
                st.info("Deletion cancelled. Returning to sample selection.")
                st.rerun() # Rerun to clear the confirmation prompt

        else:
            # 1. Show the initial delete button
            initial_delete = st.form_submit_button(f"Prepare Deletion of {num_rows_to_delete} Samples")
            
            if initial_delete:
                # Set the state variable to prompt for confirmation on the next run
                st.session_state['delete_confirmation_needed'] = True
                st.session_state['last_delete_count'] = num_rows_to_delete
                st.rerun()
    
# ----------------------------------------------------------------------
# --- EDIT ENTRY (NEW SECTION) ---
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

st.header("Edit Existing Sample")

EDIT_FIELDS = ["Project", "Type_Of_Sample", "Sample Batch", "Samples_ID_In_Batch"]
selected_edit_criteria = {}
edit_cols = st.columns(len(EDIT_FIELDS))

st.write("### 1. Select the single sample you wish to edit:")

for i, field in enumerate(EDIT_FIELDS):
    unique_values = ['-- Select a Value --'] + sorted(df[field].dropna().astype(str).unique().tolist())
    with edit_cols[i]:
        selected_value = st.selectbox(
            f"Filter by {field}:",
            unique_values,
            key=f"edit_filter_by_{field}"
        )
        selected_edit_criteria[field] = selected_value

# Apply filter to find rows to edit
combined_edit_filter = pd.Series([True] * len(df))
for field, value in selected_edit_criteria.items():
    if value != '-- Select a Value --':
        combined_edit_filter &= (df[field].astype(str) == value) 
        
rows_to_edit = df[combined_edit_filter]

# Check if a single row is selected
if len(rows_to_edit) == 1:
    st.success("✅ One sample selected for editing.")
    
    # Get the index of the single row to edit
    edit_index = rows_to_edit.index[0]
    
    # Get the existing data for pre-population
    existing_row = rows_to_edit.iloc[0]
    
    st.write("### 2. Edit the fields below:")

    with st.form("edit_form"):
        # --- FREEZER NAME (PRE-POPULATED) ---
        default_freezer = str(existing_row['Freezer Name'])
        
        # Insert default value into options list if it's not already one of the 'special' values
        edit_freezer_options = FREEZER_NAME_OPTIONS.copy()
        if default_freezer not in edit_freezer_options and default_freezer not in ["-- Select Existing or Add New --", "-- Add New Freezer Name --"]:
             edit_freezer_options.insert(1, default_freezer)

        edit_selected_freezer = st.selectbox("Freezer Name:", edit_freezer_options, 
                                             index=edit_freezer_options.index(default_freezer) if default_freezer in edit_freezer_options else 0,
                                             key="edit_select_freezer")
        edit_new_freezer_input = st.text_input("Enter New Freezer Name:", disabled=(edit_selected_freezer != "-- Add New Freezer Name --"), 
                                                key="edit_new_freezer_input")
        final_edit_freezer = edit_new_freezer_input if edit_selected_freezer == "-- Add New Freezer Name --" and edit_new_freezer_input else edit_selected_freezer

        # --- FREEZER LOCATION (PRE-POPULATED) ---
        default_location = str(existing_row['Freezer Location'])
        edit_location_options = FREEZER_LOCATION_OPTIONS.copy()
        if default_location not in edit_location_options and default_location not in ["-- Select Existing or Add New --", "-- Add New Freezer Location --"]:
             edit_location_options.insert(1, default_location)

        edit_selected_location = st.selectbox("Freezer Location:", edit_location_options,
                                              index=edit_location_options.index(default_location) if default_location in edit_location_options else 0,
                                              key="edit_select_location")
        edit_new_location_input = st.text_input("Enter New Freezer Location:", disabled=(edit_selected_location != "-- Add New Freezer Location --"), 
                                                key="edit_new_location_input")
        final_edit_location = edit_new_location_input if edit_selected_location == "-- Add New Freezer Location --" and edit_new_location_input else edit_selected_location

        # --- CASSETTO (PRE-POPULATED) ---
        default_cassetto = str(existing_row['Cassetto'])
        edit_cassetto_options = CASSETTO_OPTIONS.copy()
        if default_cassetto not in edit_cassetto_options and default_cassetto not in ["-- Select Existing or Add New --", "-- Add New Cassetto --"]:
             edit_cassetto_options.insert(1, default_cassetto)
             
        edit_selected_cassetto = st.selectbox("Cassetto:", edit_cassetto_options,
                                              index=edit_cassetto_options.index(default_cassetto) if default_cassetto in edit_cassetto_options else 0,
                                              key="edit_select_cassetto")
        edit_new_cassetto_input = st.text_input("Enter New Cassetto:", disabled=(edit_selected_cassetto != "-- Add New Cassetto --"), 
                                                key="edit_new_cassetto_input")
        final_edit_cassetto = edit_new_cassetto_input if edit_selected_cassetto == "-- Add New Cassetto --" and edit_new_cassetto_input else edit_selected_cassetto

        # --- TYPE OF SAMPLE (PRE-POPULATED) ---
        default_type = str(existing_row['Type_Of_Sample'])
        edit_type_options = TYPE_OF_SAMPLE_OPTIONS.copy()
        if default_type not in edit_type_options and default_type not in ["-- Select Existing or Add New --", "-- Add New Type --"]:
             edit_type_options.insert(1, default_type)
        
        edit_selected_type = st.selectbox("Type_Of_Sample:", edit_type_options,
                                          index=edit_type_options.index(default_type) if default_type in edit_type_options else 0,
                                          key="edit_select_type")
        edit_new_type_input = st.text_input("Enter New Sample Type:", disabled=(edit_selected_type != "-- Add New Type --"), 
                                            key="edit_new_type_input")
        final_edit_type = edit_new_type_input if edit_selected_type == "-- Add New Type --" and edit_new_type_input else edit_selected_type


        # --- REST OF THE FIELDS (PRE-POPULATED TEXT INPUTS) ---
        edit_project = st.text_input("Project", value=str(existing_row['Project']), key="edit_project_text") 
        edit_box = st.text_input("Box_Number_If_Available", value=str(existing_row['Box_Number_If_Available']), key="edit_box_text")
        edit_batch = st.text_input("Sample Batch", value=str(existing_row['Sample Batch']), key="edit_batch_text")
        edit_id = st.text_input("Samples_ID_In_Batch", value=str(existing_row['Samples_ID_In_Batch']), key="edit_id_text")
        edit_date = st.text_input("Throw_Away_Date_If_Available", value=str(existing_row['Throw_Away_Date_If_Available']), key="edit_date_text")

        edit_submitted = st.form_submit_button("Update Sample")

        if edit_submitted:
            # Basic validation check
            if final_edit_freezer in ["-- Select Existing or Add New --", "-- Add New Freezer Name --"] or \
               final_edit_location in ["-- Select Existing or Add New --", "-- Add New Freezer Location --"] or \
               final_edit_type in ["-- Select Existing or Add New --", "-- Add New Type --"]:
                st.error("Please select an existing value or enter a name for all required fields (Freezer Name/Location/Type).")
                st.stop() 

            # Create a dictionary of the updated values
            updated_row = {
                "Freezer Name": final_edit_freezer,
                "Freezer Location": final_edit_location,
                "Cassetto": final_edit_cassetto, 
                "Project": edit_project,
                "Box_Number_If_Available": edit_box,
                "Type_Of_Sample": final_edit_type,
                "Sample Batch": edit_batch,
                "Samples_ID_In_Batch": edit_id,
                "Throw_Away_Date_If_Available": edit_date
            }
            
            # Update the DataFrame in session state directly at the found index
            for key, value in updated_row.items():
                st.session_state['data_df'].at[edit_index, key] = value
                
            # Save the updated DataFrame to the Excel file
            st.session_state['data_df'].to_excel(file_path, index=False)
            
            load_data.clear()
            st.success(f"✅ Sample **{edit_index}** updated successfully! Refreshing database...")
            st.rerun()

elif len(rows_to_edit) == 0:
    st.info("No sample selected. Please choose criteria that match exactly one existing sample to enable editing.")
else:
    st.warning(f"⚠️ **{len(rows_to_edit)}** samples match the current criteria. Please refine your selection to match exactly ONE sample to enable editing.")

# ----------------------------------------------------------------------















 will the excel update after each modifications from the app, so that if then i download it it will be up to date?

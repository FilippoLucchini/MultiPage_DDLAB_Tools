import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- Configuration for a nice-looking app ---
st.set_page_config(layout="wide")

# --- Initialize Session State for Data Storage ---
if 'equipment_data' not in st.session_state:
    st.session_state.equipment_data = {
        'MiSeq': {'status': 'Running', 'last_cleaned': datetime(2025, 9, 28), 'next_maint': '12/15/2025'},
        'Qubit': {'status': 'Available', 'last_cleaned': datetime(2025, 10, 1), 'next_maint': 'N/A'},
        'Bioanalyzer': {'status': 'In Use', 'last_cleaned': datetime(2025, 9, 25), 'next_maint': '01/20/2026'},
    }
if 'bookings' not in st.session_state:
    st.session_state.bookings = pd.DataFrame({
        'Equipment': ['MiSeq', 'Qubit'],
        'User': ['Dr. Chen', 'J. Smith'],
        'Start Time': [datetime.now() + timedelta(hours=1), datetime.now() + timedelta(days=1)],
        'End Time': [datetime.now() + timedelta(hours=5), datetime.now() + timedelta(days=1, hours=2)],
        'Project': ['RNA-Seq 2025', 'gDNA QC'],
    })
if 'maintenance_log' not in st.session_state:
    st.session_state.maintenance_log = pd.DataFrame({
        'Date': [datetime(2025, 9, 28), datetime(2025, 9, 20)],
        'Equipment': ['MiSeq', 'Bioanalyzer'],
        'Type': ['Cleaning', 'Reported Issue'],
        'Details': ['Flow cell deep clean performed.', 'Fluidics error, restarted system.'],
        'User': ['T. Lee', 'A. Khan'],
    })


# --- Helper Functions for Data Management ---

def add_booking(equipment, user, start, end, project):
    """Adds a new booking to the session state dataframe."""
    new_booking = pd.DataFrame([{
        'Equipment': equipment,
        'User': user,
        'Start Time': start,
        'End Time': end,
        'Project': project
    }])
    st.session_state.bookings = pd.concat([st.session_state.bookings, new_booking], ignore_index=True)

def add_maintenance_log(date, equipment, log_type, details, user):
    """Adds a new entry to the maintenance log dataframe."""
    new_log = pd.DataFrame([{
        'Date': date,
        'Equipment': equipment,
        'Type': log_type,
        'Details': details,
        'User': user,
    }])
    st.session_state.maintenance_log = pd.concat([st.session_state.maintenance_log, new_log], ignore_index=True)


# --- Streamlit UI Components ---

st.title("🔬 Equipment Booking & Maintenance Log")
st.markdown("Centralized management for shared laboratory instruments.")

st.sidebar.header("Equipment Management Actions")
selected_action = st.sidebar.radio(
    "Choose an Action:",
    ["Book Equipment", "Log Maintenance/Issue", "View Equipment Status"]
)

# --- Equipment Status Dashboard (Main View) ---
if selected_action == "View Equipment Status":
    st.header("Instrument Health Dashboard")
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for i, (name, data) in enumerate(st.session_state.equipment_data.items()):
        with cols[i % 3]:
            # Use Streamlit containers for a card-like look
            with st.container(border=True):
                st.subheader(f"🧬 {name}")
                st.metric(
                    label="Status",
                    value=data['status'],
                    delta="Running" if data['status'] == 'Running' else None,
                    delta_color="off" if data['status'] == 'Available' else "normal" # Custom color logic for status
                )
                st.write(f"**Last Cleaned:** {data['last_cleaned'].strftime('%Y-%m-%d')}")
                st.write(f"**Next Maint:** {data['next_maint']}")

    st.subheader("Current & Upcoming Bookings")
    # Display the dataframe with nice formatting
    st.dataframe(
        st.session_state.bookings.sort_values('Start Time'),
        hide_index=True,
        column_config={
            "Start Time": st.column_config.DatetimeColumn("Start Time", format="YYYY-MM-DD HH:mm"),
            "End Time": st.column_config.DatetimeColumn("End Time", format="YYYY-MM-DD HH:mm"),
        }
    )

    st.subheader("Maintenance and Issue Log History")
    st.dataframe(
        st.session_state.maintenance_log.sort_values('Date', ascending=False),
        hide_index=True,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
        }
    )


# --- Booking Form (Sidebar Action) ---
elif selected_action == "Book Equipment":
    st.header("Book Equipment Time Slot")
    
    with st.form("booking_form"):
        equipment = st.selectbox("Equipment", list(st.session_state.equipment_data.keys()))
        user = st.text_input("Your Name/Initials")
        project = st.text_input("Project ID/Name")
        
        # Use columns for start/end time
        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.date_input("Start Date", datetime.now())
            start_time = st.time_input("Start Time", datetime.now())
        with col_end:
            end_date = st.date_input("End Date", datetime.now() + timedelta(hours=4))
            end_time = st.time_input("End Time", datetime.now() + timedelta(hours=4))
        
        submitted = st.form_submit_button("Submit Booking")

        if submitted:
            start_dt = datetime.combine(start_date, start_time)
            end_dt = datetime.combine(end_date, end_time)

            if not user or not project:
                st.error("Please fill in your Name and Project ID.")
            elif end_dt <= start_dt:
                st.error("End time must be after the start time.")
            else:
                add_booking(equipment, user, start_dt, end_dt, project)
                st.success(f"Booking confirmed for {equipment} from {start_dt.strftime('%Y-%m-%d %H:%M')} to {end_dt.strftime('%Y-%m-%d %H:%M')}.")


# --- Maintenance Log Form (Sidebar Action) ---
elif selected_action == "Log Maintenance/Issue":
    st.header("Log Maintenance or Report an Issue")

    with st.form("maintenance_form"):
        log_date = st.date_input("Date of Action/Issue", datetime.now())
        equipment = st.selectbox("Equipment", list(st.session_state.equipment_data.keys()))
        user = st.text_input("Your Name/Initials")
        
        log_type = st.radio(
            "Type of Log:",
            ["Cleaning", "Scheduled Maintenance", "Reported Issue", "Other"]
        )
        
        details = st.text_area("Details of Action/Issue", help="Describe the maintenance performed or the issue encountered (e.g., 'Flow cell washed', 'No power', 'Error code 503').")
        
        submitted = st.form_submit_button("Submit Log Entry")

        if submitted:
            if not user or not details:
                st.error("Please fill in your Name and Details.")
            else:
                add_maintenance_log(log_date, equipment, log_type, details, user)
                st.success(f"Log entry recorded for {equipment} on {log_date.strftime('%Y-%m-%d')}.")








 will the excel update after each modifications from the app, so that if then i download it it will be up to date?

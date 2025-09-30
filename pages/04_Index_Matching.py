import streamlit as st
import pandas as pd

# -------------------------------
# Utility check function
# -------------------------------
def has_space_or_hyphen(value):
    """Return True if the value contains spaces or hyphens, otherwise False."""
    if pd.isna(value):
        return False
    return (" " in str(value)) or ("-" in str(value))

# -------------------------------
# Character match function
# -------------------------------
def char_matches(str1, str2):
    """Count positional character matches between two strings."""
    if pd.isna(str1) or pd.isna(str2) or str1 == "" or str2 == "":
        return 0
    min_len = min(len(str1), len(str2))
    return sum(str1[i] == str2[i] for i in range(min_len))

# -------------------------------
# Count mismatches
# -------------------------------
def mismatches(str1, str2):
    """Return number of mismatches between two strings."""
    if pd.isna(str1) or pd.isna(str2):
        return None
    min_len = min(len(str1), len(str2))
    matches = sum(str1[i] == str2[i] for i in range(min_len))
    return min_len - matches

# -------------------------------
# Streamlit app
# -------------------------------
st.title("🔍 Index Matching & Data Quality Tool")

uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Check required columns
    required_columns = ["Lane", "index7", "CGF_ID", "Sample_ID", "Pool_Cattura", "CGF_Pool_ID"]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        st.error(f"❌ Missing required columns in file: {', '.join(missing_cols)}")
        st.stop()

    # Add Excel row info
    df["Excel_Row"] = df.index + 2  
    df["string_length"] = df["index7"].astype(str).str.len()

    # Input preview
    st.subheader("📊 Input Data Preview")
    st.dataframe(df.head())

    # -------------------------------
    # Data Quality Checks
    # -------------------------------
    st.subheader("🧪 Data Quality Checks")

    # Checks
    duplicated_cgf = df[df["CGF_ID"].duplicated(keep=False)]
    duplicated_sample = df[df["Sample_ID"].duplicated(keep=False)]
    cgf_format_issues = df[df["CGF_ID"].apply(has_space_or_hyphen)]
    sample_format_issues = df[df["Sample_ID"].apply(has_space_or_hyphen)]

    # Report summary
    st.markdown(f"""
    **Summary:**
    - 🧬 Duplicated CGF_ID: **{len(duplicated_cgf)}**
    - 🧪 Duplicated Sample_ID: **{len(duplicated_sample)}**
    - ⚠️ CGF_IDs with spaces/hyphens: **{len(cgf_format_issues)}**
    - ⚠️ Sample_IDs with spaces/hyphens: **{len(sample_format_issues)}**
    """)

    if not duplicated_cgf.empty:
        st.warning("Duplicated CGF_IDs (full rows):")
        st.dataframe(duplicated_cgf)

    if not duplicated_sample.empty:
        st.warning("Duplicated Sample_IDs (full rows):")
        st.dataframe(duplicated_sample)

    if not cgf_format_issues.empty:
        st.warning("CGF_IDs with spaces or hyphens (full rows):")
        st.dataframe(cgf_format_issues)

    if not sample_format_issues.empty:
        st.warning("Sample_IDs with spaces or hyphens (full rows):")
        st.dataframe(sample_format_issues)

    # -------------------------------
    # Lane-specific demultiplexing report
    # -------------------------------
    st.subheader("🧾 Demultiplexing Recommendations by Lane")

    for lane in df["Lane"].unique():
        lane_data = df[df["Lane"] == lane].reset_index(drop=True)

        status = "✅ Demultiplexing non stringente"
        note = []
        mismatch_rows = []

        for i in range(len(lane_data)):
            for j in range(i + 1, len(lane_data)):
                str1 = str(lane_data.loc[i, "index7"])
                str2 = str(lane_data.loc[j, "index7"])
                mm = mismatches(str1, str2)

                mismatch_rows.append({
                    "Sample_1": lane_data.loc[i, "Sample_ID"],
                    "Sample_2": lane_data.loc[j, "Sample_ID"],
                    "Index_1": str1,
                    "Index_2": str2,
                    "Mismatches": mm
                })

                if str1 == str2:
                    status = "❌ Errore: stessi indici presenti"
                    note.append(f"Samples {lane_data.loc[i,'Sample_ID']} and {lane_data.loc[j,'Sample_ID']} hanno lo stesso indice.")
                elif mm == 1 and status != "❌ Errore: stessi indici presenti":
                    status = "⚠️ Demultiplexing stringente"
                    note.append(f"Samples {lane_data.loc[i,'Sample_ID']} and {lane_data.loc[j,'Sample_ID']} hanno 1 mismatch.")

        st.markdown(f"**Lane {lane}:** {status}")
        if note:
            for n in note:
                st.markdown(f"- {n}")

        # Tabella con tutte le coppie e mismatch
        st.dataframe(pd.DataFrame(mismatch_rows))

else:
    st.info("👆 Upload an Excel file to start the analysis.")

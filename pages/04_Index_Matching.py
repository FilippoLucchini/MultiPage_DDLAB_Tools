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
# Filter matching pairs function
# -------------------------------
def filter_matching_pairs(df):
    result = []

    for lane in df["Lane"].unique():
        lane_data = df[df["Lane"] == lane].reset_index(drop=True)

        for i in range(len(lane_data)):
            for j in range(i + 1, len(lane_data)):  # avoid duplicate/self comparisons
                str1 = str(lane_data.loc[i, "index7"])
                str2 = str(lane_data.loc[j, "index7"])
                len1 = len(str1)
                len2 = len(str2)

                matches = char_matches(str1, str2)
                min_length = min(len1, len2)

                # Soglie fisse
                if min_length == 12:
                    match_threshold = 11
                elif min_length == 10:
                    match_threshold = 9
                elif min_length == 8:
                    match_threshold = 7
                else:
                    match_threshold = 5

                if matches >= match_threshold:
                    result.append({
                        "lane": lane,
                        "GCF_ID_string1": lane_data.loc[i, "CGF_ID"],
                        "GCF_ID_string2": lane_data.loc[j, "CGF_ID"],
                        "Sample_ID_1": lane_data.loc[i, "Sample_ID"],
                        "Sample_ID_2": lane_data.loc[j, "Sample_ID"],
                        "index7_string1": str1,
                        "index7_string2": str2,
                        "length1": len1,
                        "length2": len2,
                        "matches": matches
                    })

    return pd.DataFrame(result)

# -------------------------------
# Streamlit app
# -------------------------------
st.title("🔍 Index Matching Pairs Finder")

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
    # Matching Pairs
    # -------------------------------
    st.subheader("🔗 Matching Pairs")
    matching_pairs_df = filter_matching_pairs(df)

    if not matching_pairs_df.empty:
        st.dataframe(matching_pairs_df)

        # Download results
        csv = matching_pairs_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Matching Pairs (CSV)",
            data=csv,
            file_name="matching_pairs.csv",
            mime="text/csv"
        )
    else:
        st.info("✅ No matching pairs found with the given thresholds.")

  # -------------------------------
# Data Quality Checks
# -------------------------------
st.subheader("🧪 Data Quality Checks")

# Checks duplicati (solo colonne specifiche)
duplicated_cgf = df[df["CGF_ID"].duplicated(keep=False)]
duplicated_sample = df[df["Sample_ID"].duplicated(keep=False)]

# Controllo spazi o trattini in TUTTE le colonne
format_issues = {col: df[df[col].apply(has_space_or_hyphen)] for col in df.columns}

# Report summary
st.markdown(f"""
**Summary:**
- 🧬 Duplicated CGF_ID: **{len(duplicated_cgf)}**
- 🧪 Duplicated Sample_ID: **{len(duplicated_sample)}**
""")

for col, issues_df in format_issues.items():
    st.markdown(f"- ⚠️ {col} con spazi o trattini: **{len(issues_df)}**")

# Show tables if issues
if not duplicated_cgf.empty:
    st.warning("Duplicated CGF_IDs (full rows):")
    st.dataframe(duplicated_cgf)

if not duplicated_sample.empty:
    st.warning("Duplicated Sample_IDs (full rows):")
    st.dataframe(duplicated_sample)

for col, issues_df in format_issues.items():
    if not issues_df.empty:
        st.warning(f"{col} con spazi o trattini (full rows):")
        st.dataframe(issues_df)

    # -------------------------------
    # Lane-specific demultiplexing report
    # -------------------------------
    st.subheader("🧾 Demultiplexing Recommendations by Lane")

    for lane in df["Lane"].unique():
        lane_data = df[df["Lane"] == lane].reset_index(drop=True)

        status = "✅ Demultiplexing non stringente"
        note = []

        for i in range(len(lane_data)):
            for j in range(i + 1, len(lane_data)):
                str1 = str(lane_data.loc[i, "index7"])
                str2 = str(lane_data.loc[j, "index7"])
                matches = char_matches(str1, str2)
                mismatches = abs(len(str1) - matches)  # differenze sui caratteri

                if str1 == str2:
                    status = "❌ Errore: stessi indici presenti"
                    note.append(f"Samples {lane_data.loc[i,'Sample_ID']} and {lane_data.loc[j,'Sample_ID']} hanno lo stesso indice.")
                elif mismatches == 1 and status != "❌ Errore: stessi indici presenti":
                    status = "⚠️ Demultiplexing stringente"
                    note.append(f"Samples {lane_data.loc[i,'Sample_ID']} and {lane_data.loc[j,'Sample_ID']} hanno 1 mismatch.")

        st.markdown(f"**Lane {lane}:** {status}")
        if note:
            for n in note:
                st.markdown(f"- {n}")

else:
    st.info("👆 Upload an Excel file to start the analysis.")

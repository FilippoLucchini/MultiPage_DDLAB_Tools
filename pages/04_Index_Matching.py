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
def filter_matching_pairs(df, thresholds):
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

                # Threshold logic (configurable)
                match_threshold = thresholds.get(min_length, thresholds["default"])

                if matches >= match_threshold:
                    result.append({
                        "lane": lane,
                        "GCF_ID_string1": lane_data.loc[i, "CGF_ID"],
                        "GCF_ID_string2": lane_data.loc[j, "CGF_ID"],
                        "pool_catt_string1": lane_data.loc[i, "Pool_Cattura"],
                        "pool_catt_string2": lane_data.loc[j, "Pool_Cattura"],
                        "CGF_Pool_ID_string1": lane_data.loc[i, "CGF_Pool_ID"],
                        "CGF_Pool_ID_string2": lane_data.loc[j, "CGF_Pool_ID"],
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

# Sidebar
st.sidebar.header("⚙️ Index Accepted Mismatch Settings")

thresholds = {
    12: st.sidebar.number_input("Threshold for length 12", 1, 12, 11),
    10: st.sidebar.number_input("Threshold for length 10", 1, 10, 9),
    8: st.sidebar.number_input("Threshold for length 8", 1, 8, 7),
    "default": st.sidebar.number_input("Threshold for other lengths", 1, 12, 5)
}

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
    matching_pairs_df = filter_matching_pairs(df, thresholds)

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

    # Show tables if issues
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

    # Option to download all errors
    error_rows = pd.concat([duplicated_cgf, duplicated_sample, cgf_format_issues, sample_format_issues]).drop_duplicates()
    if not error_rows.empty:
        csv_errors = error_rows.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Error Rows (CSV)",
            data=csv_errors,
            file_name="error_rows.csv",
            mime="text/csv"
        )

else:
    st.info("👆 Upload an Excel file to start the analysis.")


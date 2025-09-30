import streamlit as st
import pandas as pd

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

                # Threshold logic
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
st.title("Index Matching Pairs Finder")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Add string length column like in R
    df["string_length"] = df["index7"].astype(str).str.len()

    st.subheader("Input Data Preview")
    st.dataframe(df.head())

    # Run matching function
    st.subheader("Matching Pairs")
    matching_pairs_df = filter_matching_pairs(df)

    if not matching_pairs_df.empty:
        st.dataframe(matching_pairs_df)

        # Option to download
        csv = matching_pairs_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="matching_pairs.csv",
            mime="text/csv"
        )
    else:
        st.info("No matching pairs found with the given thresholds.")


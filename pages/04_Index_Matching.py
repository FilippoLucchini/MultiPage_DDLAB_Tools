import streamlit as st
import pandas as pd

# -------------------------------
# Utility check function
# -------------------------------
def has_space_or_hyphen(value):
    if pd.isna(value):
        return False
    return (" " in str(value)) or ("-" in str(value))

# -------------------------------
# Character match function
# -------------------------------
def char_matches(str1, str2):
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
            for j in range(i + 1, len(lane_data)):
                str1 = str(lane_data.loc[i, "index7"])
                str2 = str(lane_data.loc[j, "index7"])
                len1 = len(str1)
                len2 = len(str2)

                matches = char_matches(str1, str2)
                min_length = min(len1, len2)

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
st.title("🔍 Index Matching Tool")

uploaded_file = st.file_uploader("📂 Upload Sequencing Sample List", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Rimuove spazi extra dai nomi delle colonne
    df.columns = df.columns.str.strip()

    # Controllo colonne richieste
    required_columns = ["Lane", "index7", "CGF_ID", "Sample_ID", "Pool_Cattura", "CGF_Pool_ID"]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        st.error(f"❌ Missing required columns in file: {', '.join(missing_cols)}")
        st.stop()

    # Aggiunge info utili
    df["Excel_Row"] = df.index + 2  
    df["string_length"] = df["index7"].astype(str).str.len()

    # Preview input
    st.subheader("📊 Input Data Preview")
    st.dataframe(df.head())

    # -------------------------------
    # Matching Pairs
    # -------------------------------
    st.subheader("🔗 Matching Pairs")
    matching_pairs_df = filter_matching_pairs(df)

    if not matching_pairs_df.empty:
        st.dataframe(matching_pairs_df)

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

    duplicated_cgf = df[df["CGF_ID"].duplicated(keep=False)]
    duplicated_sample = df[df["Sample_ID"].duplicated(keep=False)]

    total_format_issues = sum(df[col].apply(has_space_or_hyphen).sum() for col in df.columns)

    st.markdown(f"""
    **Summary:**
    - 🧬 ID CGF Duplicati: **{len(duplicated_cgf)}**
    - 🧪 Sample ID Duplicati: **{len(duplicated_sample)}**
    - ⚠️ Celle con spazi o trattini: **{total_format_issues}**
    """)

    if not duplicated_cgf.empty:
        st.warning("Duplicated CGF_IDs (full rows):")
        st.dataframe(duplicated_cgf)

    if not duplicated_sample.empty:
        st.warning("Duplicated Sample_IDs (full rows):")
        st.dataframe(duplicated_sample)

    if total_format_issues > 0:
        st.warning("Alcune celle contengono spazi o trattini (vedi DataFrame completo):")
        format_issues_df = df[df.apply(lambda row: any(has_space_or_hyphen(row[col]) for col in df.columns), axis=1)]
        st.dataframe(format_issues_df)

    # -------------------------------
    # Lane-specific demultiplexing report
    # -------------------------------
    st.subheader("🧾 Demultiplexing Recommendations by Lane")

    for lane in df["Lane"].unique():
        lane_data = df[df["Lane"] == lane].reset_index(drop=True)

        # Lunghezze indici index7/index5
        index7_lengths = lane_data["index7"].astype(str).str.len()
        index5_lengths = lane_data["index5"].astype(str).str.len() if "index5" in lane_data.columns else pd.Series(dtype=int)

        length_summary_dict = {}
        all_lengths = sorted(set(index7_lengths.tolist() + index5_lengths.tolist()))
        for length in all_lengths:
            in_index7 = sum(index7_lengths == length)
            in_index5 = sum(index5_lengths == length)
            if in_index5 > 0:
                length_summary_dict[length] = f"2x{length}"
            else:
                length_summary_dict[length] = f"1x{length}"

        length_summary = ", ".join(length_summary_dict.values())

        status = "✅ Demultiplexing non stringente"
        note = []

        for i in range(len(lane_data)):
            for j in range(i + 1, len(lane_data)):
                str1 = str(lane_data.loc[i, "index7"])
                str2 = str(lane_data.loc[j, "index7"])
                matches = char_matches(str1, str2)
                mismatches = abs(len(str1) - matches)

                if str1 == str2:
                    status = "❌ Errore: stessi indici presenti"
                    note.append(f"Samples {lane_data.loc[i,'Sample_ID']} and {lane_data.loc[j,'Sample_ID']} hanno lo stesso indice.")
                elif mismatches == 1 and status != "❌ Errore: stessi indici presenti":
                    status = "⚠️ Demultiplexing stringente"
                    note.append(f"Samples {lane_data.loc[i,'Sample_ID']} and {lane_data.loc[j,'Sample_ID']} hanno 1 mismatch.")

        st.markdown(f"**Lane {lane}:** {status}  |  **Index lengths:** {length_summary}")
        if note:
            for n in note:
                st.markdown(f"- {n}")

else:
    st.info("👆 Upload an Excel file to start the analysis.")

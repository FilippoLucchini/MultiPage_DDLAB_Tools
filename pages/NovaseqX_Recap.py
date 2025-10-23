import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(layout="wide", page_title="NovaSeqX - Statistiche Librerie")

@st.cache_data
def load_data(path):
    return pd.read_excel(path)

# --- Caricamento dati ---
st.title("NovaSeqX Riassunto Totale")
uploaded = st.file_uploader("Carica il file Excel (predefinito incluso)", type=["xlsx", "xls"])
default_path = "NovaSeqX_Sequenziamento_Riassunto_Totale.xlsx"
df = pd.read_excel(uploaded) if uploaded else load_data(default_path)
df.columns = df.columns.str.strip()

if df.empty:
    st.error("Il file caricato è vuoto o non contiene dati validi.")
    st.stop()

# --- Selezione colonna libreria + ordinamento ---
allowed_library_cols = [c for c in df.columns if c in ['Type', 'Library_Kit', 'Capture_Kit', 'Pool']]
if not allowed_library_cols:
    st.error("Nessuna delle colonne 'Type', 'Library_Kit', 'Capture_Kit', 'Pool' è presente nel file.")
    st.stop()

col_filt, col_sort = st.columns([1, 1])
with col_filt:
    library_col = st.selectbox("Colonna che contiene il tipo di libreria", allowed_library_cols)
    library_values = sorted(df[library_col].dropna().unique().tolist())
    chosen_library = st.selectbox("Scegli il tipo di libreria da analizzare", library_values)

with col_sort:
    sort_options = ["Pool", "Lane", "Conc_caricamento_1x (pM) (median)"]
    sort_by = st.selectbox("Ordina la tabella per", sort_options)
    sort_ascending = st.radio("Ordine", ["Crescente", "Decrescente"]) == "Crescente"
    aggiorna = st.button("🔄 Applica ordinamento")

# --- Colonne statistiche ---
def safe_median(series):
    vals = pd.to_numeric(series, errors='coerce').dropna()
    return float(np.nanmedian(vals)) if not vals.empty else np.nan

columns_map = {
    'RT/Tape': 'RT/Tape_Ratio',
    'RT/Qubit': 'RT/Qubit_Ratio',
    'Conc 1x': 'Conc_caricamento_1x (pM)',
    '% Library Lane': '%_Library_Lane',
    'Fragments Produced': '#fragments Produced sample',
    'Fragments Assigned': '#fragments Assigned_sample'
}
missing = [label for label, col in columns_map.items() if col not in df.columns]
if missing:
    st.warning(f"Mancano alcune colonne: {missing}. Le statistiche correlate non saranno calcolate.")

# --- Costruzione tabella dettagliata ---
groups = []
by = df.groupby(['Pool', 'Lane'])
for (pool, lane), grp in by:
    for libtype, subgrp in grp.groupby(library_col):
        entry = {
            "Pool": pool,
            "Lane": lane,
            "Library_Type": libtype,
            "n_samples": len(subgrp),
            "%_Library_Lane (median)": safe_median(subgrp.get(columns_map['% Library Lane'], np.nan)),
            "RT/Tape_Ratio(median)": safe_median(subgrp.get(columns_map['RT/Tape'], np.nan)),
            "RT/Qubit_Ratio(median)": safe_median(subgrp.get(columns_map['RT/Qubit'], np.nan)),
            "Conc_caricamento_1x (pM) (median)": safe_median(subgrp.get(columns_map['Conc 1x'], np.nan))
        }

        # Altri tipi nella stessa Lane
        other_libs = grp[grp[library_col] != libtype]
        if not other_libs.empty and columns_map['% Library Lane'] in df.columns:
            lib_summaries = []
            for other_type, other_grp in other_libs.groupby(library_col):
                median_pct = safe_median(other_grp[columns_map['% Library Lane']])
                lib_summaries.append(f"{other_type}: {median_pct:.2f}%")
            entry["Altri tipi nella stessa Lane (%_Library_Lane)"] = "; ".join(lib_summaries)
        else:
            entry["Altri tipi nella stessa Lane (%_Library_Lane)"] = ""

        # Fragments ratio
        if columns_map['Fragments Produced'] in df.columns and columns_map['Fragments Assigned'] in df.columns:
            produced = pd.to_numeric(subgrp[columns_map['Fragments Produced']], errors='coerce').fillna(0).sum()
            assigned = pd.to_numeric(subgrp[columns_map['Fragments Assigned']], errors='coerce').fillna(0).sum()
            entry['Fragments_Produced_vs_Assigned_percent'] = (produced / assigned * 100.0) if assigned > 0 else np.nan
        else:
            entry['Fragments_Produced_vs_Assigned_percent'] = np.nan

        groups.append(entry)

result_df = pd.DataFrame(groups)

# --- Filtro e visualizzazione tabella filtrata ---
if aggiorna:
    result_df_filtered = result_df[result_df["Library_Type"] == chosen_library]
    result_df_filtered = result_df_filtered.sort_values(by=sort_by, ascending=sort_ascending)

    st.markdown("### Statistiche dettagliate per Pool + Lane per il tipo selezionato")
    st.markdown("""
        <style>
            .compact-table td, .compact-table th {
                padding: 4px 8px;
                font-size: 13px;
                white-space: nowrap;
            }
            .compact-table {
                overflow-x: auto;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(result_df_filtered.to_html(classes='compact-table', index=False), unsafe_allow_html=True)

    st.download_button(
        "Scarica le statistiche filtrate (CSV)",
        data=result_df_filtered.to_csv(index=False).encode('utf-8'),
        file_name='library_stats_filtrate.csv'
    )

# --- Grafico a torta basato su result_df_filtered ---
if aggiorna and not result_df_filtered.empty:
    exploded = []
    for _, row in result_df_filtered.iterrows():
        pool = row['Pool']
        lane = row['Lane']
        selected_pct = row['%_Library_Lane (median)']
        exploded.append({
            'Pool': pool,
            'Lane': lane,
            'Library': row['Library_Type'],
            'Median_%': selected_pct
        })
        summary = row.get('Altri tipi nella stessa Lane (%_Library_Lane)', '')
        if summary:
            for part in summary.split(';'):
                if ':' in part:
                    libtype, pct = part.split(':')
                    try:
                        exploded.append({
                            'Pool': pool,
                            'Lane': lane,
                            'Library': libtype.strip(),
                            'Median_%': float(pct.strip().replace('%',''))
                        })
                    except:
                        continue

    df_exploded = pd.DataFrame(exploded)

    if not df_exploded.empty:
        st.header("Grafico a torta per Pool + Lane")
        col1, col2 = st.columns([1, 1])
        with col1:
            lane_options = df_exploded[['Pool', 'Lane']].drop_duplicates()
            selected_row = st.selectbox(
                "Seleziona Pool + Lane",
                lane_options.itertuples(index=False),
                format_func=lambda x: f"{x.Pool} - Lane {x.Lane}"
            )

            filtered = df_exploded[
                (df_exploded['Pool'] == selected_row.Pool) &
                (df_exploded['Lane'] == selected_row.Lane)
            ]

            if not filtered.empty:
                chart = alt.Chart(filtered).mark_arc().encode(
                    theta=alt.Theta(field="Median_%", type="quantitative"),
                    color=alt.Color(field="Library", type="nominal"),
                    tooltip=['Library', 'Median_%']
                ).properties(
                    title=f'Distribuzione % tipi di libreria — Pool {selected_row.Pool}, Lane {selected_row.Lane}'
                )
                st.altair_chart(chart, use_container_width=True

st.markdown("---")
st.caption("Script generato automaticamente — adattalo se le intestazioni delle colonne nel tuo file differiscono da quelle usate qui.")

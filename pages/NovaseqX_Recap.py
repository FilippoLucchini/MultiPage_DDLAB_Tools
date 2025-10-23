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

orig_columns = list(df.columns)

# --- Selezione colonna libreria + ordinamento ---
allowed_library_cols = [c for c in orig_columns if c in ['Type', 'Library_Kit', 'Capture_Kit', 'Pool']]
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

col_rt_tape = 'RT/Tape_Ratio' if 'RT/Tape_Ratio' in orig_columns else None
col_rt_qubit = 'RT/Qubit_Ratio' if 'RT/Qubit_Ratio' in orig_columns else None
col_conc_1x = 'Conc_caricamento_1x (pM)' if 'Conc_caricamento_1x (pM)' in orig_columns else None
col_pct_lib_lane = '%_Library_Lane' if '%_Library_Lane' in orig_columns else None
col_frag_prod = '#fragments Produced sample' if '#fragments Produced sample' in orig_columns else None
col_frag_assigned = '#fragments Assigned_sample' if '#fragments Assigned_sample' in orig_columns else None
col_pool = 'Pool'
col_lane = 'Lane'

missing = [name for name, col in [('RT/Tape', col_rt_tape), ('RT/Qubit', col_rt_qubit), ('Conc 1x', col_conc_1x), ('% Library Lane', col_pct_lib_lane), ('#fragments Produced sample', col_frag_prod), ('#fragments Assigned_sample', col_frag_assigned)] if col is None]
if missing:
    st.warning(f"Attenzione: mancano alcune colonne necessarie per tutte le statistiche: {missing}. Le statistiche correlate non saranno calcolate.")

# --- Costruzione tabella dettagliata ---
groups = []
by = df.groupby([col_pool, col_lane])
for (pool, lane), grp in by:
    for libtype, subgrp in grp.groupby(library_col):
        entry = {
            "Pool": pool,
            "Lane": lane,
            "Library_Type": libtype,
            "n_samples": len(subgrp),
            "%_Library_Lane (median)": safe_median(subgrp[col_pct_lib_lane]) if col_pct_lib_lane else np.nan,
            "RT/Tape_Ratio(median)": safe_median(subgrp[col_rt_tape]) if col_rt_tape else np.nan,
            "RT/Qubit_Ratio(median)": safe_median(subgrp[col_rt_qubit]) if col_rt_qubit else np.nan,
            "Conc_caricamento_1x (pM) (median)": safe_median(subgrp[col_conc_1x]) if col_conc_1x else np.nan
        }

        # Altri tipi nella stessa Lane
        other_libs = grp[grp[library_col] != libtype]
        if not other_libs.empty and col_pct_lib_lane:
            lib_summaries = []
            for other_type, other_grp in other_libs.groupby(library_col):
                median_pct = safe_median(other_grp[col_pct_lib_lane])
                lib_summaries.append(f"{other_type}: {median_pct:.2f}%")
            entry["Altri tipi nella stessa Lane (%_Library_Lane)"] = "; ".join(lib_summaries)
        else:
            entry["Altri tipi nella stessa Lane (%_Library_Lane)"] = ""

        if col_frag_prod and col_frag_assigned:
            produced = pd.to_numeric(subgrp[col_frag_prod], errors='coerce').fillna(0).sum()
            assigned = pd.to_numeric(subgrp[col_frag_assigned], errors='coerce').fillna(0).sum()
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

    # Tabella compatta con larghezza adattiva
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

    # --- Grafico a torta Altair ---
    st.header("3) Grafico a torta per Pool + Lane")

    col1, col2 = st.columns([1, 1])

    with col1:
        lane_options = result_df_filtered[['Pool', 'Lane']].drop_duplicates()
        selected_row = st.selectbox(
            "Seleziona Pool + Lane",
            lane_options.itertuples(index=False),
            format_func=lambda x: f"{x.Pool} - Lane {x.Lane}"
        )

        filtered = result_df_filtered[
            (result_df_filtered['Pool'] == selected_row.Pool) &
            (result_df_filtered['Lane'] == selected_row.Lane)
        ].copy()

        # Ripulisci tooltip per evitare errori
        filtered["Altri tipi nella stessa Lane (%_Library_Lane)"] = (
            filtered["Altri tipi nella stessa Lane (%_Library_Lane)"]
            .fillna("")
            .astype(str)
        )

        if filtered.empty:
            st.warning("Nessun dato disponibile per questa combinazione Pool + Lane.")
        else:
            chart = alt.Chart(filtered).mark_arc().encode(
                theta=alt.Theta(field="%_Library_Lane (median)", type="quantitative"),
                color=alt.Color(field="Library_Type", type="nominal"),
                tooltip=[
                    'Library_Type',
                    '%_Library_Lane (median)',
                    'Altri tipi nella stessa Lane (%_Library_Lane)'
                ]
            ).properties(
                title=f'Distribuzione % tipi di libreria — Pool {selected_row.Pool}, Lane {selected_row.Lane}'
            )

            st.altair_chart(chart, use_container_width=True)

    with col2:
        st.empty()

st.markdown("---")
st.caption("Script generato automaticamente — adattalo se le intestazioni delle colonne nel tuo file differiscono da quelle usate qui.")

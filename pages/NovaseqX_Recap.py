import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import altair as alt

st.set_page_config(layout="wide", page_title="NovaSeq - Filter & Library Stats")

@st.cache_data
def load_data(path):
    return pd.read_excel(path)

# --- Load data ---
st.title("NovaSeq: filtro righe e statistiche per tipo di libreria")

uploaded = st.file_uploader("Carica il file Excel (predefinito incluso)", type=["xlsx", "xls"])
default_path = "NovaSeqX_Sequenziamento_Riassunto_Totale.xlsx"
if uploaded is not None:
    df = pd.read_excel(uploaded)
else:
    df = load_data(default_path)

df.columns = df.columns.str.strip()

if df.empty:
    st.error("Il file caricato è vuoto o non contiene dati validi.")
    st.stop()

orig_columns = list(df.columns)
st.sidebar.header("Colonne trovate")
st.sidebar.write(orig_columns)

# --- SECTION 2: Library grouping & statistics ---
st.header("2) Statistiche raggruppate per tipo di libreria, pool e lane")
st.markdown("Seleziona la colonna che identifica il tipo di libreria e il tipo specifico (es. 'Type' o 'Library_Kit'). Il codice raggrupperà per Pool e Lane.")

def safe_median(series):
    vals = pd.to_numeric(series, errors='coerce').dropna()
    return float(np.nanmedian(vals)) if not vals.empty else np.nan

lib_type_col_default = 'Type' if 'Type' in orig_columns else orig_columns[0]
library_col = st.selectbox("Colonna che contiene il tipo di libreria", orig_columns, index=orig_columns.index(lib_type_col_default))
library_values = sorted(df[library_col].dropna().unique().tolist())
chosen_library = st.selectbox("Scegli il tipo di libreria da analizzare", library_values)

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

df_lib = df[df[library_col] == chosen_library].copy()
if df_lib.empty:
    st.info("Nessun campione trovato per il tipo di libreria selezionato.")
else:
    groups = []
    by = df_lib.groupby([col_pool, col_lane])
    for (pool, lane), grp in by:
        entry = {
            "Pool": pool,
            "Lane": lane,
            "n_samples": len(grp),
            "RT/Tape_Ratio(median)": safe_median(grp[col_rt_tape]) if col_rt_tape else np.nan,
            "RT/Qubit_Ratio(median)": safe_median(grp[col_rt_qubit]) if col_rt_qubit else np.nan,
            "Conc_caricamento_1x (pM) (median)": safe_median(grp[col_conc_1x]) if col_conc_1x else np.nan,
            "%_Library_Lane (median)": safe_median(grp[col_pct_lib_lane]) if col_pct_lib_lane else np.nan
        }

        others = df[(df[col_pool] == pool) & (df[col_lane] == lane) & (df[library_col] != chosen_library)]
        other_summary = ""
        if not others.empty and col_pct_lib_lane:
            lib_summaries = []
            for libtype, sec in others.groupby(library_col):
                median_pct = safe_median(sec[col_pct_lib_lane])
                lib_summaries.append(f"{libtype}: {median_pct:.2f}%")
            other_summary = "; ".join(lib_summaries)
        entry["Altri tipi di libreria (mediana %_Library_Lane)"] = other_summary

        if col_frag_prod and col_frag_assigned:
            produced = pd.to_numeric(grp[col_frag_prod], errors='coerce').fillna(0).sum()
            assigned = pd.to_numeric(grp[col_frag_assigned], errors='coerce').fillna(0).sum()
            entry['Fragments_Produced_vs_Assigned_percent'] = (produced / assigned * 100.0) if assigned > 0 else np.nan
        else:
            entry['Fragments_Produced_vs_Assigned_percent'] = np.nan

        groups.append(entry)

    result_df = pd.DataFrame(groups).sort_values(by=["Pool", "Lane"])
    st.markdown("### Statistiche per pool & lane (mediane e riassunti)")
    st.dataframe(result_df)
    st.download_button("Scarica le statistiche (CSV)", data=result_df.to_csv(index=False).encode('utf-8'), file_name='library_stats.csv')

# Grafico Altair
# Esplodi la colonna 'Altri tipi di libreria (mediana %_Library_Lane)' in righe separate
exploded = []
for _, row in result_df.iterrows():
    pool = row['Pool']
    lane = row['Lane']
    summary = row['Altri tipi di libreria (mediana %_Library_Lane)']
    if summary:
        for part in summary.split(';'):
            if ':' in part:
                libtype, pct = part.split(':')
                exploded.append({
                    'Pool': pool,
                    'Lane': lane,
                    'Library': libtype.strip(),
                    'Median_%': float(pct.strip().replace('%',''))
                })

df_exploded = pd.DataFrame(exploded)

# Crea il grafico a barre impilate
chart = alt.Chart(df_exploded).mark_bar().encode(
    x=alt.X('Pool:N', title='Pool'),
    y=alt.Y('Median_%:Q', title='Mediana % Library Lane'),
    color=alt.Color('Library:N', title='Tipo di libreria'),
    column=alt.Column('Lane:N', title='Lane'),
    tooltip=['Pool', 'Lane', 'Library', 'Median_%']
).properties(
    title='Distribuzione altri tipi di libreria per Pool e Lane'
)

st.altair_chart(chart, use_container_width=True)

st.markdown("---")
st.caption("Script generato automaticamente — adattalo se le intestazioni delle colonne nel tuo file differiscono da quelle usate qui.")


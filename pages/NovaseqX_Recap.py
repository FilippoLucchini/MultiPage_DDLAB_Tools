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
st.title("NovaseqX Riassunto Totale")
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

# --- SECTION 2: Library grouping & statistics ---
st.markdown("Seleziona la colonna che identifica il tipo di libreria e il tipo specifico (es. 'Type' o 'Library_Kit'). Il codice raggrupperà per Pool e Lane.")

def safe_median(series):
    vals = pd.to_numeric(series, errors='coerce').dropna()
    return float(np.nanmedian(vals)) if not vals.empty else np.nan

lib_type_col_default = 'Library_Kit' if 'Library_Kit' in orig_columns else orig_columns[0]
allowed_library_cols = [c for c in orig_columns if c in ['Type', 'Library_Kit']]
if not allowed_library_cols:
    st.error("Nessuna delle colonne 'Type', 'Library_Kit' è presente nel file.")
    st.stop()

library_col = st.selectbox("Colonna che contiene il tipo di libreria", allowed_library_cols)
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
            entry['% Production'] = (produced / assigned * 100.0) if assigned > 0 else np.nan
        else:
            entry['% Production'] = np.nan

        groups.append(entry)

    result_df = pd.DataFrame(groups).sort_values(by=["Pool", "Lane"])
    st.markdown("### Statistiche per pool & lane (mediane e riassunti)")
    st.dataframe(result_df)
    st.download_button("Scarica le statistiche (CSV)", data=result_df.to_csv(index=False).encode('utf-8'), file_name='library_stats.csv')

# Grafico Altair

# Prepara i dati esplosi
exploded = []
for _, row in result_df.iterrows():
    pool = row['Pool']
    lane = row['Lane']
    selected_pct = row['%_Library_Lane (median)']
    selected_type = chosen_library
    exploded.append({
        'Pool': pool,
        'Lane': lane,
        'Library': selected_type,
        'Median_%': selected_pct
    })
    summary = row['Altri tipi di libreria (mediana %_Library_Lane)']
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

# Verifica che ci siano dati
if df_exploded.empty:
    st.warning("Nessun dato disponibile per il grafico a torta.")
else:
    st.header("3) Grafico a torta per Pool + Lane")

    col1, col2 = st.columns([1, 1])  # Layout a due colonne

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

        if filtered.empty:
            st.warning("Nessun dato disponibile per questa combinazione Pool + Lane.")
        else:
            chart = alt.Chart(filtered).mark_arc().encode(
                theta=alt.Theta(field="Median_%", type="quantitative"),
                color=alt.Color(field="Library", type="nominal"),
                tooltip=['Library', 'Median_%']
            ).properties(
                title=f'Distribuzione % tipi di libreria — Pool {selected_row.Pool}, Lane {selected_row.Lane}'
            )

            st.altair_chart(chart, use_container_width=True)

    with col2:
        st.empty()


st.markdown("---")
st.caption("Script generato automaticamente — adattalo se le intestazioni delle colonne nel tuo file differiscono da quelle usate qui.")


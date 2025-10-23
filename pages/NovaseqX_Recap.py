import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

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

# --- SECTION 1: Filtering ---
st.header("1) Filtra i dati")
st.markdown("Scegli la colonna del primo filtro (obbligatorio). Poi puoi aggiungere altri filtri che dipendono dal filtro precedente.")

if 'filters' not in st.session_state:
    st.session_state.filters = []

cols = orig_columns
first_col = st.selectbox("Prima colonna di filtro (obbligatoria)", cols, key="first_col")

if first_col and first_col in df.columns:
    if df[first_col].dropna().empty:
        st.warning(f"La colonna '{first_col}' non contiene valori validi.")
        first_values = []
    else:
        first_values = sorted(df[first_col].dropna().unique().tolist())
else:
    st.warning("La colonna selezionata non è valida o non è presente nel file.")
    first_values = []

first_selected = st.multiselect(
    f"Valori per '{first_col}' (seleziona almeno uno)",
    first_values,
    key="first_sel"
) if first_values else []

if 'first_selected_prev' not in st.session_state or st.session_state.first_selected_prev != tuple(first_selected):
    st.session_state.filters = []
    st.session_state.first_selected_prev = tuple(first_selected)

cols_available = [c for c in cols if c != first_col]
add_col_btn = st.button("Aggiungi filtro dipendente")
if add_col_btn:
    st.session_state.filters.append({'col': None, 'vals': []})

for i, f in enumerate(st.session_state.filters):
    with st.expander(f"Filtro aggiuntivo #{i+1}", expanded=True):
        col_choice = st.selectbox(f"Colonna (filtro #{i+1})", options=[None] + cols_available, key=f"col_{i}")
        st.session_state.filters[i]['col'] = col_choice
        df_tmp = df.copy()
        if first_selected:
            df_tmp = df_tmp[df_tmp[first_col].isin(first_selected)]
        for j in range(i):
            colj = st.session_state.filters[j].get('col')
            valsj = st.session_state.filters[j].get('vals', [])
            if colj and valsj:
                df_tmp = df_tmp[df_tmp[colj].isin(valsj)]
        if col_choice:
            available_vals = sorted(df_tmp[col_choice].dropna().unique().tolist())
            vals_selected = st.multiselect(f"Valori per '{col_choice}'", available_vals, key=f"vals_{i}")
            st.session_state.filters[i]['vals'] = vals_selected
        if st.button("Rimuovi questo filtro", key=f"rem_{i}"):
            st.session_state.filters.pop(i)
            st.rerun()

if not first_selected:
    st.warning("Seleziona almeno un valore per il primo filtro per vedere i risultati.")
else:
    df_filtered = df[df[first_col].isin(first_selected)].copy()
    for f in st.session_state.filters:
        col = f.get('col')
        vals = f.get('vals', [])
        if col and vals:
            df_filtered = df_filtered[df_filtered[col].isin(vals)]

    st.markdown(f"### Risultato: {len(df_filtered)} righe corrispondenti ai filtri")
    st.dataframe(df_filtered)
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("Scarica CSV dei risultati", data=csv, file_name="filtered_results.csv")

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
col_frag_assigned = '#fragments Assigned_sample ' if '#fragments Assigned_sample ' in orig_columns else None
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
            "%_Library_Lane (median)": safe_median(grp[col_pct_lib_lane]) if col_pct_lib_lane else np.nan,
            "Fragments_Produced_vs_Assigned_percent": (
                grp[col_frag_prod].replace({np.nan: 0}).sum() / grp[col_frag_assigned].replace({np.nan: 0}).sum() * 100.0
                if col_frag_prod and col_frag_assigned and grp[col_frag_assigned].replace({np.nan: 0}).sum() > 0
                else np.nan
            )
        }

        others = df[
            (df[col_pool] == pool) &
            (df[col_lane] == lane) &
            (df[library_col] != chosen_library)
        ]
        other_summary = ""
        if not others.empty and col_pct_lib_lane:
            lib_summaries = []
            for libtype, sec in others.groupby(library_col):
                median_pct = safe_median(sec[col_pct_lib_lane])
                lib_summaries.append(f"{libtype}: {median_pct:.2f}%")
            other_summary = "; ".join(lib_summaries)
        entry["Altri tipi di libreria (mediana %_Library_Lane)"] = other_summary

        groups.append(entry)

    result_df = pd.DataFrame(groups).sort_values(by=["Pool", "Lane"])
    st.markdown("### Statistiche per pool & lane (mediane e riassunti)")
    st.dataframe(result_df)
    st.download_button(
        "Scarica le statistiche (CSV)",
        data=result_df.to_csv(index=False).encode('utf-8'),
        file_name='library_stats.csv'
    )

st.markdown("---")
st.caption("Script generato automaticamente — adattalo se le intestazioni delle colonne nel tuo file differiscono da quelle usate qui.")


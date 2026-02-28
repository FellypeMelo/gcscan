import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import os
from Bio import SeqIO
from src.domain.analysis import calculate_gc_percentage, calculate_sliding_window, detect_cpg_islands
from src.domain.statistics import calculate_descriptive_stats
from src.infrastructure.plotting.adapters import plot_gc_distribution

def render_sidebar():
    """Renderiza a barra lateral e retorna as configurações."""
    with st.sidebar:
        st.header("📂 Entrada de Dados")
        files = st.file_uploader("Escolha arquivos FASTA", type=['fasta', 'fa', 'fna'], accept_multiple_files=True)
        st.divider()
        st.header("⚙️ Opções de Análise")
        do_sw = st.checkbox("Análise de Janela Deslizante", value=False)
        w, s = 100, 50
        if do_sw:
            w = st.number_input("Janela (bp)", min_value=10, value=100)
            s = st.number_input("Passo (bp)", min_value=1, value=50)
        do_cpg = st.checkbox("Detecção de Ilhas CpG", value=False)
    return files, do_sw, w, s, do_cpg

def process_uploads(uploaded_files, do_sw, win_size, step_size, do_cpg):
    """Processa arquivos carregados."""
    results, sw_res, cpg_res = {}, {}, {}
    prog = st.progress(0)
    for i, up in enumerate(uploaded_files):
        # Usando processamento em memória para evitar arquivos temporários se possível, 
        # mas Biopython SeqIO.parse prefere handle ou path.
        from io import StringIO
        stringio = StringIO(up.getvalue().decode("utf-8"))
        for record in SeqIO.parse(stringio, "fasta"):
            uid = f"{up.name}::{record.id}" if len(uploaded_files) > 1 else record.id
            results[uid] = calculate_gc_percentage(str(record.seq))
            if do_sw: sw_res[uid] = calculate_sliding_window(str(record.seq), win_size, step_size)
            if do_cpg: cpg_res[uid] = detect_cpg_islands(str(record.seq))
        prog.progress((i + 1) / len(uploaded_files))
    prog.empty()
    return results, sw_res, cpg_res

def render_main_dashboard(results, sw_res, cpg_res, sw_params):
    """Renderiza o dashboard principal."""
    stats = calculate_descriptive_stats(list(results.values()))
    _render_kpis(stats)
    st.divider()
    
    tabs = st.tabs(["📈 Visão Geral", "🔍 Individual", "🧬 Avançada", "📄 Dados Brutos"])
    with tabs[0]: _render_overview_tab(results, stats)
    with tabs[1]: _render_details_tab(results)
    with tabs[2]: _render_advanced_tab(sw_res, cpg_res, sw_params)
    with tabs[3]: _render_raw_tab(results)

def _render_kpis(stats):
    st.subheader("📊 Relatório de Estatísticas")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total", f"{int(stats['count'])}")
    k2.metric("Média GC", f"{stats['mean']:.2f}%")
    k3.metric("Desvio Padrão", f"± {stats['std_dev']:.2f}")
    k4.metric("Mediana GC", f"{stats['median']:.2f}%")

def _render_overview_tab(results, stats):
    fig, ax = plt.subplots(figsize=(10, 5))
    from src.infrastructure.plotting.adapters import _plot_bar_chart, _plot_histogram, _setup_bar_chart, _setup_histogram
    if stats['count'] < 20:
        _setup_bar_chart(ax, int(stats['count']))
        _plot_bar_chart(results, ax)
    else:
        _setup_histogram(ax, int(stats['count']))
        _plot_histogram(results, ax, stats)
    st.pyplot(fig)
    plt.close(fig)

def _render_details_tab(results):
    df = pd.DataFrame(list(results.items()), columns=['ID', 'GC (%)'])
    c1, c2 = st.columns(2)
    min_v = c1.slider("Mínimo %", 0.0, 100.0, 0.0)
    max_v = c2.slider("Máximo %", 0.0, 100.0, 100.0)
    filtered = df[(df['GC (%)'] >= min_v) & (df['GC (%)'] <= max_v)]
    st.dataframe(filtered.style.format({'GC (%)': '{:.2f}'}), use_container_width=True)

def _render_advanced_tab(sw_res, cpg_res, sw_params):
    if not (sw_res or cpg_res):
        st.warning("Habilite análises avançadas na barra lateral.")
        return
    if sw_res:
        st.subheader("🪟 Janela Deslizante")
        sel = st.selectbox("Sequência", list(sw_res.keys()))
        step = sw_params['step']
        sw_df = pd.DataFrame({'Posição': [i*step for i in range(len(sw_res[sel]))], 'GC': sw_res[sel]})
        chart = alt.Chart(sw_df).mark_line().encode(x='Posição', y=alt.Y('GC', scale=alt.Scale(domain=[0, 100])))
        st.altair_chart(chart, use_container_width=True)
    if cpg_res:
        st.subheader("🏝️ Ilhas CpG")
        for sid, isls in cpg_res.items():
            with st.expander(sid):
                data = [[i.start, i.end, i.gc_percent, i.oe_ratio] for i in isls]
                st.table(pd.DataFrame(data, columns=['Início', 'Fim', 'GC %', 'O/E']))

def _render_raw_tab(results):
    df = pd.DataFrame(list(results.items()), columns=['ID', 'GC (%)'])
    st.download_button("📥 Baixar CSV", df.to_csv(index=False).encode('utf-8'), "results.csv", "text/csv")

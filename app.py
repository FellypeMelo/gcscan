"""
GCScan Web Interface

Propósito: Interface web profissional para análise de conteúdo GC utilizando Streamlit.
Funcionalidades:
- Upload de arquivos FASTA
- Dashboard com KPIs (Média, Desvio Padrão)
- Visualização adaptativa (Histograma vs Barras)
- Análise Avançada (Sliding Window, CpG Islands)
- Exportação de dados
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from Bio import SeqIO
from main import (
    calculate_gc_content, 
    calculate_statistics, 
    plot_histogram, 
    plot_bar_chart,
    calculate_sliding_window_gc,
    detect_cpg_islands
)

# Configuração da página
st.set_page_config(
    page_title="GCScan - Analisador Genético Profissional",
    page_icon="🧬",
    layout="wide"
)

def render_sidebar():
    """Renderiza a barra lateral e retorna as configurações do usuário."""
    with st.sidebar:
        st.header("📂 Entrada de Dados")
        uploaded_files = st.file_uploader(
            "Escolha arquivos FASTA", 
            type=['fasta', 'fa', 'fna'], 
            accept_multiple_files=True
        )
        st.info("Suporte a multi-arquivos e análise em lote.")
        st.divider()
        st.header("⚙️ Opções de Análise")
        do_sliding_window = st.checkbox("Análise de Janela Deslizante", value=False)
        win_size, step_size = 100, 50
        if do_sliding_window:
            win_size = st.number_input("Tamanho da Janela (bp)", min_value=10, max_value=10000, value=100)
            step_size = st.number_input("Tamanho do Passo (bp)", min_value=1, max_value=10000, value=50)
        do_cpg = st.checkbox("Detecção de Ilhas CpG", value=False)
        st.divider()
        st.markdown("Desenvolvido por **GCScan Team**")
    return uploaded_files, do_sliding_window, win_size, step_size, do_cpg

def process_files(uploaded_files, do_sw, win_size, step_size, do_cpg):
    """Processa os arquivos carregados e realiza as análises solicitadas."""
    all_results = {}
    all_sw_results = {}
    all_cpg_results = {}
    
    progress_bar = st.progress(0)
    for i, uploaded_file in enumerate(uploaded_files):
        try:
            temp_filename = f"temp_{uploaded_file.name}"
            with open(temp_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Análises
            file_gc = calculate_gc_content(temp_filename)
            for seq_id, gc in file_gc.items():
                unique_id = f"{uploaded_file.name}::{seq_id}" if len(uploaded_files) > 1 else seq_id
                all_results[unique_id] = gc
            
            for record in SeqIO.parse(temp_filename, "fasta"):
                unique_id = f"{uploaded_file.name}::{record.id}" if len(uploaded_files) > 1 else record.id
                if do_sw:
                    all_sw_results[unique_id] = calculate_sliding_window_gc(record.seq, win_size, step_size)
                if do_cpg:
                    islands = detect_cpg_islands(record.seq)
                    if islands: all_cpg_results[unique_id] = islands
            
            os.remove(temp_filename)
        except Exception as e:
            st.error(f"Erro ao processar {uploaded_file.name}: {e}")
        progress_bar.progress((i + 1) / len(uploaded_files))
    progress_bar.empty()
    return all_results, all_sw_results, all_cpg_results

def render_dashboard(all_results, all_sw_results, all_cpg_results, do_sw, win_size, step_size, do_cpg):
    """Renderiza o dashboard principal com resultados e gráficos."""
    stats = calculate_statistics(all_results)
    st.subheader("📊 Relatório de Estatísticas")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total", f"{int(stats['count'])}")
    k2.metric("Média GC", f"{stats['mean']:.2f}%")
    k3.metric("Desvio Padrão", f"± {stats['std_dev']:.2f}")
    k4.metric("Mediana GC", f"{stats['median']:.2f}%")
    st.divider()

    t_overview, t_details, t_advanced, t_raw = st.tabs([
        "📈 Visão Geral", "🔍 Individual", "🧬 Avançada", "📄 Dados Brutos"
    ])
    
    with t_overview:
        fig, ax = plt.subplots(figsize=(10, 5))
        if stats['count'] < 20: plot_bar_chart(all_results, ax)
        else: plot_histogram(all_results, ax, stats)
        st.pyplot(fig)
        plt.close(fig)

    with t_details:
        df = pd.DataFrame(list(all_results.items()), columns=['ID', 'GC (%)'])
        c1, c2 = st.columns(2)
        min_v = c1.slider("Mínimo %", 0.0, 100.0, 0.0)
        max_v = c2.slider("Máximo %", 0.0, 100.0, 100.0)
        filtered = df[(df['GC (%)'] >= min_v) & (df['GC (%)'] <= max_v)]
        st.dataframe(filtered.style.format({'GC (%)': '{:.2f}'}), use_container_width=True)

    with t_advanced:
        if not (do_sw or do_cpg):
            st.warning("Habilite análises avançadas na barra lateral.")
        if do_sw and all_sw_results:
            st.subheader("🪟 Janela Deslizante")
            sel = st.selectbox("Sequência", list(all_sw_results.keys()))
            sw_df = pd.DataFrame({'Posição': [i*step_size for i in range(len(all_sw_results[sel]))], 'GC': all_sw_results[sel]})
            import altair as alt
            chart = alt.Chart(sw_df).mark_line().encode(x='Posição', y=alt.Y('GC', scale=alt.Scale(domain=[0, 100])))
            st.altair_chart(chart, use_container_width=True)
        if do_cpg:
            st.subheader("🏝️ Ilhas CpG")
            if all_cpg_results:
                for sid, isls in all_cpg_results.items():
                    with st.expander(sid):
                        st.table(pd.DataFrame(isls, columns=['Início', 'Fim', 'GC %', 'O/E']))
            else: st.info("Nenhuma ilha encontrada.")

    with t_raw:
        df = pd.DataFrame(list(all_results.items()), columns=['ID', 'GC (%)'])
        st.download_button("📥 Baixar CSV", df.to_csv(index=False).encode('utf-8'), "results.csv", "text/csv")

def main():
    st.title("🧬 GCScan - Analisador de Conteúdo GC (Pro)")
    st.markdown("Ferramenta profissional de bioinformática.")
    
    uploaded_files, do_sw, win_size, step_size, do_cpg = render_sidebar()
    
    if uploaded_files:
        all_results, all_sw, all_cpg = process_files(uploaded_files, do_sw, win_size, step_size, do_cpg)
        if all_results:
            render_dashboard(all_results, all_sw, all_cpg, do_sw, win_size, step_size, do_cpg)
    else:
        st.info("Aguardando upload de arquivos.")

if __name__ == "__main__":
    main()

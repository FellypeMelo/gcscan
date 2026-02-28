"""
GCScan Web Interface

Propósito: Interface web profissional para análise de conteúdo GC utilizando Streamlit.
Funcionalidades:
- Upload de arquivos FASTA
- Dashboard com KPIs (Média, Desvio Padrão)
- Visualização adaptativa (Histograma vs Barras)
- Exportação de dados
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from main import calculate_gc_content, calculate_statistics, plot_histogram, plot_bar_chart

# Configuração da página
st.set_page_config(
    page_title="GCScan - Analisador Genético Profissional",
    page_icon="🧬",
    layout="wide"
)

def main():
    """
    Função principal da aplicação Streamlit.
    Orquestra a interface do usuário e o fluxo de processamento.
    """
    
    # Cabeçalho e Descrição
    st.title("🧬 GCScan - Analisador de Conteúdo GC (Pro)")
    st.markdown("""
    Ferramenta profissional de bioinformática para análise estatística de conteúdo GC.
    Ideal para controle de qualidade (QC) de sequenciamento e estudos genômicos.
    """)

    # Sidebar para Upload e Configurações
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
        if do_sliding_window:
            win_size = st.number_input("Tamanho da Janela (bp)", min_value=10, max_value=10000, value=100)
            step_size = st.number_input("Tamanho do Passo (bp)", min_value=1, max_value=10000, value=50)
        
        do_cpg = st.checkbox("Detecção de Ilhas CpG", value=False)
        
        st.divider()
        st.markdown("Desenvolvido por **GCScan Team**")

    if uploaded_files:
        st.divider()
        
        all_results = {}
        
        # Barra de progresso para UX
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        all_sw_results = {} # Store sliding window results
        all_cpg_results = {} # Store CpG results
        
        # Processamento de cada arquivo
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processando {uploaded_file.name}...")
            
            try:
                # Salvar arquivo temporário para garantir compatibilidade com Biopython
                temp_filename = f"temp_{uploaded_file.name}"
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Calcular GC (Core Logic)
                file_results = calculate_gc_content(temp_filename)
                
                # Análises Adicionais (Se habilitadas)
                from Bio import SeqIO
                for record in SeqIO.parse(temp_filename, "fasta"):
                    unique_id = f"{uploaded_file.name}::{record.id}" if len(uploaded_files) > 1 else record.id
                    
                    if do_sliding_window:
                        from main import calculate_sliding_window_gc
                        sw = calculate_sliding_window_gc(record.seq, win_size, step_size)
                        all_sw_results[unique_id] = sw
                    
                    if do_cpg:
                        from main import detect_cpg_islands
                        islands = detect_cpg_islands(record.seq)
                        if islands:
                            all_cpg_results[unique_id] = islands
                
                # Merge nos resultados globais
                for seq_id, gc in file_results.items():
                    unique_id = f"{uploaded_file.name}::{seq_id}" if len(uploaded_files) > 1 else seq_id
                    all_results[unique_id] = gc
                
                # Remover temp
                os.remove(temp_filename)
                
            except Exception as e:
                st.error(f"Erro ao processar {uploaded_file.name}: {e}")
            
            # Atualizar progresso
            progress_bar.progress((i + 1) / len(uploaded_files))
            
        status_text.empty()
        progress_bar.empty()

        if all_results:
            # Calcular Estatísticas Globais
            stats = calculate_statistics(all_results)
            count = stats['count']
            
            # --- DASHBOARD ---
            
            st.subheader("📊 Relatório de Estatísticas")
            
            # 1. KPIs (Key Performance Indicators)
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("Total de Sequências", f"{int(stats['count'])}")
            kpi2.metric("Média GC", f"{stats['mean']:.2f}%", help="Média aritmética do conteúdo GC")
            kpi3.metric("Desvio Padrão", f"± {stats['std_dev']:.2f}", help="Medida de dispersão dos dados")
            kpi4.metric("Mediana GC", f"{stats['median']:.2f}%")
            
            st.divider()
            
            # 2. Tabs para Organização
            tab_overview, tab_details, tab_advanced, tab_raw = st.tabs([
                "📈 Visão Geral (Distribuição)", 
                "🔍 Análise Individual", 
                "🧬 Análise Avançada",
                "📄 Dados Brutos"
            ])
            
            with tab_overview:
                st.markdown("### Distribuição de Conteúdo GC")
                
                # Plotagem Adaptativa
                fig, ax = plt.subplots(figsize=(10, 5))
                
                if count < 20:
                    st.info("Exibindo Gráfico de Barras (N < 20 amostras).")
                    plot_bar_chart(all_results, ax)
                else:
                    st.success(f"Exibindo Histograma de Distribuição (N = {count} amostras).")
                    plot_histogram(all_results, ax, stats)
                
                st.pyplot(fig)
                plt.close(fig)
                
                st.markdown(f"""
                **Interpretação:**
                - A linha **Vermelha** indica a média ({stats['mean']:.2f}%).
                - As linhas **Laranjas** indicam desvio padrão (±{stats['std_dev']:.2f}).
                """)

            with tab_details:
                st.markdown("### Análise Detalhada por Sequência")
                
                # DataFrame
                df = pd.DataFrame(list(all_results.items()), columns=['ID_Sequencia', 'GC_Content (%)'])
                
                # Filtros interativos
                col_filter1, col_filter2 = st.columns(2)
                min_gc = col_filter1.slider("Filtrar GC Mínimo (%)", 0.0, 100.0, 0.0)
                max_gc = col_filter2.slider("Filtrar GC Máximo (%)", 0.0, 100.0, 100.0)
                
                filtered_df = df[(df['GC_Content (%)'] >= min_gc) & (df['GC_Content (%)'] <= max_gc)]
                
                st.dataframe(filtered_df.style.format({'GC_Content (%)': '{:.2f}'}), use_container_width=True)
                st.caption(f"Exibindo {len(filtered_df)} de {len(df)} sequências.")

            with tab_advanced:
                st.markdown("### Resultados de Análise Avançada")
                
                if not (do_sliding_window or do_cpg):
                    st.warning("Habilite a Janela Deslizante ou Detecção de CpG na barra lateral para ver os resultados aqui.")
                
                if do_sliding_window and all_sw_results:
                    st.subheader("🪟 Janela Deslizante")
                    selected_seq = st.selectbox("Selecione a sequência para visualizar", list(all_sw_results.keys()))
                    
                    sw_data = all_sw_results[selected_seq]
                    # Criar DataFrame para plotagem
                    x_coords = [i * step_size for i in range(len(sw_data))]
                    sw_df = pd.DataFrame({
                        'Posição (bp)': x_coords,
                        'GC (%)': sw_data
                    })
                    
                    import altair as alt
                    chart = alt.Chart(sw_df).mark_line(color='steelblue').encode(
                        x='Posição (bp)',
                        y=alt.Y('GC (%)', scale=alt.Scale(domain=[0, 100])),
                        tooltip=['Posição (bp)', 'GC (%)']
                    ).interactive().properties(height=400)
                    
                    st.altair_chart(chart, use_container_width=True)
                    st.caption(f"Visualizando variação local de GC em {selected_seq} (Janela: {win_size}bp, Passo: {step_size}bp)")

                if do_cpg:
                    st.divider()
                    st.subheader("🏝️ Ilhas CpG")
                    if all_cpg_results:
                        for seq_id, islands in all_cpg_results.items():
                            with st.expander(f"Ilhas em {seq_id} ({len(islands)} encontradas)"):
                                cpg_df = pd.DataFrame(islands, columns=['Início', 'Fim', 'GC (%)', 'Obs/Exp'])
                                st.table(cpg_df.style.format({'GC (%)': '{:.1f}', 'Obs/Exp': '{:.2f}'}))
                    else:
                        st.info("Nenhuma ilha CpG detectada com os critérios padrão nas sequências processadas.")

            with tab_raw:
                st.markdown("### Exportação de Dados")
                # Download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Baixar Todos os Resultados (CSV)",
                    data=csv,
                    file_name='gc_scan_results_full.csv',
                    mime='text/csv',
                )

    else:
        st.info("Aguardando upload de arquivos para iniciar a análise.")

if __name__ == "__main__":
    main()

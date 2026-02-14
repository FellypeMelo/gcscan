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
        st.markdown("Desenvolvido por **GCScan Team**")

    if uploaded_files:
        st.divider()
        
        all_results = {}
        
        # Barra de progresso para UX
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Processamento de cada arquivo
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processando {uploaded_file.name}...")
            
            try:
                # Salvar arquivo temporário para garantir compatibilidade com Biopython
                with open(f"temp_{uploaded_file.name}", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Calcular GC (Core Logic)
                file_results = calculate_gc_content(f"temp_{uploaded_file.name}")
                
                # Merge nos resultados globais
                # Prefixar chave com nome do arquivo se houver conflito ou para rastreabilidade
                # Aqui vamos manter simples e agrupar tudo para análise global, 
                # mas mantendo identificador original
                for seq_id, gc in file_results.items():
                    unique_id = f"{uploaded_file.name}::{seq_id}" if len(uploaded_files) > 1 else seq_id
                    all_results[unique_id] = gc
                
                # Remover temp
                os.remove(f"temp_{uploaded_file.name}")
                
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
            tab_overview, tab_details, tab_raw = st.tabs(["📈 Visão Geral (Distribuição)", "🔍 Análise Individual", "📄 Dados Brutos"])
            
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

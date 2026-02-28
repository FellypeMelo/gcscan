"""
GCScan Web Interface (Entry Point)
"""

import streamlit as st
from src.infrastructure.web.components import render_sidebar, process_uploads, render_main_dashboard

def main():
    st.set_page_config(
        page_title="GCScan - Analisador Genético Profissional",
        page_icon="🧬",
        layout="wide"
    )
    st.title("🧬 GCScan - Analisador de Conteúdo GC (Pro)")
    st.markdown("Ferramenta profissional de bioinformática.")
    
    files, do_sw, w, s, do_cpg = render_sidebar()
    
    if files:
        results, sw_res, cpg_res = process_uploads(files, do_sw, w, s, do_cpg)
        if results:
            sw_params = {'window': w, 'step': s}
            render_main_dashboard(results, sw_res, cpg_res, sw_params)
    else:
        st.info("Aguardando upload de arquivos.")

if __name__ == "__main__":
    main()

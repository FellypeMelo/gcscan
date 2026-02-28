import argparse

def parse_args():
    """Define e processa argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        description="GCScan - Analisador de Conteúdo GC Profissional"
    )
    parser.add_argument("input", help="Arquivo ou diretório FASTA.")
    parser.add_argument("--output_dir", "-o", default="results", help="Diretório de saída.")
    parser.add_argument("--window", "-w", type=int, help="Tamanho da janela.")
    parser.add_argument("--step", "-s", type=int, help="Tamanho do passo.")
    parser.add_argument("--cpg", action="store_true", help="Ativar ilhas CpG.")
    parser.add_argument("--parallel", action="store_true", help="Ativar processamento Multicore (Multiprocessing).")
    parser.add_argument("--workers", type=int, default=None, help="Número de workers paralelos (default: CPU Count).")
    return parser.parse_args()

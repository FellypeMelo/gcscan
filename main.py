"""
GCScan - Analisador de Conteúdo GC (CLI Entry Point)
"""

import sys
import os
from src.infrastructure.cli.parser import parse_args
from src.infrastructure.cli.runner import run_analysis

def main():
    args = parse_args()
    
    if not os.path.exists(args.input):
        print(f"Erro: Entrada '{args.input}' não encontrada.")
        sys.exit(1)
        
    try:
        run_analysis(args)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

"""
GCScan - Analisador de Conteúdo GC

Propósito: Ler arquivos FASTA, calcular a porcentagem de conteúdo GC
em cada sequência e gerar visualização gráfica dos resultados.

Este módulo utiliza Biopython para parsing de FASTA e Matplotlib
para geração de gráficos.
"""

from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import matplotlib.pyplot as plt
import os


def calculate_gc_content(fasta_path):
    """
    Calcula o conteúdo GC de cada sequência em um arquivo FASTA.

    Args:
        fasta_path: Caminho para o arquivo FASTA

    Returns:
        dict: Dicionário com ID da sequência como chave e % GC como valor
    """
    results = {}

    for record in SeqIO.parse(fasta_path, "fasta"):
        # Calcula fração GC e converte para porcentagem
        gc_percent = gc_fraction(record.seq) * 100
        results[record.id] = gc_percent

    return results


def plot_gc_content(results, output_path="gc_content.png"):
    """
    Gera gráfico de barras com o conteúdo GC.

    Args:
        results: Dicionário com resultados do cálculo GC
        output_path: Caminho para salvar o gráfico
    """
    plt.figure(figsize=(10, 6))
    plt.bar(results.keys(), results.values(), color="steelblue")
    plt.ylabel("Conteúdo GC (%)", fontsize=12)
    plt.xlabel("Sequência", fontsize=12)
    plt.title("Análise de Conteúdo GC", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Gráfico salvo em: {output_path}")
    plt.show()


def main():
    """Função principal do programa."""
    fasta_file = "data/sample.fasta"

    if not os.path.exists(fasta_file):
        print(f"Erro: Arquivo {fasta_file} não encontrado.")
        print("Por favor, adicione um arquivo FASTA na pasta data/")
        return

    print("=" * 50)
    print("GCScan - Analisador de Conteúdo GC")
    print("=" * 50)

    # Calcula conteúdo GC
    results = calculate_gc_content(fasta_file)

    # Exibe resultados
    print("\nResultados:")
    print("-" * 30)
    for seq_id, gc_value in results.items():
        print(f"{seq_id}: {gc_value:.2f}%")

    # Gera gráfico
    if results:
        plot_gc_content(results)

    print("\nAnálise concluída!")


if __name__ == "__main__":
    main()

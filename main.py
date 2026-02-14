"""
GCScan - Analisador de Conteúdo GC

Propósito: Ler arquivos FASTA, calcular a porcentagem de conteúdo GC
em cada sequência, gerar visualização gráfica e exportar resultados.
"""

import argparse
import csv
import os
import sys
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import numpy as np
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction


def calculate_gc_content(fasta_path: str) -> Dict[str, float]:
    """
    Calcula o conteúdo GC de cada sequência em um arquivo FASTA.
    
    Entrada:
        fasta_path (str): Caminho para o arquivo FASTA.
    
    Saída:
        dict: Dicionário onde a chave é o ID da sequência e o valor é a porcentagem de GC.
    
    Complexidade (Big O):
        O(N), onde N é o número total de nucleotídeos no arquivo.
        Precisamos iterar por cada base para contar Gs e Cs.
    """
    results = {}
    try:
        # SeqIO.parse retorna um iterador, processando uma sequência por vez (eficiente em memória)
        for record in SeqIO.parse(fasta_path, "fasta"):
            # O(L) onde L é o comprimento da sequência atual
            gc_percent = gc_fraction(record.seq) * 100
            results[record.id] = gc_percent
    except Exception as e:
        print(f"Erro ao ler arquivo {fasta_path}: {e}")
        sys.exit(1)

    return results


def calculate_statistics(results: Dict[str, float]) -> Dict[str, float]:
    """
    Calcula estatísticas descritivas (Média, Mediana, Desvio Padrão).
    
    Entrada:
        results (dict): Dicionário com resultados do cálculo GC.
        
    Saída:
        dict: Dicionário contendo as estatísticas calculadas.
        
    Complexidade (Big O):
        O(S), onde S é o número de sequências (para converter dict values para lista e calcular média/std).
    """
    values = list(results.values())
    if not values:
        return {}
    
    stats = {
        "mean": np.mean(values),
        "median": np.median(values),
        "std_dev": np.std(values),
        "min": np.min(values),
        "max": np.max(values),
        "count": len(values)
    }
    return stats


def save_results_to_csv(results: Dict[str, float], output_path: str):
    """
    Salva os resultados do cálculo GC em um arquivo CSV.
    
    Entrada:
        results (dict): Dicionário com IDs e porcentagens de GC.
        output_path (str): Caminho onde o arquivo CSV será salvo.
    
    Saída:
        None (Gera um arquivo físico no disco).
    
    Complexidade (Big O):
        O(S), onde S é o número de sequências.
        Iteramos uma vez sobre o dicionário de resultados para escrever no arquivo.
    """
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Sequence_ID', 'GC_Content_Percent'])
            for seq_id, gc_value in results.items():
                writer.writerow([seq_id, f"{gc_value:.2f}"])
        print(f"Resultados exportados para: {output_path}")
    except IOError as e:
        print(f"Erro ao salvar CSV: {e}")


def plot_bar_chart(results: Dict[str, float], ax):
    """
    Função auxiliar para plotar gráfico de barras (para poucos dados).
    """
    names = list(results.keys())
    values = list(results.values())
    
    bars = ax.bar(names, values, color="steelblue", alpha=0.8, edgecolor='black', linewidth=0.5)
    
    ax.set_ylabel("Conteúdo GC (%)", fontsize=12)
    ax.set_xlabel("ID da Sequência", fontsize=12)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Rotação dos labels do eixo X
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10)
    
    # Adicionar valor acima
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=8)


def plot_histogram(results: Dict[str, float], ax, stats: Dict[str, float]):
    """
    Função auxiliar para plotar histograma (para muitos dados).
    Inclui linhas verticais para Média e Desvio Padrão.
    """
    values = list(results.values())
    
    # Histograma
    n, bins, patches = ax.hist(values, bins='auto', color='steelblue', alpha=0.7, rwidth=0.85, edgecolor='black')
    
    ax.set_ylabel("Frequência", fontsize=12)
    ax.set_xlabel("Conteúdo GC (%)", fontsize=12)
    ax.set_xlim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Linhas de Estatística
    mean = stats['mean']
    std = stats['std_dev']
    
    ax.axvline(mean, color='red', linestyle='-', linewidth=2, label=f'Média ({mean:.1f}%)')
    ax.axvline(mean - std, color='orange', linestyle='--', linewidth=1.5, label=f'-1 SD ({(mean-std):.1f}%)')
    ax.axvline(mean + std, color='orange', linestyle='--', linewidth=1.5, label=f'+1 SD ({(mean+std):.1f}%)')
    
    ax.legend(loc='upper right', frameon=True)


def plot_gc_content(results: Dict[str, float], output_path: str):
    """
    Gera visualização adaptativa do conteúdo GC.
    Bar Chart se N < 20, Histograma se N >= 20.
    
    Entrada:
        results (dict): Dicionário com resultados do cálculo GC.
        output_path (str): Caminho para salvar a imagem do gráfico.
    
    Saída:
        None (Gera um arquivo de imagem no disco).
    
    Complexidade (Big O):
        O(S) para preparação dos dados e plotagem.
    """
    if not results:
        print("Nenhum resultado para plotar.")
        return

    stats = calculate_statistics(results)
    count = stats['count']
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    if count < 20:
        ax.set_title(f"Análise de Conteúdo GC (N={count})", fontsize=14, fontweight="bold")
        plot_bar_chart(results, ax)
    else:
        ax.set_title(f"Distribuição de Conteúdo GC (N={count})", fontsize=14, fontweight="bold")
        plot_histogram(results, ax, stats)

    plt.tight_layout()
    try:
        plt.savefig(output_path, dpi=300, bbox_inches="tight") # 300 DPI for Scientific Publication
        print(f"Gráfico salvo em: {output_path}")
    except IOError as e:
        print(f"Erro ao salvar gráfico: {e}")
    finally:
        plt.close(fig) # Importante para liberar memória em loops


def main():
    """
    Função principal que orquestra o fluxo do programa via CLI.
    """
    parser = argparse.ArgumentParser(
        description="GCScan - Analisador de Conteúdo GC Profissional"
    )
    
    # Argumentos Inputs
    parser.add_argument(
        "input", 
        help="Caminho para o arquivo FASTA de entrada ou diretório contendo arquivos FASTA."
    )
    
    # Argumentos Outputs
    parser.add_argument(
        "--output_dir", "-o",
        default="results",
        help="Diretório onde os resultados (CSV e PNG) serão salvos. Padrão: 'results/'"
    )

    args = parser.parse_args()

    # Validar entrada
    if not os.path.exists(args.input):
        print(f"Erro: Entrada '{args.input}' não encontrada.")
        sys.exit(1)

    # Preparar diretório de saída
    if not os.path.exists(args.output_dir):
        try:
            os.makedirs(args.output_dir)
            print(f"Diretório criado: {args.output_dir}")
        except OSError as e:
            print(f"Erro ao criar diretório de saída: {e}")
            sys.exit(1)

    # Identificar arquivos para processar
    files_to_process = []
    if os.path.isdir(args.input):
        for f in os.listdir(args.input):
            if f.lower().endswith(('.fasta', '.fa', '.fna')):
                files_to_process.append(os.path.join(args.input, f))
    else:
        files_to_process.append(args.input)

    if not files_to_process:
        print("Nenhum arquivo FASTA encontrado.")
        sys.exit(0)

    print("=" * 60)
    print(f"GCScan - Iniciando análise profissional de {len(files_to_process)} arquivo(s)")
    print("=" * 60)

    for fasta_file in files_to_process:
        base_name = os.path.splitext(os.path.basename(fasta_file))[0]
        print(f"\nProcessando: {base_name}...")
        
        # 1. Calcular
        results = calculate_gc_content(fasta_file)
        
        if not results:
            print(f"  Aviso: Nenhuma sequência encontrada em {base_name}.")
            continue

        # 2. Estatísticas (apenas para log/display, plotagem recalcula ou poderíamos passar)
        stats = calculate_statistics(results)
        print(f"  > Sequências: {stats['count']}")
        print(f"  > Média GC:   {stats['mean']:.2f}% (± {stats['std_dev']:.2f})")

        # 3. Exportar CSV
        csv_path = os.path.join(args.output_dir, f"{base_name}_gc.csv")
        save_results_to_csv(results, csv_path)

        # 4. Gerar Gráfico (Adaptativo)
        png_path = os.path.join(args.output_dir, f"{base_name}_gc_analysis.png")
        plot_gc_content(results, png_path)

    print("\n" + "=" * 60)
    print("Processamento concluído com sucesso!")


if __name__ == "__main__":
    main()

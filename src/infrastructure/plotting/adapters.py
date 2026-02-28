import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import Dict

def plot_gc_distribution(results: Dict[str, float], stats: Dict[str, float], output_path: str):
    """Gera visualização adaptativa do conteúdo GC."""
    if not results: return
    
    count = stats['count']
    fig, ax = plt.subplots(figsize=(12, 7))
    
    if count < 20:
        _setup_bar_chart(ax, count)
        _plot_bar_chart(results, ax)
    else:
        _setup_histogram(ax, count)
        _plot_histogram(results, ax, stats)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

def _setup_bar_chart(ax, count: int):
    ax.set_title(f"Análise de Conteúdo GC (N={count})", fontsize=14, fontweight="bold")
    ax.set_ylabel("Conteúdo GC (%)", fontsize=12)
    ax.set_xlabel("ID da Sequência", fontsize=12)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

def _plot_bar_chart(results: Dict[str, float], ax):
    names = list(results.keys())
    values = list(results.values())
    bars = ax.bar(names, values, color="steelblue", alpha=0.8, edgecolor='black', linewidth=0.5)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)

def _setup_histogram(ax, count: int):
    ax.set_title(f"Distribuição de Conteúdo GC (N={count})", fontsize=14, fontweight="bold")
    ax.set_ylabel("Frequência", fontsize=12)
    ax.set_xlabel("Conteúdo GC (%)", fontsize=12)
    ax.set_xlim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

def _plot_histogram(results: Dict[str, float], ax, stats: Dict[str, float]):
    values = list(results.values())
    ax.hist(values, bins='auto', color='steelblue', alpha=0.7, rwidth=0.85, edgecolor='black')
    
    mean, std = stats['mean'], stats['std_dev']
    ax.axvline(mean, color='red', linestyle='-', linewidth=2, label=f'Média ({mean:.1f}%)')
    ax.axvline(mean - std, color='orange', linestyle='--', linewidth=1.5, label=f'-1 SD ({(mean-std):.1f}%)')
    ax.axvline(mean + std, color='orange', linestyle='--', linewidth=1.5, label=f'+1 SD ({(mean+std):.1f}%)')
    ax.legend(loc='upper right', frameon=True)

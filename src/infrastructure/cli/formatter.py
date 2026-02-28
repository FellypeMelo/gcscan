from typing import Dict, List
from src.domain.models import CpGIsland

def print_header(file_count: int):
    print("=" * 60)
    print(f"GCScan - Iniciando análise profissional de {file_count} arquivo(s)")
    print("=" * 60)

def print_file_start(base_name: str):
    print(f"\nProcessando: {base_name}...")

def print_stats(stats: Dict[str, float]):
    print(f"  > Sequências: {stats['count']}")
    print(f"  > Média GC:   {stats['mean']:.2f}% (± {stats['std_dev']:.2f})")

def print_sliding_window_info(seq_id: str, count: int):
    print(f"    > Janela Deslizante ({seq_id}): {count} janelas calculadas.")

def print_cpg_islands(seq_id: str, islands: List[CpGIsland]):
    if islands:
        print(f"    > Ilhas CpG ({seq_id}): {len(islands)} encontradas.")
        for isl in islands:
            print(f"      - [{isl.start}:{isl.end}] GC: {isl.gc_percent:.1f}%, Obs/Exp: {isl.oe_ratio:.2f}")
    else:
        print(f"    > Ilhas CpG ({seq_id}): Nenhuma encontrada.")

def print_footer():
    print("\n" + "=" * 60)
    print("Processamento concluído com sucesso!")

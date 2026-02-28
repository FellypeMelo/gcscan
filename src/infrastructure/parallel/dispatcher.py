import concurrent.futures
import os
from typing import Dict, List, Tuple, Any
from src.infrastructure.io.fasta import read_fasta
from src.domain.analysis import calculate_gc_percentage, calculate_sliding_window, detect_cpg_islands
from src.domain.models import CpGIsland

def _process_single_sequence(item: Tuple[str, str, int, int, bool]) -> Tuple[str, float, List[CpGIsland], List[float]]:
    """Função encapsulada para rodar isoladamente em cada núcleo (Process) e evitar overhead."""
    seq_id, sequence, window, step, cpg = item
    
    gc_percent = calculate_gc_percentage(sequence)
    
    islands = []
    if cpg:
        islands = detect_cpg_islands(sequence)
        
    windows = []
    if window > 0:
        actual_step = step if step > 0 else window
        windows = calculate_sliding_window(sequence, window, actual_step)
        
    return seq_id, gc_percent, islands, windows

def process_fasta_parallel(
    file_path: str, 
    window: int = 0, 
    step: int = 0, 
    cpg: bool = False, 
    max_workers: int = None
) -> Tuple[Dict[str, float], Dict[str, List[CpGIsland]], Dict[str, List[float]]]:
    """
    Despacha a leitura FASTA através de `os.cpu_count()` ou max_workers definidos.
    O iterador do Biopython aciona via generator (prevenindo OOM em arquivos Gigantes),
    e o executor mapeia a rotina pura algébrica sobre os núcleos disponíveis.
    """
    if max_workers is None:
        max_workers = os.cpu_count() or 1
        
    results = {}
    all_islands = {}
    all_windows = {}
    
    iterator = read_fasta(file_path)
    
    def generate_tasks():
        for seq_id, sequence in iterator:
            yield (seq_id, sequence, window, step, cpg)
            
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # chunkSize agrupa processos em lotes para minimizar o overhead de pickle e troca de IPC
        for seq_id, gc, islands, windows in executor.map(_process_single_sequence, generate_tasks(), chunksize=10):
            results[seq_id] = gc
            if cpg:
                all_islands[seq_id] = islands
            if window > 0:
                all_windows[seq_id] = windows
                
    return results, all_islands, all_windows

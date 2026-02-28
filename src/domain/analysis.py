from typing import List, Tuple, Optional
from src.domain.models import CpGIsland

def calculate_gc_percentage(sequence: str) -> float:
    """Calcula a porcentagem de GC em uma sequência de DNA."""
    if not sequence: return 0.0
    seq = sequence.upper()
    gc_count = seq.count('G') + seq.count('C')
    return (gc_count / len(seq)) * 100

def calculate_sliding_window(sequence: str, win_size: int, step: int) -> List[float]:
    """Calcula GC em janelas deslizantes."""
    return [calculate_gc_percentage(sequence[i:i+win_size]) 
            for i in range(0, len(sequence)-win_size+1, step)]

def detect_cpg_islands(sequence: str, min_len: int = 200, min_gc: float = 50.0, min_oe: float = 0.6) -> List[CpGIsland]:
    """Identifica ilhas CpG em uma sequência de DNA."""
    islands = []
    seq_str = str(sequence).upper()
    i, n = 0, len(seq_str)
    while i < n - 50 + 1:
        res = _try_seed_at(seq_str, i, min_len, min_gc, min_oe)
        if res:
            islands.append(res[0])
            i = res[1]
        else:
            i += 10
    return islands

def _try_seed_at(seq: str, i: int, m_len: int, m_gc: float, m_oe: float) -> Optional[Tuple[CpGIsland, int]]:
    """Tenta encontrar e expandir uma semente na posição i."""
    sub = seq[i : i + 50]
    g, c = sub.count('G'), sub.count('C')
    if ((g + c) / 50) * 100 < m_gc: return None
    
    oe = (sub.count('CG') * 50) / (c * g) if (c * g) > 0 else 0
    if oe < m_oe: return None
    
    return _expand_and_validate(seq, i, m_len, m_gc, m_oe)

def _expand_and_validate(seq: str, i: int, m_len: int, m_gc: float, m_oe: float) -> Optional[Tuple[CpGIsland, int]]:
    """Expande semente e valida critérios finais."""
    start, end = _expand_borders(seq, i, i + 50)
    
    # Encontrar limites reais de G/C dentro do range expandido
    sub = seq[start:end]
    first_gc = _find_first_gc(sub)
    last_gc = _find_last_gc(sub)
    
    if first_gc == -1: return None
    
    actual_start = start + first_gc
    actual_end = start + last_gc + 1
    final_sub = seq[actual_start:actual_end]
    
    f_len = len(final_sub)
    if f_len < m_len: return None
    
    g, c = final_sub.count('G'), final_sub.count('C')
    gc = ((g + c) / f_len) * 100
    oe = (final_sub.count('CG') * f_len) / (c * g) if (c * g) > 0 else 0
    
    if gc >= m_gc and oe >= m_oe:
        return CpGIsland(actual_start, actual_end, gc, oe), actual_end
    return None

def _find_first_gc(s: str) -> int:
    for idx, char in enumerate(s):
        if char in "GC": return idx
    return -1

def _find_last_gc(s: str) -> int:
    for idx in range(len(s) - 1, -1, -1):
        if s[idx] in "GC": return idx
    return -1

def _expand_borders(seq: str, start: int, end: int) -> Tuple[int, int]:
    """Expande fronteiras enquanto encontrar G ou C."""
    while start > 0 and seq[start - 1] in "GC": start -= 1
    while end < len(seq) and seq[end] in "GC": end += 1
    return start, end

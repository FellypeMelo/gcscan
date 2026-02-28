from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass(frozen=True)
class CpGIsland:
    start: int
    end: int
    gc_percent: float
    oe_ratio: float

@dataclass(frozen=True)
class SequenceAnalysis:
    id: str
    gc_percent: float
    sliding_window: List[float]
    cpg_islands: List[CpGIsland]

@dataclass(frozen=True)
class AnalysisSummary:
    count: int
    mean_gc: float
    median_gc: float
    std_dev_gc: float
    min_gc: float
    max_gc: float

# Design Doc: Modular Kernel Architecture for GCScan

## 1. Vision
To transition GCScan from a monolithic script collection to a modular "Kernel-based" architecture that enforces AI-XP Iron Laws, specifically **Clean Architecture** and **Dependency Inversion**.

## 2. Proposed Structure

```text
gcscan/
├── src/
│   ├── domain/                 # PURE LOGIC (Kernel)
│   │   ├── __init__.py
│   │   ├── analysis.py         # GC calculation, Sliding Window, CpG Detection
│   │   ├── statistics.py       # Descriptive statistics
│   │   └── models.py           # Value Objects (SequenceResult, AnalysisSummary)
│   ├── infrastructure/         # External World (Shells)
│   │   ├── __init__.py
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   ├── parser.py       # Argparse definitions
│   │   │   └── formatter.py    # Console output logic
│   │   ├── web/
│   │   │   ├── __init__.py
│   │   │   └── components.py   # Streamlit UI pieces
│   │   ├── io/
│   │   │   ├── __init__.py
│   │   │   ├── fasta.py        # Biopython wrapper
│   │   │   └── exporters.py    # CSV and Image saving
│   │   └── plotting/
│   │       ├── __init__.py
│   │       └── adapters.py     # Matplotlib/Altair logic
├── tests/                      # Mirroring src/
│   ├── domain/
│   └── infrastructure/
├── main.py                     # CLI Entry Point (Thin)
├── app.py                      # Web Entry Point (Thin)
└── data/                       # Local testing data (ignored)
```

## 3. Principles Enforcement

### Clean Architecture (Law 2)
- **Domain:** `src/domain/` will have ZERO imports from `Bio`, `matplotlib`, `streamlit`, or `pandas`. It operates on pure Python types and custom Value Objects.
- **Infrastructure:** All 3rd-party dependencies are confined here.

### Mathematical Rigor & SOLID (Law 1 & 5)
- All domain functions will be tested for edge cases (zero length, 100% GC, etc.) before implementation.
- **SRP:** Parsing args is in `cli/parser.py`; calculating GC is in `domain/analysis.py`.

### Algorithmic Elegance
- Any function exceeding 15 lines (like the current `detect_cpg_islands` or `main`) will be decomposed into smaller units in the new structure.

## 4. Migration Plan
1. Create directory structure.
2. Implement `domain` with TDD.
3. Migrate `io` and `plotting`.
4. Refactor `main.py` and `app.py`.
5. Verify 100% test parity.

# Implementation Plan: System Analysis, Cleanup, and Modular Kernel Restructuring

## Phase 1: Full System Analysis & Audit
- [x] Task: Audit core logic (`main.py`, `app.py`) against AI-XP Iron Laws.
    - [x] Check for functions exceeding 15 logical lines. (Found: detect_cpg_islands, plot_gc_content, main in main.py; render_sidebar, process_files, render_dashboard in app.py)
    - [x] Identify classes exceeding 200 lines. (None found)
    - [x] Audit for "summarized code" anti-patterns (// ...). (None found)
    - [x] Check for direct infrastructure leaks into domain logic (Clean Architecture violation). (Found: logic mixed with CLI/UI and I/O)
- [x] Task: Audit data directories (`test_data/`, `data/`, `results/`) for redundancy.
    - [x] Map all FASTA files used in current tests. (Found: None used from test_data/, tests generate own temps)
    - [x] Identify unused/duplicated test assets. (Found: 55+ files in test_data/ and generate_test_data.py are candidates for cleanup or moving to a non-production bucket)
    - [x] Verify persistence of `.gitignore` rules for `results/`. (Verified: results/ and data/*.fasta are ignored)
- [x] Task: Audit test suite coverage and TDD compliance.
    - [x] Verify if all core logic has corresponding failing test history. (Verified for latest features: sw and cpg. Older logic legacy.)
    - [x] Run current coverage report (`pytest --cov=main`). (Result: 94% global. main.py 91%, app.py 98%. Missing edge cases in expansion and CLI error handling.)
    - [x] Identify logic blocks lacking "Red-Green-Refactor" documentation. (Older CLI parsing logic lacks documented RGR history.)
- [x] Task: Propose Modular Kernel Architecture (Design Doc).
    - [x] Define `src/domain/` (Pure logic, no infra imports).
    - [x] Define `src/infrastructure/` (CLI, Web UI, I/O).
    - [x] Plan Dependency Inversion (DIP) for the Kernel. (Defined in KERNEL_DESIGN.md)
- [x] Task: Conductor - User Manual Verification 'Full System Analysis & Audit' (Protocol in workflow.md) [checkpoint: 8622488]

## Phase 2: Cleanup & Preparation
- [x] Task: Remove redundant FASTA files and temporary artifacts.
    - [x] Wipe `__pycache__` and `.pytest_cache`. (Done)
    - [x] Delete `temp_*` files. (Done)
    - [x] Remove identified redundant FASTA assets. (Removed test_data/ and generate_test_data.py)
- [x] Task: Execute Dead Code removal based on audit findings.
    - [x] Remove unused imports. (Removed unused numpy from app.py)
    - [x] Delete unreachable code branches. (None found in core logic)
    - [x] Ensure every change is a full SEARCH/REPLACE block. (Verified)
- [~] Task: Conductor - User Manual Verification 'Cleanup & Preparation' (Protocol in workflow.md)

## Phase 3: Modular Kernel Restructuring (AI-XP Agêntico Loop)
- [ ] Task: Implement Domain Kernel (Pure GC & CpG) - **Phase 🔴 RED**.
    - [ ] Create `tests/domain/test_kernel.py`.
    - [ ] Write failing tests for pure sequence analysis (Mathematical Rigor).
- [ ] Task: Implement Domain Kernel (Logic) - **Phase 🟢 GREEN**.
    - [ ] Create `src/domain/kernel.py`.
    - [ ] Implement MINIMUM code to pass domain tests.
- [ ] Task: Refactor Domain Kernel - **Phase 🔵 REFACTOR**.
    - [ ] Enforce "Algorithmic Elegance" (Functions <= 15 lines).
    - [ ] Minimize nesting depth (<= 2).
    - [ ] Verify cyclomatic complexity <= 15.
- [ ] Task: Refactor CLI Shell (`main.py`) to depend on Kernel (DIP).
    - [ ] Move CLI-specific logic to `src/infrastructure/cli.py`.
    - [ ] Ensure `main.py` is a thin entry point.
- [ ] Task: Refactor Web Shell (`app.py`) to depend on Kernel (DIP).
    - [ ] Move Web-specific logic to `src/infrastructure/web.py`.
    - [ ] Ensure `app.py` is a thin entry point.
- [ ] Task: Conductor - User Manual Verification 'Modular Restructuring' (Protocol in workflow.md)

## Phase 4: Final Verification & Integration
- [ ] Task: Update and verify full test suite coverage (>90%).
    - [ ] Ensure no code bypassed strong type protections.
    - [ ] Validate "Value Objects" usage for domain IDs/metrics.
- [ ] Task: Perform end-to-end integration testing (CLI + Web).
    - [ ] Verify zero regressions in FASTA parsing.
    - [ ] Verify correct output generation in `results/`.
- [ ] Task: Update documentation and Conductor index.
    - [ ] Reflect new folder hierarchy in `README.md`.
    - [ ] Update `conductor/index.md` paths.
- [ ] Task: Conductor - User Manual Verification 'Final Verification & Integration' (Protocol in workflow.md)

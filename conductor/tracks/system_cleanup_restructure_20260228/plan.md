# Implementation Plan: System Analysis, Cleanup, and Modular Kernel Restructuring

## Phase 1: Full System Analysis & Audit
- [ ] Task: Audit core logic (`main.py`, `app.py`) against AI-XP constraints (15-line functions, max 200-line classes).
- [ ] Task: Audit data directories (`test_data/`, `data/`, `results/`) for redundancy and unused assets.
- [ ] Task: Audit test suite coverage and integrity (Ensuring no logic exists without a failing test first).
- [ ] Task: Propose Modular Kernel Architecture (Design Doc adhering to Dependency Inversion: Domain isolated from Infra).
- [ ] Task: Conductor - User Manual Verification 'Full System Analysis & Audit' (Protocol in workflow.md)

## Phase 2: Cleanup & Preparation
- [ ] Task: Remove redundant FASTA files and temporary artifacts (`__pycache__`, etc.).
- [ ] Task: Execute Dead Code removal based on audit findings (Strict SEARCH/REPLACE blocks only).
- [ ] Task: Conductor - User Manual Verification 'Cleanup & Preparation' (Protocol in workflow.md)

## Phase 3: Modular Kernel Restructuring (AI-XP Agêntico Loop)
- [ ] Task: Implement Domain Kernel (Pure GC Calculation & CpG logic) - **Phase 🔴 RED: Write failing tests first.**
- [ ] Task: Implement Domain Kernel (Logic) - **Phase 🟢 GREEN: Implement minimal code to pass.**
- [ ] Task: Refactor Domain Kernel - **Phase 🔵 REFACTOR: Optimize for <15 lines/function.**
- [ ] Task: Refactor CLI Shell (`main.py`) to depend on Kernel (DIP) and remove summarized code.
- [ ] Task: Refactor Web Shell (`app.py`) to depend on Kernel (DIP) and remove summarized code.
- [ ] Task: Conductor - User Manual Verification 'Modular Restructuring' (Protocol in workflow.md)

## Phase 4: Final Verification & Integration
- [ ] Task: Update and verify full test suite coverage (>90%).
- [ ] Task: Perform end-to-end integration testing (CLI + Web) with zero regressions.
- [ ] Task: Update documentation and Conductor index paths to reflect the new structure.
- [ ] Task: Conductor - User Manual Verification 'Final Verification & Integration' (Protocol in workflow.md)

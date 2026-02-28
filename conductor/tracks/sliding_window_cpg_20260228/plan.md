# Implementation Plan: Sliding Window and CpG Island Detection

## Phase 1: Core Analysis Logic [checkpoint: 95be8fa]
- [x] Task: Implement Sliding Window GC calculation [3cbebff]
    - [x] Write Tests: Verify GC content for various window/step sizes
    - [x] Implement Feature: Core sliding window iterator and calculation
- [x] Task: Implement CpG Island Detection logic [f8892fc]
    - [x] Write Tests: Verify detection criteria against synthetic sequences
    - [x] Implement Feature: Algorithm to identify CpG islands
- [x] Task: Conductor - User Manual Verification 'Core Analysis Logic' (Protocol in workflow.md) [95be8fa]

## Phase 2: CLI and Web Integration
- [x] Task: Add sliding window options to CLI (`main.py`) [5b2ba36]
    - [x] Phase 1: Write Failing Tests (argparse, output logic)
    - [x] Phase 2: Implement CLI enhancements (sliding window & CpG args)
    - [x] Phase 3: Optimize CLI code and error handling
    - [x] Verification: Coverage >90% and Quality Gates
- [x] Task: Integrate features into Web UI (`app.py`) [52fcd6e]
    - [x] Phase 1: Write Failing Tests (Streamlit components and data flow)
    - [x] Phase 2: Implement Web UI features (interactive charts & results)
    - [x] Phase 3: Optimize UI logic and visual clarity
    - [x] Verification: Coverage >90% (Achieved 98%) and Quality Gates
- [x] Task: Conductor - User Manual Verification 'CLI and Web Integration' (Protocol in workflow.md) [Confirmed by user]

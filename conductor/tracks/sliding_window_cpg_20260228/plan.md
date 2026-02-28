# Implementation Plan: Sliding Window and CpG Island Detection

## Phase 1: Core Analysis Logic
- [x] Task: Implement Sliding Window GC calculation [3cbebff]
    - [x] Write Tests: Verify GC content for various window/step sizes
    - [x] Implement Feature: Core sliding window iterator and calculation
- [ ] Task: Implement CpG Island Detection logic
    - [ ] Write Tests: Verify detection criteria against synthetic sequences
    - [ ] Implement Feature: Algorithm to identify CpG islands
- [ ] Task: Conductor - User Manual Verification 'Core Analysis Logic' (Protocol in workflow.md)

## Phase 2: CLI and Web Integration
- [ ] Task: Add sliding window options to CLI (`main.py`)
    - [ ] Write Tests: Verify CLI arguments and output formats
    - [ ] Implement Feature: Update `argparse` and processing loop
- [ ] Task: Integrate features into Web UI (`app.py`)
    - [ ] Write Tests: Verify UI components and data flow
    - [ ] Implement Feature: Add controls and interactive charts
- [ ] Task: Conductor - User Manual Verification 'CLI and Web Integration' (Protocol in workflow.md)

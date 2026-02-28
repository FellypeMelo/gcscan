# Track Specification: Sliding Window and CpG Island Detection

## Overview
Implement advanced genomic analysis features: sliding window analysis for local GC content variation and detection of CpG islands.

## Functional Requirements
- **Sliding Window Analysis:**
    - User can specify window size and step size.
    - Calculate GC content for each window.
    - Visualize local GC content across the sequence.
- **CpG Island Detection:**
    - Identify regions meeting standard CpG island criteria (e.g., length > 200bp, GC > 50%, Obs/Exp CpG > 0.6).
    - Report coordinates and statistics for detected islands.

## Non-Functional Requirements
- **Performance:** Efficiently process large sequences using sliding windows.
- **UI Integration:** Add options to CLI and Web interface.

## Acceptance Criteria
- Sliding window results match manual calculations for test sequences.
- CpG islands correctly identified in known high-GC regions.
- Visualizations clearly show local variations.

import os
import sys
from src.infrastructure.io.fasta import read_fasta
from src.infrastructure.io.exporters import save_results_to_csv
from src.infrastructure.plotting.adapters import plot_gc_distribution
from src.infrastructure.cli.formatter import (
    print_header, print_file_start, print_stats, 
    print_sliding_window_info, print_cpg_islands, print_footer
)
from src.domain.analysis import (
    calculate_gc_percentage, calculate_sliding_window, detect_cpg_islands
)
from src.domain.statistics import calculate_descriptive_stats

def run_analysis(args):
    """Orquestra a análise para os arquivos fornecidos."""
    files = _identify_files(args.input)
    if not files:
        print("Nenhum arquivo FASTA encontrado.")
        return

    print_header(len(files))
    _ensure_dir(args.output_dir)

    for fasta_file in files:
        _process_single_file(fasta_file, args)

    print_footer()

def _identify_files(input_path: str):
    if os.path.isfile(input_path): return [input_path]
    if os.path.isdir(input_path):
        return [os.path.join(input_path, f) for f in os.listdir(input_path)
                if f.lower().endswith(('.fasta', '.fa', '.fna'))]
    return []

def _ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def _process_single_file(file_path: str, args):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    print_file_start(base_name)
    
    results = {}
    for seq_id, sequence in read_fasta(file_path):
        gc = calculate_gc_percentage(sequence)
        results[seq_id] = gc
        
        if args.window:
            step = args.step if args.step else args.window
            sw = calculate_sliding_window(sequence, args.window, step)
            print_sliding_window_info(seq_id, len(sw))
            
        if args.cpg:
            islands = detect_cpg_islands(sequence)
            print_cpg_islands(seq_id, islands)

    if results:
        stats = calculate_descriptive_stats(list(results.values()))
        print_stats(stats)
        
        csv_path = os.path.join(args.output_dir, f"{base_name}_gc.csv")
        save_results_to_csv(results, csv_path)
        
        png_path = os.path.join(args.output_dir, f"{base_name}_gc_analysis.png")
        plot_gc_distribution(results, stats, png_path)

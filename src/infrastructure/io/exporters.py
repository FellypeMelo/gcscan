import csv
from typing import Dict

def save_results_to_csv(results: Dict[str, float], output_path: str):
    """Salva os resultados do cálculo GC em um arquivo CSV."""
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Sequence_ID', 'GC_Content_Percent'])
        for seq_id, gc_value in results.items():
            writer.writerow([seq_id, f"{gc_value:.2f}"])

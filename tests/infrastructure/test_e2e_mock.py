import os
import sys
import pytest
import subprocess
import pandas as pd
from src.domain.analysis import (
    calculate_gc_percentage,
    calculate_sliding_window,
    detect_cpg_islands
)

MOCK_FASTA_PATH = "data/mock_e2e.fasta"

def load_mock_sequence():
    with open(MOCK_FASTA_PATH, "r") as f:
        lines = f.readlines()
    # Skip header and join sequence lines
    return "".join(line.strip() for line in lines[1:])

def test_domain_functions_with_mock():
    """Testa as funções de domínio diretamente usando os dados de mock."""
    sequence = load_mock_sequence()
    
    # 1. GC Global
    # A sequência tem 100bp de 50% GC, 300bp de 100% GC, e 100bp de 0% GC.
    # Total bp = 500
    # Total GC = 50 + 300 + 0 = 350
    # Porcentagem esperada = 350 / 500 = 70.0%
    global_gc = calculate_gc_percentage(sequence)
    assert abs(global_gc - 70.0) < 0.1
    
    # 2. Janela Deslizante
    # Com janela de 100 e passo 100:
    # Janela 1 (0-100): 50% GC
    # Janela 2 (100-200): 100% GC
    # Janela 3 (200-300): 100% GC
    # Janela 4 (300-400): 100% GC
    # Janela 5 (400-500): 0% GC
    windows = calculate_sliding_window(sequence, win_size=100, step=100)
    assert len(windows) == 5
    assert abs(windows[0] - 50.0) < 0.1
    assert abs(windows[1] - 100.0) < 0.1
    assert abs(windows[2] - 100.0) < 0.1
    assert abs(windows[3] - 100.0) < 0.1
    assert abs(windows[4] - 0.0) < 0.1

    # 3. Detecção de Ilha CpG
    # A ilha CpG está na região 100 a 400.
    islands = detect_cpg_islands(sequence, min_len=200, min_gc=50.0, min_oe=0.6)
    assert len(islands) >= 1
    main_island = islands[0]
    assert main_island.start == 58 and main_island.end == 400
    assert main_island.gc_percent >= 50.0

def test_cli_e2e_execution():
    """Testa a execução E2E da CLI com o mock data."""
    output_dir = "results"
    
    # Executa a CLI
    result = subprocess.run(
        [sys.executable, "main.py", MOCK_FASTA_PATH, "--window", "100", "--step", "50", "--cpg"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    assert "Processamento concluído com sucesso!" in result.stdout
    
    # Verifica arquivos gerados
    csv_file = os.path.join(output_dir, "mock_e2e_gc.csv")
    png_file = os.path.join(output_dir, "mock_e2e_gc_analysis.png")
    
    assert os.path.exists(csv_file), f"CSV não encontrado: {csv_file}"
    assert os.path.exists(png_file), f"PNG não encontrado: {png_file}"
    
    # Valida conteúdo do CSV gerado
    df = pd.read_csv(csv_file)
    assert 'Sequence_ID' in df.columns
    assert 'GC_Content_Percent' in df.columns
    assert len(df) >= 1
    assert df['Sequence_ID'].iloc[0] == 'mock_e2e_sequence'
    assert abs(df['GC_Content_Percent'].iloc[0] - 70.0) < 0.1

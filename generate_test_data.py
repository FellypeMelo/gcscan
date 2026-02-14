#!/usr/bin/env python3
"""
GCScan - Gerador de Dados de Teste

Este script gera 50+ conjuntos de dados sintéticos para testar o GCScan.
Os dados são fabricados para cobrir diferentes cenários e variações de GC.

Os dados de teste são COMMITADOS no GitHub para garantir que o projeto
funcione imediatamente após o clone.

Para dados reais, use a pasta data/ (que está no .gitignore)
"""

import random
import os
from datetime import datetime

# Constantes
TEST_DATA_DIR = "test_data"
NUM_DATASETS = 55  # Mais de 50 conforme solicitado
MIN_SEQ_LENGTH = 50
MAX_SEQ_LENGTH = 500


def generate_sequence(length, gc_content_target=None):
    """
    Gera uma sequência de DNA sintética.

    Args:
        length: Comprimento da sequência
        gc_content_target: Target GC content (0.0 a 1.0), None para aleatório

    Returns:
        str: Sequência de DNA
    """
    if gc_content_target is None:
        gc_content_target = random.uniform(0.2, 0.8)

    sequence = []
    for _ in range(length):
        if random.random() < gc_content_target:
            # Adiciona G ou C
            sequence.append(random.choice(["G", "C"]))
        else:
            # Adiciona A ou T
            sequence.append(random.choice(["A", "T"]))

    return "".join(sequence)


def create_fasta_entry(seq_id, sequence, description=""):
    """Cria uma entrada no formato FASTA."""
    if description:
        return f">{seq_id} {description}\n{sequence}\n"
    return f">{seq_id}\n{sequence}\n"


def generate_test_dataset_1_single_sequences():
    """Dataset 1-15: Sequências individuais com diferentes conteúdos GC."""
    datasets = []

    # GC muito baixo (10-20%)
    for i in range(5):
        seq = generate_sequence(random.randint(100, 300), gc_content_target=0.15)
        datasets.append(
            (f"gcscan_test_{i + 1:02d}_very_low_gc", [seq], f"GC content ~15%")
        )

    # GC médio (40-60%)
    for i in range(5, 10):
        seq = generate_sequence(random.randint(100, 300), gc_content_target=0.50)
        datasets.append(
            (f"gcscan_test_{i + 1:02d}_medium_gc", [seq], f"GC content ~50%")
        )

    # GC muito alto (70-80%)
    for i in range(10, 15):
        seq = generate_sequence(random.randint(100, 300), gc_content_target=0.75)
        datasets.append(
            (f"gcscan_test_{i + 1:02d}_very_high_gc", [seq], f"GC content ~75%")
        )

    return datasets


def generate_test_dataset_2_multiple_sequences():
    """Dataset 16-30: Arquivos multi-FASTA com várias sequências."""
    datasets = []

    for i in range(15):
        num_sequences = random.randint(3, 10)
        sequences = []

        for j in range(num_sequences):
            gc_target = random.uniform(0.2, 0.8)
            seq = generate_sequence(random.randint(50, 200), gc_target)
            sequences.append(seq)

        datasets.append(
            (
                f"gcscan_test_{i + 16:02d}_multi_{num_sequences}seqs",
                sequences,
                f"{num_sequences} sequences",
            )
        )

    return datasets


def generate_test_dataset_3_edge_cases():
    """Dataset 31-40: Casos de borda."""
    datasets = []

    # Sequência muito curta (50 bp)
    seq = generate_sequence(50, 0.5)
    datasets.append(("gcscan_test_31_very_short", [seq], "Very short sequence (50bp)"))

    # Sequência muito longa (500 bp)
    seq = generate_sequence(500, 0.5)
    datasets.append(("gcscan_test_32_very_long", [seq], "Very long sequence (500bp)"))

    # GC extremamente baixo (5%)
    seq = generate_sequence(200, 0.05)
    datasets.append(("gcscan_test_33_extreme_low_gc", [seq], "Extreme low GC ~5%"))

    # GC extremamente alto (95%)
    seq = generate_sequence(200, 0.95)
    datasets.append(("gcscan_test_34_extreme_high_gc", [seq], "Extreme high GC ~95%"))

    # GC exatamente 0%
    seq = "".join(random.choice(["A", "T"]) for _ in range(100))
    datasets.append(("gcscan_test_35_zero_gc", [seq], "Zero GC content (only AT)"))

    # GC exatamente 100%
    seq = "".join(random.choice(["G", "C"]) for _ in range(100))
    datasets.append(
        ("gcscan_test_36_100percent_gc", [seq], "100% GC content (only GC)")
    )

    # Muitas sequências curtas
    sequences = [
        generate_sequence(random.randint(30, 50), random.uniform(0.3, 0.7))
        for _ in range(20)
    ]
    datasets.append(("gcscan_test_37_many_short", sequences, "20 short sequences"))

    # Poucas sequências longas
    sequences = [
        generate_sequence(random.randint(300, 400), random.uniform(0.3, 0.7))
        for _ in range(3)
    ]
    datasets.append(("gcscan_test_38_few_long", sequences, "3 long sequences"))

    # Variação extrema de GC no mesmo arquivo
    sequences = [
        generate_sequence(100, 0.1),
        generate_sequence(100, 0.9),
        generate_sequence(100, 0.5),
        generate_sequence(100, 0.2),
        generate_sequence(100, 0.8),
    ]
    datasets.append(
        ("gcscan_test_39_extreme_variation", sequences, "Extreme GC variation")
    )

    # Sequência balanceada
    seq = generate_sequence(200, 0.5)
    datasets.append(("gcscan_test_40_perfect_balance", [seq], "Perfect 50-50 balance"))

    return datasets


def generate_test_dataset_4_realistic_scenarios():
    """Dataset 41-50: Cenários realistas."""
    datasets = []

    # Simulando Plasmodium falciparum (baixo GC ~19%)
    seq = generate_sequence(300, 0.19)
    datasets.append(
        ("gcscan_test_41_plasmodium_like", [seq], "Plasmodium-like (~19% GC)")
    )

    # Simulando Streptomyces (alto GC ~72%)
    seq = generate_sequence(300, 0.72)
    datasets.append(
        ("gcscan_test_42_streptomyces_like", [seq], "Streptomyces-like (~72% GC)")
    )

    # Simulando Humanos (médio GC ~41%)
    seq = generate_sequence(300, 0.41)
    datasets.append(("gcscan_test_43_human_like", [seq], "Human-like (~41% GC)"))

    # Simulando E. coli (médio-alto GC ~51%)
    seq = generate_sequence(300, 0.51)
    datasets.append(("gcscan_test_44_ecoli_like", [seq], "E. coli-like (~51% GC)"))

    # Simulando Mycoplasma (muito baixo GC ~32%)
    seq = generate_sequence(300, 0.32)
    datasets.append(
        ("gcscan_test_45_mycoplasma_like", [seq], "Mycoplasma-like (~32% GC)")
    )

    # Simulando variedade de organelas
    sequences = [
        generate_sequence(150, 0.45),  # Nuclear
        generate_sequence(150, 0.44),  # Mitocondrial
        generate_sequence(150, 0.38),  # Cloroplasto
    ]
    datasets.append(("gcscan_test_46_organelles", sequences, "Mixed organelles"))

    # Simulando genes vs intergênicos
    sequences = [
        generate_sequence(200, 0.55),  # Gene (alto GC)
        generate_sequence(200, 0.35),  # Intergênico (baixo GC)
        generate_sequence(200, 0.52),  # Gene
    ]
    datasets.append(
        ("gcscan_test_47_genes_intergenic", sequences, "Genes vs intergenic")
    )

    # Simulando exons e íntrons
    sequences = [
        generate_sequence(100, 0.53),  # Exon
        generate_sequence(100, 0.42),  # Íntron
        generate_sequence(100, 0.54),  # Exon
    ]
    datasets.append(("gcscan_test_48_exons_introns", sequences, "Exons and introns"))

    # Simulando evolução (sequências relacionadas)
    base_seq = generate_sequence(200, 0.5)
    sequences = [base_seq]
    for _ in range(4):
        # Introduz mutações aleatórias
        seq_list = list(base_seq)
        for _ in range(random.randint(1, 5)):
            pos = random.randint(0, len(seq_list) - 1)
            seq_list[pos] = random.choice(["A", "T", "G", "C"])
        sequences.append("".join(seq_list))
    datasets.append(("gcscan_test_49_evolution", sequences, "Evolutionary variants"))

    # Simulando amostras de metagenômica
    sequences = [
        generate_sequence(random.randint(80, 250), random.uniform(0.2, 0.8))
        for _ in range(8)
    ]
    datasets.append(("gcscan_test_50_metagenomics", sequences, "Metagenomic sample"))

    return datasets


def generate_test_dataset_5_stress_tests():
    """Dataset 51-55: Testes de estresse."""
    datasets = []

    # Muitas sequências (50)
    sequences = [
        generate_sequence(random.randint(50, 100), random.uniform(0.3, 0.7))
        for _ in range(50)
    ]
    datasets.append(
        ("gcscan_test_51_massive_50seqs", sequences, "50 sequences stress test")
    )

    # Sequências muito longas (5 de 1000bp cada)
    sequences = [generate_sequence(1000, random.uniform(0.3, 0.7)) for _ in range(5)]
    datasets.append(
        ("gcscan_test_52_massive_length", sequences, "5 sequences of 1000bp")
    )

    # Alternância extrema AT/GC
    seq = "AT" * 100 + "GC" * 100
    datasets.append(("gcscan_test_53_alternating", [seq], "Alternating AT/GC blocks"))

    # GC gradual
    sequences = [
        generate_sequence(100, 0.2),
        generate_sequence(100, 0.3),
        generate_sequence(100, 0.4),
        generate_sequence(100, 0.5),
        generate_sequence(100, 0.6),
        generate_sequence(100, 0.7),
        generate_sequence(100, 0.8),
    ]
    datasets.append(("gcscan_test_54_gradual_gc", sequences, "Gradual GC increase"))

    # Aleatório puro
    sequences = [generate_sequence(random.randint(50, 300)) for _ in range(10)]
    datasets.append(("gcscan_test_55_random", sequences, "Completely random"))

    return datasets


def save_fasta_files(datasets):
    """Salva os datasets como arquivos FASTA."""
    # Cria diretório se não existir
    os.makedirs(TEST_DATA_DIR, exist_ok=True)

    # Cria arquivo de manifesto
    manifest_path = os.path.join(TEST_DATA_DIR, "MANIFEST.txt")
    with open(manifest_path, "w") as manifest:
        manifest.write("=" * 70 + "\n")
        manifest.write("GCScan - Dados de Teste Sintéticos\n")
        manifest.write("=" * 70 + "\n\n")
        manifest.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        manifest.write(f"Total de datasets: {len(datasets)}\n\n")
        manifest.write("ATENÇÃO: Estes são dados FABRICADOS para teste.\n")
        manifest.write("Para dados reais, use a pasta data/\n\n")
        manifest.write("Lista de arquivos:\n")
        manifest.write("-" * 70 + "\n")

        for filename, sequences, description in datasets:
            filepath = os.path.join(TEST_DATA_DIR, f"{filename}.fasta")

            # Escreve arquivo FASTA
            with open(filepath, "w") as f:
                for i, seq in enumerate(sequences):
                    seq_id = f"{filename}_seq{i + 1}"
                    f.write(create_fasta_entry(seq_id, seq, description))

            # Adiciona ao manifesto
            manifest.write(
                f"{filename}.fasta - {description} ({len(sequences)} seqs)\n"
            )

            print(f"[OK] Gerado: {filename}.fasta ({len(sequences)} sequências)")

    print(f"\n[OK] Manifesto salvo em: {manifest_path}")
    print(f"[OK] Total: {len(datasets)} arquivos FASTA gerados")


def main():
    """Função principal do gerador."""
    print("=" * 70)
    print("GCScan - Gerador de Dados de Teste")
    print("=" * 70)
    print()

    # Coleta todos os datasets
    all_datasets = []
    all_datasets.extend(generate_test_dataset_1_single_sequences())
    all_datasets.extend(generate_test_dataset_2_multiple_sequences())
    all_datasets.extend(generate_test_dataset_3_edge_cases())
    all_datasets.extend(generate_test_dataset_4_realistic_scenarios())
    all_datasets.extend(generate_test_dataset_5_stress_tests())

    # Salva arquivos
    save_fasta_files(all_datasets)

    print()
    print("=" * 70)
    print("Geração concluída!")
    print("=" * 70)
    print(f"\nOs dados de teste estão em: {TEST_DATA_DIR}/")
    print("Estes dados podem ser commitados no GitHub.")
    print("\nPara usar:")
    print(
        f"  python main.py  # ou especifique: test_data/gcscan_test_01_very_low_gc.fasta"
    )


if __name__ == "__main__":
    main()

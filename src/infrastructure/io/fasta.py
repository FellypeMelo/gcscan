from Bio import SeqIO
from typing import Iterator, Tuple

def read_fasta(file_path: str) -> Iterator[Tuple[str, str]]:
    """Lê um arquivo FASTA e retorna um iterador de (id, sequência)."""
    for record in SeqIO.parse(file_path, "fasta"):
        yield record.id, str(record.seq)

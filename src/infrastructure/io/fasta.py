from typing import Iterator, Tuple

def read_fasta(file_path: str) -> Iterator[Tuple[str, str]]:
    """
    Lê um arquivo FASTA e retorna um iterador de (id, sequência).
    Implementação estrita garantindo complexidade espacial O(1) de I/O no parsing,
    bufferizando linha por linha sem instanciar classes pesadas.
    """
    with open(file_path, "r") as handle:
        header = ""
        seq_parts = []
        for line in handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header:
                    yield header, "".join(seq_parts)
                header = line[1:].split()[0]
                seq_parts = []
            else:
                seq_parts.append(line)
        
        # Última sequência
        if header:
            yield header, "".join(seq_parts)

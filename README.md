# GCScan - Analisador de Conteúdo GC (Kernel-Based)

## Descrição

O **GCScan** é uma ferramenta de bioinformática profissional para análise do conteúdo GC (guanina-citosina) em sequências de DNA. Agora estruturado em uma arquitetura de Kernel Modular, garantindo escalabilidade e rigor matemático.

O conteúdo GC é uma métrica fundamental em genética e bioinformática, afetando a estabilidade do DNA, a temperatura de melting e servindo como base para identificação de espécies e predição de genes.

## Funcionalidades

- **Kernel de Análise Puro**: Lógica de cálculo desacoplada de interfaces.
- **Leitura de FASTA**: Suporte robusto via Biopython.
- **Análise Multi-escala**: 
  - Cálculo de GC Global.
  - Análise de Janelas Deslizantes.
  - Detecção de Ilhas CpG.
- **Interfaces Duplas**:
  - **CLI**: Ferramenta de linha de comando para automação.
  - **Web UI**: Dashboard interativo com Streamlit.
- **Visualização Adaptativa**: Gráficos inteligentes baseados no volume de dados.
- **Exportação**: Resultados em CSV e imagens PNG de alta resolução.

## Estrutura do Projeto

```text
gcscan/
├── src/
│   ├── domain/                 # NÚCLEO (Lógica Pura)
│   │   ├── analysis.py         # Algoritmos GC e CpG
│   │   ├── statistics.py       # Estatística Descritiva
│   │   └── models.py           # Objetos de Valor
│   ├── infrastructure/         # SHELLS (Mundo Externo)
│   │   ├── cli/                # Orquestração de Linha de Comando
│   │   ├── web/                # Componentes Streamlit
│   │   ├── io/                 # Leitura de FASTA e Exportadores
│   │   └── plotting/           # Geradores de Gráficos
├── tests/                      # Suíte de Testes (TDD)
├── main.py                     # Ponto de Entrada CLI
├── app.py                      # Ponto de Entrada Web
└── data/                       # Dados Reais (Gitignored)
```

## Instalação

### Pré-requisitos
- Python 3.10+
- pip

### Passos
1. Clone o repositório:
```bash
git clone https://github.com/FellypeMelo/gcscan.git
cd gcscan
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Usar

### Interface de Linha de Comando (CLI)
```bash
# Análise básica
python main.py data/sample.fasta

# Análise completa com janelas e CpG
python main.py data/sample.fasta --window 100 --step 50 --cpg
```

### Interface Web (Streamlit)
```bash
streamlit run app.py
```

## Desenvolvimento (AI-XP)

Este projeto segue o framework **AI-XP** (Artificially Intelligent eXtreme Programming):
- **TDD Mandatório**: Nenhum código entra sem teste verde.
- **Clean Architecture**: Domínio isolado de infraestrutura.
- **SOLID**: Princípios de design estritos para manutenibilidade.

Para rodar os testes:
```bash
$env:PYTHONPATH="."; pytest --cov=src
```

## Licença
Este projeto está licenciado sob a licença MIT.

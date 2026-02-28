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

## Como Usar (Passo a Passo)

O GCScan oferece duas formas de uso: via Interface de Linha de Comando (CLI) para automações ou via Interface Web (Streamlit) para análises visuais iterativas.

### 1. Preparando os Dados
Antes de executar qualquer análise, coloque seus arquivos FASTA (sequências de DNA) na pasta `data/`.
*Dica: Um arquivo de exemplo (`sample.fasta`) já está disponível para testes.*

### 2. Usando a Interface Web (Dashboard)
A interface web é a forma mais interativa de explorar suas sequências.

1. Inicie a aplicação:
   ```bash
   streamlit run app.py
   ```
2. O seu navegador abrirá automaticamente em `http://localhost:8501`.
3. Arraste e solte o seu arquivo `.fasta` na área de upload.
4. Ajuste os parâmetros de análise na barra lateral:
   - **Tamanho da Janela (Window Size):** Define a resolução da análise deslizante.
   - **Tamanho do Passo (Step Size):** Define o avanço da janela.
   - **Detectar Ilhas CpG:** Ative para mapear densidade de dinucleotídeos CG.
5. Os gráficos interativos e resumos estatísticos serão gerados em tempo real na tela.

### 3. Usando a Interface de Linha de Comando (CLI)
A CLI é ideal para processamento em lote ou integração em pipelines de bioinformática.

**Exemplo básico (Cálculo Global):**
```bash
python main.py data/sample.fasta
```

**Exemplo avançado (Janela Deslizante + Detecção CpG):**
```bash
python main.py data/sample.fasta --window 100 --step 50 --cpg
```

**Opções disponíveis:**
- `--window`: Tamanho da janela para análise local (ex: 100).
- `--step`: Tamanho do passo de deslocamento da janela (ex: 50).
- `--cpg`: Flag para ativar a detecção de Ilhas CpG.
- `--output`: Diretório opcional para salvar os resultados (padrão: `results/`).

### 4. Coletando os Resultados
Após a execução via CLI, os resultados serão automaticamente exportados para a pasta `results/`:
- **`[nome_do_arquivo]_gc.csv`**: Arquivo de dados brutos contendo posições, GC% local e status de CpG.
- **`[nome_do_arquivo]_gc_analysis.png`**: Gráfico em alta resolução com a variação do conteúdo GC e marcação das ilhas CpG.

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

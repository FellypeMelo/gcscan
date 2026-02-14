# GCScan - Analisador de Conteúdo GC

## Descrição

O **GCScan** é uma ferramenta de bioinformática para análise do conteúdo GC (guanina-citosina) em sequências de DNA. O conteúdo GC é uma métrica fundamental em genética e bioinformática, pois afeta a estabilidade do DNA, a temperatura de melting e é usado em diversas análises como identificação de espécies, predição de genes e estudos evolutivos.

### O que é Conteúdo GC?

O conteúdo GC representa a porcentagem de bases de guanina (G) e citosina (C) em uma sequência de DNA. Este valor varia entre diferentes organismos e pode fornecer informações importantes sobre:
- Estabilidade estrutural do DNA
- Temperatura de melting (Tm)
- Classificação taxonômica
- Regiões codificantes vs não-codificantes

## Funcionalidades

- **Leitura de FASTA**: Suporte para arquivos no formato FASTA (.fasta, .fa)
- **Cálculo automático**: Calcula o %GC para cada sequência no arquivo
- **Visualização gráfica**: Gera gráficos de barras com Matplotlib
- **Exportação**: Salva resultados em formato de imagem (.png)

## Estrutura de Dados

Este projeto possui **duas pastas** distintas para dados:

### 📁 `test_data/` - Dados Sintéticos (Commitados)
Contém **55+ arquivos FASTA fabricados** automaticamente para testes. Estes dados são:
- ✅ **Commitados no GitHub** (incluídos no repositório)
- 🧪 **Sintéticos** (gerados algoritmicamente)
- 📊 **Variados** (diferentes conteúdos GC, tamanhos, cenários)
- 🎯 **Documentados** (cada arquivo tem propósito específico)

**Como regenerar:**
```bash
python generate_test_data.py
```

### 📁 `data/` - Dados Reais (Gitignored)
Pasta para seus **dados reais de pesquisa**. Por padrão:
- 🚫 **NÃO é commitada** no GitHub (protegida por `.gitignore`)
- 🧬 **Dados reais** do NCBI, sequenciamento, etc.
- 💾 **Arquivos grandes** permitidos
- 🔒 **Privacidade** mantida

**Como usar:**
```bash
# Baixe dados reais do NCBI ou outros bancos
# Salve em data/
python main.py  # Edite o código para apontar para data/seu_arquivo.fasta
```

**Tipos de dados suportados:**
- Nucleotide FASTA (.fasta, .fa, .fna) ← **Recomendado**
- Coding Region (CDS) - Para ORFs específicos
- Multi-FASTA - Múltiplas sequências

## Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. Clone este repositório:
```bash
git clone https://github.com/FellypeMelo/gcscan.git
cd gcscan
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

Ou instale manualmente:
```bash
pip install biopython==1.81 matplotlib==3.7.1
```

## Como Usar

### Uso Básico

1. Coloque seu arquivo FASTA na pasta `data/`:
```bash
mkdir -p data
cp seu_arquivo.fasta data/
```

2. Execute o programa:
```bash
python main.py
```

3. O programa irá:
   - Ler todas as sequências do arquivo
   - Calcular o conteúdo GC de cada uma
   - Exibir os resultados no terminal
   - Gerar um gráfico (`gc_content.png`)

### Formato do Arquivo FASTA

```
>identificador_da_sequencia
ATGCATGCATGCATGCATGCATGC
>outra_sequencia
GGGGCCCCAAAAAAAATTTTGGGG
```

### Exemplo de Saída

```
==================================================
GCScan - Analisador de Conteúdo GC
==================================================

Resultados:
------------------------------
seq1: 50.00%
seq2: 50.00%
seq3: 0.00%

Gráfico salvo em: gc_content.png

Análise concluída!
```

## Estrutura do Projeto

```
gcscan/
├── main.py              # Código principal
├── requirements.txt     # Dependências
├── README.md           # Documentação
└── data/
    └── sample.fasta    # Arquivo de exemplo
```

## Guia de Desenvolvimento

### Milestones do Projeto

#### Milestone 1: Funcionalidades Básicas ✅
- [x] Leitura de arquivos FASTA
- [x] Cálculo de conteúdo GC
- [x] Geração de gráficos simples
- [x] Documentação inicial

#### Milestone 2: Melhorias de Interface 🚧
- [ ] Suporte a argumentos de linha de comando (argparse)
- [ ] Opção de saída em formato CSV/TSV
- [ ] Interface web simples (Streamlit)
- [ ] Suporte a múltiplos arquivos simultâneos

#### Milestone 3: Análises Avançadas 📊
- [ ] Análise de janelas deslizantes (sliding window)
- [ ] Detecção de ilhas CpG
- [ ] Comparação entre múltiplas amostras
- [ ] Estatísticas descritivas (média, mediana, desvio padrão)

#### Milestone 4: Integração e Automação 🔄
- [ ] Pipeline com outros módulos (FastaFlow)
- [ ] Suporte a processamento em lote
- [ ] Geração de relatórios PDF
- [ ] API REST para análise remota

### Tarefas para Contribuidores

**Nível Iniciante:**
1. Adicionar tratamento de erros para arquivos mal formatados
2. Implementar logging em vez de print
3. Criar testes unitários simples

**Nível Intermediário:**
1. Adicionar suporte a arquivos multi-FASTA grandes (>1GB)
2. Implementar análise de janelas deslizantes
3. Criar visualizações interativas (Plotly)

**Nível Avançado:**
1. Implementar análise paralela com multiprocessing
2. Criar interface web completa
3. Adicionar suporte a RNA (uracila) e proteínas

## Algoritmo

O cálculo do conteúdo GC segue a fórmula:

```
GC% = (número de G + número de C) / comprimento total × 100
```

Implementação no código:
```python
gc_fraction = (count(G) + count(C)) / len(sequence)
gc_percent = gc_fraction * 100
```

## Exemplos de Aplicação

### 1. Identificação de Bactérias
Bactérias com alto conteúdo GC (>60%) vs baixo conteúdo GC (<40%):
- *Streptomyces coelicolor*: ~72% GC
- *Mycoplasma genitalium*: ~32% GC

### 2. Predição de Regiões Codificantes
Regiões codificantes geralmente têm conteúdo GC diferente de regiões não-codificantes.

### 3. Estudos de Evolução
Comparação do conteúdo GC entre espécies relacionadas pode revelar padrões evolutivos.

## Próximos Passos Recomendados

1. **Implementar argparse**: Permitir especificar arquivo de entrada via linha de comando
2. **Adicionar exportação CSV**: Facilitar análise em outras ferramentas
3. **Criar testes**: Garantir que o cálculo está correto
4. **Documentar funções**: Adicionar docstrings mais detalhadas
5. **Criar notebook Jupyter**: Demonstrar uso com visualizações interativas

## Referências

- [Biopython Documentation](https://biopython.org/wiki/Documentation)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [FASTA Format](https://en.wikipedia.org/wiki/FASTA_format)
- [GC Content in Bioinformatics](https://www.ncbi.nlm.nih.gov/pmc/articles/PMCPMC2827198/)

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Contato

Para dúvidas ou sugestões, abra uma issue no GitHub.

---

**Status**: 🟢 Funcional - Pronto para uso e expansão
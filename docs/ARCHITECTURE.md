# GCScan v2.0 - Documentação de Arquitetura (C4 Model)

Este documento mapeia o coração da arquitetura técnica do GCScan, guiada imperativamente pelos princípios de Clean Architecture, AI-XP e abstrações seguras para a versão de Alta Performance.

## 1. Contexto do Sistema (Nível 1)
Descreve as interações em alto nível do analisador e o papel do domínio.

```mermaid
C4Context
  title GCScan - Diagrama de Contexto de Sistema

  Person(bioinfo, "Bioinformata", "Pesquisador executando análises massivas de Genomas")
  System(gcscan, "GCScan Analyzer", "Analisador Genômico de Conteúdo GC focado em Alta Performance e Alta Eficiência.")

  Rel(bioinfo, gcscan, "Envia arquivos FASTA multi-gigabyte e parâmetros de varredura.")
```

## 2. Diagrama de Containers (Nível 2)
Expansão das responsabilidades focada em manter a **Dependency Inversion**. Infraestruturas dependem do Núcleo, o Núcleo nunca conhece a ponta.

```mermaid
C4Container
  title GCScan - Diagrama de Containers

  Person(bioinfo, "Bioinformata", "Usuário")
  
  System_Boundary(c1, "Aplicações GCScan") {
    Container(cli, "CLI Orchestrator", "Python Argparse", "Processa requisições via terminal e despacha caminhos ou pipelines automatizados.")
    Container(web, "Streamlit Dashboard", "Python/Streamlit", "Interface interativa para pesquisadores operarem visualmente sobre pequenas escalas.")
    Container(core, "GCScan Engine", "Python Puro + Multiprocessing", "Módulo de domínio totalmente limpo e isolado; orquestra divisão via CPU.")
  }

  System_Ext(filesystem, "S.O File System", "Arquivos .fasta (Entrada) e .csv/.png (Saída)")

  Rel(bioinfo, cli, "Dispara via terminal bash/zsh")
  Rel(bioinfo, web, "Analisa relatórios online via navegador")
  Rel(cli, filesystem, "Lê FASTA / Exporta arquivos", "File I/O")
  Rel(cli, core, "Repassa metadados em Memória RAM para varredura")
  Rel(web, core, "Repassa Dataframes para as plotagens gráficas")
```

## 3. Diagrama de Componentes (Nível 3)
Detalhando o GCScan Engine e como o sistema distribui a carga da versão 2.0 (Multiprocessing FASTA Parser).

```mermaid
C4Component
  title GCScan Engine - Diagrama de Componentes Internos

  Container_Boundary(core_engine, "GCScan Engine (src/domain)") {
    Component(analyser, "Algoritmos Cpg/GC", "Python / Math", "Varre sequências DNA e atua matematicamente através de lógica pura e TDD forte.")
    Component(stats, "Stats Analyzer", "Python", "Estatísticas Descritivas globais sobre a malha.")
    Component(models, "Value Objects", "Python dataclasses", "Entidades puras (ex: CpGIsland) garantindo abstração tipada forte.")
  }
  
  Container_Boundary(infra_engine, "Infraestrutura CPL (src/infrastructure)") {
    Component(parallel, "Chunked FASTA Reader", "Python (concurrent.futures)", "Gerenciador Multiprocessing: Separa e envia blocos estritos independentes aos Cores Reais.")
    Component(biopython, "File IO adapter", "Python (Bio)", "Carrega os iteradores nativos lendo do Big Data minimizando carga de disco.")
    
    Rel(parallel, analyser, "Transmite carga estritamente através das fronteiras", "CPU Isolada")
    Rel(parallel, biopython, "Invoca Iterador", "Ponteiro Seq")
  }
  
  Rel(analyser, models, "Emite Data Transfer objects")
  Rel(analyser, stats, "Processa Variâncias e Desvio Padrões")

```

## Aderência a Regras (Zero Vibe Coding)
1. **Domínio Independente**: Nenhuma seta do componente `GCScan Engine` sai para o File System, Bibliotecas de Plots, ou Protocolos de Rede. Essa barreira lógica é garantida no Continuous Integration através da validação AST.
2. **Economia I/O**: `Chunked FASTA Reader` distribui cópias particionadas nas instâncias de Multiprocess sem estourar o limite de `memory/RAM`.

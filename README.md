# ⚡ Balta.io — IA Generativa, Busca Vetorial & Agentes com C# / .NET

<div align="center">

![Balta.io](https://img.shields.io/badge/Plataforma-balta.io-7928CA?style=for-the-badge&logo=dotnet&logoColor=white)
![.NET](https://img.shields.io/badge/.NET-10%20%2F%209%20%2F%208-512BD4?style=for-the-badge&logo=dotnet&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Vector%20DB-PostgreSQL%20%2B%20pgvector-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Ollama](https://img.shields.io/badge/Local%20LLM-Ollama%20(Phi--3)-black?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Treinamento%20T%C3%A9cnico%20Pr%C3%A1tico-brightgreen?style=for-the-badge)

</div>

Repositório prático de treinamento técnico avançado em **Inteligência Artificial Generativa, Busca Vetorial, RAG e Agentes Autônomos em C#**, baseado nas trilhas e formações práticas da plataforma **[balta.io](https://balta.io)** ministradas por André Baltieri (13x Microsoft MVP).

---

## 🎯 Objetivo & Foco do Repositório

Diferente de cursos meramente conceituais, este repositório é focado em **engenharia e código executável de ponta a ponta**:
- Execução de **modelos locais de IA (SLMs e Embeddings via Ollama + Phi-3)**, com zero custo de tokens e total privacidade.
- Modelagem e persistência de dados vetoriais com **PostgreSQL + pgvector** utilizando **Entity Framework Core**.
- Integração nativa e tipada com **OllamaSharp**.
- Adoção das novas abstrações unificadas do ecossistema .NET: **`Microsoft.Extensions.AI`** e **`Microsoft.Extensions.VectorData`**.
- Orquestração de prompts, memórias e agentes inteligentes com **Semantic Kernel**.

---

## 🧭 Mapa de Módulos & Laboratórios

| # | Módulo | Foco Técnico | Status | Link |
| :-: | :--- | :--- | :-: | :---: |
| **01** | **Setup Ollama & Modelo Phi-3** | Infraestrutura local de IA, instalação do Ollama, download do `phi3`, testes de API e Docker Compose | 🚀 Pronto | [Acessar](modules/01-setup-ollama-phi3/) |
| **02** | **Busca Vetorial com pgvector & EF Core** | Criação de tabelas com colunas `Vector`, extensões PostgreSQL, mapeamento com EF Core e consultas por distância de cosseno | 🚀 Pronto | [Acessar](modules/02-busca-vetorial-pgvector-efcore/) |
| **03** | **OllamaSharp & Microsoft.Extensions.AI** | Cliente tipado C# para Ollama, contratos `IChatClient`, `IEmbeddingGenerator` e abstração de provedores | 🚀 Pronto | [Acessar](modules/03-ollamasharp-e-microsoft-extensions-ai/) |
| **04** | **Semantic Kernel: RAG & Plugins** | Orquestração de IA com Semantic Kernel, injeção de dependência, plugins nativos e pipeline de RAG | 🚀 Pronto | [Acessar](modules/04-semantic-kernel-rag-plugins/) |
| **05** | **Agentes Autônomos em .NET** | Criação de agentes inteligentes com tomada de decisão, chamadas de funções (function calling) e persistência de histórico | 🚀 Pronto | [Acessar](modules/05-agentes-autonomos-dotnet/) |

---

## 🛠️ Stack Tecnológica

- **Linguagem & Runtime:** C# (.NET 10 / 9 / 8)
- **Banco Vetorial:** PostgreSQL 16 + extensão `pgvector`
- **Inferência & Embeddings Locais:** Ollama (`phi3` / `nomic-embed-text`)
- **Bibliotecas .NET:**
  - `OllamaSharp`
  - `Pgvector.EntityFrameworkCore` & `Npgsql.EntityFrameworkCore.PostgreSQL`
  - `Microsoft.Extensions.AI` & `Microsoft.Extensions.VectorData`
  - `Microsoft.SemanticKernel`
- **Ferramental Interno:** `tools/knowledge-extractor/` (transcrição acelerada via Whisper, extração de texto de PDFs e normalização de mídias com De-Para)
- **Containerização:** Docker & Docker Compose

---

## 🚀 Como Executar o Ambiente Local

### 1. Subir a Infraestrutura (PostgreSQL com pgvector + Ollama)
```bash
docker compose -f docker/docker-compose.yml up -d
```

### 2. Baixar o Modelo Local no Ollama
Se estiver rodando via Docker:
```bash
docker exec -it balta-ollama ollama pull phi3
```
Se estiver rodando o Ollama nativo no host:
```bash
ollama pull phi3
```

### 3. Compilar e Executar a Solução C#
```bash
cd src
dotnet build Balta.IA.slnx
dotnet run --project 01-OllamaSharp.Basics
```

---

## 🎧 Ferramenta de Extração de Conhecimento (`tools/knowledge-extractor`)

Este repositório inclui a suite para transcrição e processamento dos materiais do treinamento:

```bash
# Transcrever vídeo/áudio de aula (gera .txt e legendas .srt)
uv run --project tools/knowledge-extractor knowledge-extractor transcribe caminho/aula.mp4 -o modules/01-setup-ollama-phi3/materiais/transcricoes/

# Processar todo o material bruto de um módulo (processa arquivos em materiais/raw/)
uv run --project tools/knowledge-extractor knowledge-extractor process-module modules/01-setup-ollama-phi3

# Extrair texto estruturado de PDFs/slides
uv run --project tools/knowledge-extractor knowledge-extractor extract-pdf docs/material.pdf -o docs/
```

---

## 📂 Estrutura de Diretórios

```text
balta/
├── .agent-kit/                # Personas especializadas e padrões do ecossistema
├── .antigravity/              # Instruções para Antigravity IDE & agy
├── .github/                   # Instruções de Copilot e automações
├── .verify                    # Token de vinculação oficial da plataforma balta.io
├── docker/
│   ├── docker-compose.yml     # PostgreSQL + pgvector + Ollama
│   └── init-pgvector.sql      # Script de inicialização do pgvector
├── docs/                      # Guias de arquitetura e setup
├── modules/                   # Módulos práticos (aulas, labs, materiais raw/transcrições)
├── src/                       # Solução .NET com os projetos práticos
│   ├── Balta.IA.slnx
│   ├── 01-OllamaSharp.Basics/
│   ├── 02-PgVector.EFCore/
│   ├── 03-MicrosoftExtensionsAI.Sample/
│   └── 04-SemanticKernel.RagAgent/
└── tools/knowledge-extractor/ # Suite Python (uv) para transcrição e extração
```
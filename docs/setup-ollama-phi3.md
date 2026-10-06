# 🦙 Setup do Ollama & Modelo Phi-3

Guia passo a passo para execução do ambiente local de inferência e geração de embeddings com **Ollama** e **Phi-3**.

---

## 1. O que é o Ollama?
O [Ollama](https://ollama.com/) é uma ferramenta de código aberto que permite executar modelos de linguagem (LLMs e SLMs) e modelos de embeddings diretamente na sua máquina local, com suporte a GPU e CPU, expondo uma API REST compatível.

---

## 2. Opções de Execução

### Opção A: Execução Nativa no Windows (Recomendada)
1. Baixe o instalador oficial em [ollama.com/download/windows](https://ollama.com/download/windows).
2. Conclua a instalação padrão.
3. Abra o terminal (PowerShell ou Git Bash) e baixe o modelo Phi-3:
   ```bash
   ollama pull phi3
   ```
4. Teste a execução do modelo:
   ```bash
   ollama run phi3 "Olá, explique em 2 linhas o que é busca vetorial."
   ```

### Opção B: Execução via Docker Compose
No diretório raiz deste repositório, execute:
```bash
docker compose -f docker/docker-compose.yml up -d
```
Para baixar o modelo dentro do container:
```bash
docker exec -it balta-ollama ollama pull phi3
```

---

## 3. Endpoints da API Local

Por padrão, o Ollama roda na porta `11434`:
- **Base URL:** `http://localhost:11434`
- **Embeddings:** `POST http://localhost:11434/api/embeddings`
- **Chat:** `POST http://localhost:11434/api/chat`
- **Tags (Modelos locais instalados):** `GET http://localhost:11434/api/tags`

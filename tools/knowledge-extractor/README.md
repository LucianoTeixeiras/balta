# 🛠️ Knowledge Extractor — MBA UNIPDS

Ferramenta CLI interna do repositório para extração, transcrição e governança de materiais de estudo:
- **Normalização de Arquivos e Auditoria De-Para**: Padronização de vídeos e PDFs para convenção *kebab-case* com sincronização de transcrições e registro persistente em `docs/logs/file-renaming-audit.json` e `docs/logs/file-renaming-audit.md`.
- **Vídeos e Áudios (`.mp4`, `.mkv`, `.mp3`, etc.)**: Extração de áudio via `ffmpeg` e transcrição acelerada com `faster-whisper` em PT-BR (gerando `.txt` e legendas `.srt` com timestamps e log em tempo real).
- **Apostilas e Slides (`.pdf`)**: Extração de texto e estruturação página a página em Markdown (`.md`).

---

## 🚀 Como Usar (via `uv`)

Como todas as dependências e o ambiente virtual são gerenciados pelo `uv`, você pode executar os comandos a partir da raiz do repositório ou de dentro da pasta `tools/knowledge-extractor`:

### 1. Normalizar nomes de arquivos de um módulo (com auditoria De-Para):
```bash
# Simulação prévia (Dry-Run sem alterar nada)
uv run --project tools/knowledge-extractor knowledge-extractor normalize-files modules/01-fundamentos-ia-llms

# Aplicação real das renomeações e gravação do log de auditoria
uv run --project tools/knowledge-extractor knowledge-extractor normalize-files modules/01-fundamentos-ia-llms --apply
```

### 2. Consultar o histórico de auditoria De-Para:
```bash
# Exibir todos os registros
uv run --project tools/knowledge-extractor knowledge-extractor audit-log

# Buscar por palavra-chave específica (ex: "teachable", "erick-wendel", "ppc")
uv run --project tools/knowledge-extractor knowledge-extractor audit-log --search "teachable"
```

### 3. Processar todo o material bruto de um módulo:
Processa automaticamente todos os vídeos e PDFs presentes em `modules/<modulo>/materiais/raw/` e grava as saídas em `modules/<modulo>/materiais/transcricoes/`:
```bash
uv run --project tools/knowledge-extractor knowledge-extractor process-module modules/01-fundamentos-ia-llms
```

### 4. Transcrever um arquivo de vídeo ou áudio específico:
```bash
uv run --project tools/knowledge-extractor knowledge-extractor transcribe caminho/para/aula-01.mp4 -o modules/01-fundamentos-ia-llms/materiais/transcricoes/
```

### 5. Extrair conteúdo de um PDF específico:
```bash
uv run --project tools/knowledge-extractor knowledge-extractor extract-pdf docs/ementa.pdf -o docs/
```

---

## ⚙️ Opções Disponíveis

- `-m, --model-size`: Tamanho do modelo Whisper (`tiny`, `base`, `small`, `medium`, `large-v3`). Padrão: `base`.
- `-d, --device`: `auto`, `cpu` ou `cuda`. Padrão: `auto` (detecta GPU automaticamente se disponível).
- `-l, --language`: Código do idioma. Padrão: `pt`.
- `-f, --force`: Força o reprocessamento de mídias/PDFs que já foram transcritos.
- `--apply`: Aplica as renomeações do comando `normalize-files`.

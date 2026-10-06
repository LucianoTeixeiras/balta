"""Interface de linha de comando para o Knowledge Extractor."""

from __future__ import annotations

import sys
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table

from knowledge_extractor.audio_transcriber import Transcriber
from knowledge_extractor.file_normalizer import FileNormalizer
from knowledge_extractor.pdf_parser import extract_text_from_pdf

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console(highlight=False)


@click.group()
def cli() -> None:
    """Ferramenta de extração de conhecimento (transcrição de vídeos e leitura de PDFs) para o MBA UNIPDS."""
    pass


@cli.command("normalize-files")
@click.argument("module_dir", type=click.Path(exists=True, path_type=Path))
@click.option("--apply", "apply_changes", is_flag=True, default=False, help="Aplica as renomeações e grava no log de auditoria")
def normalize_files_cmd(module_dir: Path, apply_changes: bool) -> None:
    """Normaliza nomes de arquivos em materiais/raw/ e materiais/transcricoes/ gerando log de auditoria De-Para."""
    normalizer = FileNormalizer()
    normalizer.execute_normalization(module_dir, dry_run=not apply_changes)


@cli.command("audit-log")
@click.option("-s", "--search", default=None, help="Filtra o log por termo de busca (nome antigo, novo ou módulo)")
def audit_log_cmd(search: str | None) -> None:
    """Exibe o histórico de auditoria de arquivos renomeados (De-Para)."""
    normalizer = FileNormalizer()
    records = normalizer.load_audit_log()

    if not records:
        console.print("[yellow]ℹ Nenhum registro de auditoria encontrado.[/yellow]")
        return

    if search:
        search_lower = search.lower()
        records = [
            r for r in records
            if search_lower in r.get("old_name", "").lower()
            or search_lower in r.get("new_name", "").lower()
            or search_lower in r.get("module", "").lower()
            or search_lower in r.get("sha256", "").lower()
        ]

    table = Table(title=f"Histórico de Auditoria De-Para ({len(records)} registros)")
    table.add_column("Data (UTC)", style="dim")
    table.add_column("Módulo", style="cyan")
    table.add_column("De (Original)", style="magenta")
    table.add_column("Para (Normalizado)", style="bold green")
    table.add_column("Tipo", style="yellow")
    table.add_column("SHA-256", style="dim")

    for r in records:
        ts = r.get("timestamp", "").replace("T", " ").split(".")[0]
        sha = (r.get("sha256") or "")[:8]
        table.add_row(ts, r.get("module", "-"), r.get("old_name", "-"), r.get("new_name", "-"), r.get("type", "-"), sha)

    console.print(table)


@cli.command("transcribe")
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option("-o", "--output-dir", type=click.Path(path_type=Path), default=None, help="Diretório de saída para .txt e .srt")
@click.option("-m", "--model-size", default="base", help="Tamanho do modelo Whisper (tiny, base, small, medium, large-v3)")
@click.option("-d", "--device", default="auto", help="Device de execução ('cpu', 'cuda' ou 'auto')")
@click.option("-l", "--language", default="pt", help="Idioma do áudio (ex: pt, en)")
def transcribe_cmd(
    input_file: Path,
    output_dir: Path | None,
    model_size: str,
    device: str,
    language: str,
) -> None:
    """Transcreve um arquivo de vídeo (.mp4, .mkv) ou áudio (.mp3, .wav)."""
    transcriber = Transcriber(model_size=model_size, device=device, language=language)
    transcriber.transcribe_file(input_file, output_dir=output_dir)


@cli.command("extract-pdf")
@click.argument("pdf_file", type=click.Path(exists=True, path_type=Path))
@click.option("-o", "--output-dir", type=click.Path(path_type=Path), default=None, help="Diretório de saída para .md")
@click.option("--as-text", is_flag=True, default=False, help="Salva como .txt simples ao invés de Markdown estruturado")
def extract_pdf_cmd(
    pdf_file: Path,
    output_dir: Path | None,
    as_text: bool,
) -> None:
    """Extrai texto e páginas de um arquivo PDF."""
    extract_text_from_pdf(pdf_file, output_dir=output_dir, as_markdown=not as_text)


@cli.command("process-module")
@click.argument("module_dir", type=click.Path(exists=True, path_type=Path))
@click.option("-m", "--model-size", default="base", help="Tamanho do modelo Whisper (tiny, base, small, medium, large-v3)")
@click.option("-f", "--force", is_flag=True, default=False, help="Força o reprocessamento de arquivos já extraídos")
def process_module_cmd(module_dir: Path, model_size: str, force: bool) -> None:
    """Processa todos os arquivos em `materiais/raw/` de um módulo e gera saídas em `materiais/transcricoes/`."""
    raw_dir = module_dir / "materiais" / "raw"
    transcricoes_dir = module_dir / "materiais" / "transcricoes"

    if not raw_dir.exists():
        console.print(f"[red]❌ Diretório raw não encontrado:[/red] {raw_dir}")
        return

    transcricoes_dir.mkdir(parents=True, exist_ok=True)

    media_extensions = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".wav", ".mp3", ".m4a"}
    pdf_extensions = {".pdf"}

    all_files = [p for p in raw_dir.iterdir() if p.is_file() and not p.name.startswith(".")]

    if not all_files:
        console.print(f"[yellow]ℹ Nenhum arquivo encontrado em:[/yellow] {raw_dir}")
        return

    table = Table(title=f"Arquivos em {module_dir.name} (materiais/raw)")
    table.add_column("Arquivo", style="cyan")
    table.add_column("Tipo", style="magenta")
    table.add_column("Tamanho", justify="right")
    table.add_column("Status", style="green")

    pending_media: list[Path] = []
    pending_pdf: list[Path] = []

    for f in all_files:
        size_mb = f.stat().st_size / (1024 * 1024)
        ext = f.suffix.lower()
        stem = f.stem
        is_media = ext in media_extensions
        is_pdf = ext in pdf_extensions
        tipo = "Vídeo/Áudio" if is_media else ("PDF" if is_pdf else "Outro")

        if is_media:
            txt_exists = (transcricoes_dir / f"{stem}.txt").exists()
            srt_exists = (transcricoes_dir / f"{stem}.srt").exists()
            if not force and txt_exists and srt_exists:
                status = "[dim]Já transcrito (Skip)[/dim]"
            else:
                status = "[bold yellow]Pendente[/bold yellow]"
                pending_media.append(f)
        elif is_pdf:
            md_exists = (transcricoes_dir / f"{stem}.md").exists()
            if not force and md_exists:
                status = "[dim]Já extraído (Skip)[/dim]"
            else:
                status = "[bold yellow]Pendente[/bold yellow]"
                pending_pdf.append(f)
        else:
            status = "[dim]Ignorado[/dim]"

        table.add_row(f.name, tipo, f"{size_mb:.1f} MB", status)

    console.print(table)

    # Processa mídias pendentes
    if pending_media:
        transcriber = Transcriber(model_size=model_size, device="auto", language="pt")
        for media in pending_media:
            transcriber.transcribe_file(media, output_dir=transcricoes_dir)

    # Processa PDFs pendentes
    for pdf in pending_pdf:
        extract_text_from_pdf(pdf, output_dir=transcricoes_dir, as_markdown=True)

    console.print(f"[bold green]✨ Processamento concluído com sucesso![/bold green]")


def main() -> None:
    cli()


if __name__ == "__main__":
    main()

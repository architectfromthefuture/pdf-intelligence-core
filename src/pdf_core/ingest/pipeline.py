"""Phase 1: inbox → Markdown + audit."""

from pathlib import Path

from pdf_core.config import Settings, load_settings, repo_root
from pdf_core.ingest.extract import extract
from pdf_core.ingest.normalize import normalize
from pdf_core.ingest.validate import validate_pdf
from pdf_core.storage.audit import write_audit


def process_file(pdf_path: Path, *, settings: Settings | None = None) -> None:
    settings = settings or load_settings()
    meta = validate_pdf(pdf_path)

    if not meta["valid"]:
        print(f"[REJECTED] {pdf_path.name} → {meta['error']}")
        write_audit(
            {
                "file": pdf_path.name,
                "status": "rejected",
                "error": meta["error"],
            },
            settings.audit,
            pdf_path.stem,
        )
        return

    result = extract(pdf_path)
    cleaned = normalize(result["text"])

    settings.markdown.mkdir(parents=True, exist_ok=True)

    md_path = settings.markdown / f"{pdf_path.stem}.md"
    md_path.write_text(cleaned, encoding="utf-8")

    audit = {
        "file": pdf_path.name,
        "hash": meta["hash"],
        "pages": meta["pages"],
        "extractor": result["method"],
        "status": "success",
        "output": str(md_path.relative_to(repo_root())),
    }

    if "fallback_reason" in result:
        audit["fallback_reason"] = result["fallback_reason"]

    write_audit(audit, settings.audit, pdf_path.stem)

    print(f"[OK] {pdf_path.name}")


def run_pipeline(*, settings: Settings | None = None) -> None:
    settings = settings or load_settings()
    settings.inbox.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(settings.inbox.glob("*.pdf"))

    if not pdfs:
        print("No PDFs found in data/inbox/")
        return

    for pdf in pdfs:
        process_file(pdf, settings=settings)

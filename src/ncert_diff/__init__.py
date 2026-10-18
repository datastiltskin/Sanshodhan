"""Track changes between editions of NCERT textbooks."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_FILE = REPO_ROOT / "sources.yaml"
PDF_DIR = REPO_ROOT / "pdfs"
MANIFEST_DIR = REPO_ROOT / "manifest"
TEXTS_DIR = REPO_ROOT / "texts"

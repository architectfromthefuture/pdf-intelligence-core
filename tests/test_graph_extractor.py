import json

import pdf_core.graph.pipeline as mgp
import pdf_core.graph.store as st
import pdf_core.graph.trace as gtrace
from pdf_core.graph.builder import build_relations
from pdf_core.graph.extractor import extract_entities
from pdf_core.graph.pipeline import run_graph_pipeline


def test_extract_entities_regex():
    text = "We discussed New York Times and also Microsoft Word today."
    got = extract_entities(text)
    assert got["method"] == "regex_capital_phrase"
    assert "New York Times" in got["entities"]


def test_build_relations_pairwise():
    edges = build_relations(["A", "B", "C"], "doc:chunk_0000")
    assert len(edges) == 3
    assert {e["relation"] for e in edges} == {"co_occurs_in"}
    assert all(e["source_chunk_id"] == "doc:chunk_0000" for e in edges)


def test_pipeline_writes_graph_artifacts(monkeypatch, tmp_path):

    def root():
        return tmp_path

    monkeypatch.setattr(mgp, "repo_root", root)
    monkeypatch.setattr(st, "repo_root", root)
    monkeypatch.setattr(gtrace, "repo_root", root)

    (tmp_path / "data/chunks").mkdir(parents=True)
    payload = {
        "doc_id": "demo",
        "chunks": [
            {
                "chunk_id": "chunk_0000",
                "text": "New York Times reported on United States policy.",
                "start_word": 0,
                "end_word": 8,
            },
        ],
        "strategy": "fixed_word_window",
        "chunk_size": 500,
        "total_chunks": 1,
    }
    (tmp_path / "data/chunks/demo.json").write_text(json.dumps(payload), encoding="utf-8")

    run_graph_pipeline()

    assert (tmp_path / "data/graphs/nodes.json").exists()
    assert (tmp_path / "data/graphs/edges.json").exists()
    assert (tmp_path / "data/graphs/graph_index.json").exists()
    assert (tmp_path / "data/graphs/traces").is_dir()

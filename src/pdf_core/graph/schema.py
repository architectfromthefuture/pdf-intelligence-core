from dataclasses import dataclass


@dataclass
class Node:
    id: str
    label: str
    source_chunk_id: str


@dataclass
class Edge:
    id: str
    source: str
    target: str
    relation: str
    source_chunk_id: str

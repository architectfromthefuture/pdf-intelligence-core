"""Phase 1: normalize extractor output."""

import re


def normalize(text: str) -> str:
    text = re.sub(r"-\n", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    lines = [line.rstrip() for line in text.split("\n")]

    cleaned: list[str] = []
    seen: set[str] = set()

    for line in lines:
        key = line.strip()
        if key and key not in seen:
            cleaned.append(line)
            seen.add(key)

    return "\n".join(cleaned).strip()

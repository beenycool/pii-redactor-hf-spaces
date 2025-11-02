"""Utility helpers for text chunking and PII tag management."""

from __future__ import annotations

import re
from collections import Counter
from typing import Dict, Iterable, List, Tuple

from api_client import PIIEntity


_SENTENCE_BOUNDARY_PATTERN = re.compile(r"(?<=[.!?])\s")


def chunk_text(text: str, max_chars: int = 400) -> List[str]:
    """Split text into chunks not exceeding *max_chars* without cutting words.

    Prefers to split on sentence boundaries. Falls back to whitespace if
    necessary. Leading/trailing whitespace is stripped from each chunk.
    """

    if max_chars <= 0:
        raise ValueError("max_chars must be positive")

    clean_text = text.strip()
    if not clean_text:
        return []

    if len(clean_text) <= max_chars:
        return [clean_text]

    chunks: List[str] = []
    start = 0
    length = len(clean_text)

    while start < length:
        provisional_end = min(start + max_chars, length)
        window = clean_text[start:provisional_end]

        if provisional_end == length:
            chunk = clean_text[start:length].strip()
            if chunk:
                chunks.append(chunk)
            break

        sentence_break = None
        for match in _SENTENCE_BOUNDARY_PATTERN.finditer(window):
            sentence_break = match.end()

        if sentence_break:
            end = start + sentence_break
        else:
            last_space = window.rfind(" ")
            if last_space == -1:
                end = provisional_end
            else:
                end = start + last_space

        chunk = clean_text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end
        while start < length and clean_text[start].isspace():
            start += 1

    return chunks


def _normalise_category(category: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", category.upper()).strip("_") or "UNKNOWN"


class PIITagManager:
    """Bidirectional mapping between PII tags and their original values."""

    def __init__(self) -> None:
        self._tag_to_value: Dict[str, str] = {}
        self._value_to_tag: Dict[Tuple[str, str], str] = {}
        self._counters: Counter[str] = Counter()

    @property
    def mapping(self) -> Dict[str, str]:
        """Expose the current tag to value mapping."""

        return dict(self._tag_to_value)

    def register(self, category: str, value: str) -> str:
        """Return an existing tag for (category, value) or create a new one."""

        normalised_category = _normalise_category(category)
        key = (normalised_category, value)
        if key in self._value_to_tag:
            return self._value_to_tag[key]

        self._counters[normalised_category] += 1
        tag = f"<PII_{normalised_category}_{self._counters[normalised_category]}>"
        self._value_to_tag[key] = tag
        self._tag_to_value[tag] = value
        return tag

    def replace_in_text(
        self, text: str, entities: Iterable[PIIEntity]
    ) -> Tuple[str, Dict[str, str]]:
        """Replace entity values within *text* with their corresponding tags."""

        replacements: List[Tuple[str, str]] = []
        for entity in entities:
            if not entity.value:
                continue
            tag = self.register(entity.type, entity.value)
            replacements.append((entity.value, tag))

        redacted = text
        for value, tag in sorted(replacements, key=lambda item: len(item[0]), reverse=True):
            pattern = re.escape(value)
            redacted = re.sub(pattern, tag, redacted)

        return redacted, self.mapping

    def restore_text(self, text: str) -> str:
        """Restore original values into *text* by replacing tags."""

        restored = text
        for tag, value in self._tag_to_value.items():
            restored = restored.replace(tag, value)
        return restored



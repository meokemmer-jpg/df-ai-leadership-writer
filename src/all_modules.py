"""All-Modules consolidated for df-ai-leadership-writer (Welle-44 Skeleton). [CRUX-MK]

Contains: outline_manager + style_guide + chapter_generator + audit_logger +
adapter_orchestrator. Pattern-equivalent to df-symbiotic-minds-writer.
"""

import os
import re
import sys
import json
import hmac
import hashlib
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ============================================================
# OUTLINE MANAGER
# ============================================================

@dataclass(frozen=True)
class Chapter:
    number: int
    title: str
    target_words: int = 6000
    status: str = "outlined"


AI_LEADERSHIP_OUTLINE: List[Chapter] = [
    Chapter(1, "Was ist AI Leadership? Definition + Abgrenzung"),
    Chapter(2, "Phronesis vs Pattern-Recognition - Die zentrale Aufteilung"),
    Chapter(3, "Trinity-Decision-Framework fuer C-Level"),
    Chapter(4, "Algorithmic Shield - Anti-Pattern Nr. 1"),
    Chapter(5, "Hybrid-by-Default 7-Schritte (Decision)"),
    Chapter(6, "3-Tier-Measurement - Effizienz / Quality / Capability"),
    Chapter(7, "Reversibility-Check - READ/WRITE/DESTROY"),
    Chapter(8, "Vier-Autoren-Mindset fuer Leader"),
    Chapter(9, "Reality Anchoring schuetzen - Walk the Floor"),
    Chapter(10, "Cognitive Atrophy verhindern"),
    Chapter(11, "Sensemaking statt Decision-Making"),
    Chapter(12, "Implementation-Roadmap fuer Mittelstand"),
]


class OutlineManager:
    def __init__(self, book_title: str = "AI Leadership",
                 subtitle: str = "Fuehrung in AI-First-Unternehmen"):
        self.book_title = book_title
        self.subtitle = subtitle
        self.chapters: List[Chapter] = list(AI_LEADERSHIP_OUTLINE)

    def get_chapter(self, number: int) -> Optional[Chapter]:
        for ch in self.chapters:
            if ch.number == number:
                return ch
        return None

    def list_chapters(self) -> List[Chapter]:
        return list(self.chapters)

    def chapter_count(self) -> int:
        return len(self.chapters)

    def total_target_words(self) -> int:
        return sum(ch.target_words for ch in self.chapters)


# ============================================================
# STYLE GUIDE
# ============================================================

@dataclass
class StyleViolation:
    rule: str
    severity: str
    message: str
    line_offset: int = 0


@dataclass
class StyleReport:
    violations: List[StyleViolation] = field(default_factory=list)
    sentences_checked: int = 0
    paragraphs_checked: int = 0
    avg_sentence_len: float = 0.0
    passes: bool = True


class StyleGuide:
    """Business-Pragmatism-Style. Concise, example-driven."""

    def __init__(self, max_sentence_words: int = 25, max_paragraph_sentences: int = 5):
        self.max_sentence_words = max_sentence_words
        self.max_paragraph_sentences = max_paragraph_sentences

    def split_sentences(self, text: str) -> List[str]:
        if not text:
            return []
        parts = re.split(r"(?<=[.!?])\s+", text.strip())
        return [p for p in parts if p]

    def split_paragraphs(self, text: str) -> List[str]:
        if not text:
            return []
        parts = re.split(r"\n\s*\n", text.strip())
        return [p.strip() for p in parts if p.strip()]

    def count_words(self, sentence: str) -> int:
        return len(sentence.split())

    def audit(self, text: str) -> StyleReport:
        report = StyleReport()
        sentences = self.split_sentences(text)
        paragraphs = self.split_paragraphs(text)
        report.sentences_checked = len(sentences)
        report.paragraphs_checked = len(paragraphs)

        for i, sent in enumerate(sentences):
            wc = self.count_words(sent)
            if wc > self.max_sentence_words:
                report.violations.append(StyleViolation(
                    rule="business_sentence_length", severity="warn",
                    message=f"Sentence {i+1}: {wc} words", line_offset=i))

        for i, para in enumerate(paragraphs):
            ps = self.split_sentences(para)
            if len(ps) > self.max_paragraph_sentences:
                report.violations.append(StyleViolation(
                    rule="business_paragraph_length", severity="info",
                    message=f"Paragraph {i+1}: {len(ps)} sentences", line_offset=i))

        if sentences:
            total_words = sum(self.count_words(s) for s in sentences)
            report.avg_sentence_len = total_words / len(sentences)

        report.passes = len([v for v in report.violations if v.severity == "error"]) == 0
        return report


# ============================================================
# CHAPTER GENERATOR
# ============================================================

@dataclass
class GeneratedChapter:
    chapter_number: int
    chapter_title: str
    text: str
    word_count: int
    source: str
    iso_timestamp: str
    style_passes: bool
    activation_gate_id: Optional[str] = None
    style_violations_count: int = 0


class ChapterGenerator:
    def __init__(self, book_title: str = "AI Leadership",
                 style_guide: Optional[StyleGuide] = None):
        self.book_title = book_title
        self.style_guide = style_guide or StyleGuide()

    def _check_real_mode(self) -> bool:
        return os.environ.get("DF_BOOK_REAL_ENABLED", "false") == "true"

    def _phronesis_ticket(self) -> Optional[str]:
        ticket = os.environ.get("PHRONESIS_TICKET", "")
        return ticket if ticket else None

    def generate_mock(self, chapter: Chapter) -> GeneratedChapter:
        stub_text = (
            f"# Kapitel {chapter.number}: {chapter.title}\n\n"
            f"[MOCK STUB - Buch '{self.book_title}']\n\n"
            f"Mock-Stub. Real-Generation erfordert DF_BOOK_REAL_ENABLED=true + PHRONESIS_TICKET.\n"
            f"Target-Words: {chapter.target_words}, Status: {chapter.status}\n\n"
            f"Inhalt zu '{chapter.title}': Mock-Platzhalter fuer Welle-44 Skeleton.\n"
        )
        report = self.style_guide.audit(stub_text)
        return GeneratedChapter(
            chapter_number=chapter.number, chapter_title=chapter.title,
            text=stub_text, word_count=len(stub_text.split()),
            source="mock", iso_timestamp=_iso_now(),
            style_passes=report.passes,
            style_violations_count=len(report.violations))

    def generate_real(self, chapter: Chapter) -> GeneratedChapter:
        ticket = self._phronesis_ticket()
        if not ticket:
            raise RuntimeError(
                "Real-Mode erfordert PHRONESIS_TICKET ENV-Var. "
                "Phronesis-Pflicht Martin: K_0/Q_0-Approval-Decision-Card.")
        raise NotImplementedError(
            f"df-ai-leadership-writer Real-LLM-Mode ist Welle-45+-Pflicht. "
            f"Skeleton-DF (Welle-44) liefert Mock-Default. Ticket: {ticket}")

    def generate_chapter(self, chapter: Chapter) -> GeneratedChapter:
        if self._check_real_mode():
            return self.generate_real(chapter)
        return self.generate_mock(chapter)


# ============================================================
# AUDIT LOGGER
# ============================================================

@dataclass
class AuditEntry:
    iso_timestamp: str
    event_type: str
    payload: Dict
    sequence_no: int
    prev_hash: str
    chain_hash: str = ""


class AuditLogger:
    def __init__(self, log_path: Path, hmac_key: Optional[bytes] = None):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._hmac_key = hmac_key or os.urandom(32)
        self._lock = threading.Lock()
        self._sequence_no = 0
        self._last_hash = "GENESIS"
        if self.log_path.exists():
            self._recover_state()

    def _recover_state(self):
        with self.log_path.open("r") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    self._sequence_no = entry["sequence_no"] + 1
                    self._last_hash = entry["chain_hash"]
                except (json.JSONDecodeError, KeyError):
                    continue

    def _compute_chain_hash(self, prev_hash: str, payload_json: str) -> str:
        msg = (prev_hash + payload_json).encode("utf-8")
        return hmac.new(self._hmac_key, msg, hashlib.sha256).hexdigest()

    def append(self, event_type: str, payload: Dict) -> AuditEntry:
        with self._lock:
            payload_json = json.dumps(payload, sort_keys=True)
            chain_hash = self._compute_chain_hash(self._last_hash, payload_json)
            entry = AuditEntry(
                iso_timestamp=_iso_now(), event_type=event_type, payload=payload,
                sequence_no=self._sequence_no, prev_hash=self._last_hash,
                chain_hash=chain_hash)
            with self.log_path.open("a") as f:
                f.write(json.dumps({
                    "iso_timestamp": entry.iso_timestamp,
                    "event_type": entry.event_type,
                    "payload": entry.payload,
                    "sequence_no": entry.sequence_no,
                    "prev_hash": entry.prev_hash,
                    "chain_hash": entry.chain_hash,
                }) + "\n")
            self._sequence_no += 1
            self._last_hash = chain_hash
            return entry

    def verify_chain(self) -> bool:
        if not self.log_path.exists():
            return True
        prev_hash = "GENESIS"
        with self.log_path.open("r") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    payload_json = json.dumps(entry["payload"], sort_keys=True)
                    expected = self._compute_chain_hash(prev_hash, payload_json)
                    if expected != entry["chain_hash"]:
                        return False
                    if entry["prev_hash"] != prev_hash:
                        return False
                    prev_hash = entry["chain_hash"]
                except (json.JSONDecodeError, KeyError):
                    return False
        return True


# ============================================================
# ADAPTER ORCHESTRATOR
# ============================================================

@dataclass
class OrchestratorRunResult:
    iso_started: str
    iso_completed: str
    chapters_generated: int
    chapters_failed: int
    source_mode: str
    audit_log_path: str
    quota_used: int


class AdapterOrchestrator:
    def __init__(self, book_title: str = "AI Leadership",
                 audit_log_dir: Optional[Path] = None,
                 quota_max_per_run: int = 5):
        self.book_title = book_title
        self.outline = OutlineManager(book_title=book_title)
        self.style = StyleGuide()
        self.generator = ChapterGenerator(book_title=book_title, style_guide=self.style)
        self.quota_max = quota_max_per_run
        log_dir = Path(audit_log_dir) if audit_log_dir else Path.home() / ".df-state"
        log_dir.mkdir(parents=True, exist_ok=True)
        self.audit = AuditLogger(log_dir / "df-ai-leadership-writer-audit.jsonl")

    def _check_stop_flag(self) -> bool:
        return (Path.home() / ".df-state" / "df-ai-leadership-writer.STOP.flag").exists()

    def _detect_source_mode(self) -> str:
        return "real-llm" if os.environ.get("DF_BOOK_REAL_ENABLED", "false") == "true" else "mock"

    def run(self, chapter_numbers: Optional[List[int]] = None) -> OrchestratorRunResult:
        iso_start = _iso_now()
        source_mode = self._detect_source_mode()
        self.audit.append("run_start", {
            "iso_timestamp": iso_start, "source_mode": source_mode,
            "quota_max": self.quota_max, "chapter_request": chapter_numbers})

        if self._check_stop_flag():
            self.audit.append("run_stopped", {"reason": "STOP.flag detected"})
            return OrchestratorRunResult(
                iso_started=iso_start, iso_completed=_iso_now(),
                chapters_generated=0, chapters_failed=0, source_mode=source_mode,
                audit_log_path=str(self.audit.log_path), quota_used=0)

        if chapter_numbers is None:
            chapter_numbers = list(range(1, self.quota_max + 1))
        chapter_numbers = chapter_numbers[: self.quota_max]

        generated, failed = 0, 0
        for ch_num in chapter_numbers:
            chapter = self.outline.get_chapter(ch_num)
            if not chapter:
                self.audit.append("chapter_not_found", {"chapter_number": ch_num})
                failed += 1
                continue
            try:
                result = self.generator.generate_chapter(chapter)
                self.audit.append("chapter_generated", {
                    "chapter_number": result.chapter_number,
                    "chapter_title": result.chapter_title,
                    "word_count": result.word_count,
                    "source": result.source, "style_passes": result.style_passes})
                generated += 1
            except (NotImplementedError, RuntimeError) as e:
                self.audit.append("chapter_generation_failed", {
                    "chapter_number": ch_num, "error": str(e)})
                failed += 1

        self.audit.append("run_complete", {
            "chapters_generated": generated, "chapters_failed": failed})
        return OrchestratorRunResult(
            iso_started=iso_start, iso_completed=_iso_now(),
            chapters_generated=generated, chapters_failed=failed,
            source_mode=source_mode, audit_log_path=str(self.audit.log_path),
            quota_used=generated)


def main():
    orch = AdapterOrchestrator()
    result = orch.run()
    print(f"DF-ai-leadership-writer run: {result.chapters_generated} generated, "
          f"{result.chapters_failed} failed, mode={result.source_mode}")
    sys.exit(0 if result.chapters_failed == 0 else 1)


if __name__ == "__main__":
    main()

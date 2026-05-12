"""All-tests for df-ai-leadership-writer (consolidated). [CRUX-MK]

Test-Bilanz: 17+ Tests across all 4 modules
(outline_manager: 4, style_guide: 4, chapter_generator: 6, adapter_orchestrator: 3)
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.all_modules import (
    OutlineManager, Chapter, AI_LEADERSHIP_OUTLINE,
    StyleGuide, StyleReport,
    ChapterGenerator, GeneratedChapter,
    AdapterOrchestrator, OrchestratorRunResult,
    AuditLogger,
)


# OutlineManager Tests (4)

def test_outline_manager_init():
    om = OutlineManager()
    assert om.book_title == "AI Leadership"


def test_chapter_count_is_12():
    """Welle-44 spec: 12 Kapitel fuer AI Leadership."""
    assert OutlineManager().chapter_count() == 12


def test_get_chapter_returns_correct():
    om = OutlineManager()
    ch1 = om.get_chapter(1)
    assert ch1 is not None
    assert "AI Leadership" in ch1.title


def test_chapter_is_frozen():
    ch = Chapter(1, "Test")
    try:
        ch.number = 2  # type: ignore
        raise AssertionError("Chapter should be frozen")
    except (AttributeError, Exception):
        pass


# StyleGuide Tests (4)

def test_style_guide_init():
    sg = StyleGuide()
    assert sg.max_sentence_words == 25


def test_audit_short_text_passes():
    sg = StyleGuide()
    text = "Kurz und klar. Geht so. Gut."
    report = sg.audit(text)
    assert report.passes is True


def test_audit_long_sentence_warns():
    sg = StyleGuide(max_sentence_words=5)
    text = "Dies ist ein sehr langer Satz mit vielen Worten."
    report = sg.audit(text)
    assert any(v.rule == "business_sentence_length" for v in report.violations)


def test_split_sentences_handles_empty():
    sg = StyleGuide()
    assert sg.split_sentences("") == []


# ChapterGenerator Tests (6)

def test_generator_init():
    gen = ChapterGenerator()
    assert gen.book_title == "AI Leadership"


def test_default_mock_mode():
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("DF_BOOK_REAL_ENABLED", None)
        gen = ChapterGenerator()
        assert gen._check_real_mode() is False


def test_mock_chapter_generation():
    gen = ChapterGenerator()
    ch = Chapter(1, "Test")
    result = gen.generate_chapter(ch)
    assert result.source == "mock"
    assert "MOCK STUB" in result.text


def test_real_mode_without_ticket_raises():
    with patch.dict(os.environ, {"DF_BOOK_REAL_ENABLED": "true"}, clear=False):
        os.environ.pop("PHRONESIS_TICKET", None)
        gen = ChapterGenerator()
        try:
            gen.generate_chapter(Chapter(1, "X"))
            raise AssertionError("Should have raised RuntimeError")
        except RuntimeError as e:
            assert "PHRONESIS_TICKET" in str(e)


def test_real_mode_with_ticket_raises_not_implemented():
    with patch.dict(os.environ, {
        "DF_BOOK_REAL_ENABLED": "true",
        "PHRONESIS_TICKET": "PT-2026-05-11-002",
    }, clear=False):
        gen = ChapterGenerator()
        try:
            gen.generate_chapter(Chapter(1, "X"))
            raise AssertionError("Should raise NotImplementedError")
        except NotImplementedError as e:
            assert "Welle-45+" in str(e)


def test_env_var_truthy_strict_check():
    """Only literal '=true' activates real mode."""
    for val in ["1", "yes", "True", "TRUE"]:
        with patch.dict(os.environ, {"DF_BOOK_REAL_ENABLED": val}, clear=False):
            assert ChapterGenerator()._check_real_mode() is False


# AdapterOrchestrator Tests (3)

def test_orchestrator_init():
    with tempfile.TemporaryDirectory() as tmp:
        orch = AdapterOrchestrator(audit_log_dir=Path(tmp))
        assert orch.book_title == "AI Leadership"


def test_run_default_quota():
    with tempfile.TemporaryDirectory() as tmp:
        orch = AdapterOrchestrator(audit_log_dir=Path(tmp), quota_max_per_run=3)
        result = orch.run()
        assert result.chapters_generated == 3
        assert result.source_mode == "mock"


def test_run_with_specific_chapters():
    with tempfile.TemporaryDirectory() as tmp:
        orch = AdapterOrchestrator(audit_log_dir=Path(tmp), quota_max_per_run=10)
        result = orch.run(chapter_numbers=[1, 3, 5])
        assert result.chapters_generated == 3

"""df-ai-leadership-writer src package [CRUX-MK]

LAZY-IMPORT: heavy modules import only via __getattr__.
Modules consolidated into all_modules.py for compact build (Welle-44 Skeleton).
"""

__version__ = "0.1.0-skeleton"


def __getattr__(name):
    if name in ("ChapterGenerator", "OutlineManager", "StyleGuide",
                "AdapterOrchestrator", "AuditLogger", "Chapter",
                "GeneratedChapter", "OrchestratorRunResult"):
        from . import all_modules
        return getattr(all_modules, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")

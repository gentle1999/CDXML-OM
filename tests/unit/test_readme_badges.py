import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BADGE_PATTERN = re.compile(r"\[!\[[^\]]+\]\((https://img\.shields\.io/[^)]+)\)\]\(([^)]+)\)")


def _badges(readme: Path) -> list[tuple[str, str]]:
    return BADGE_PATTERN.findall(readme.read_text(encoding="utf-8"))


def test_english_and_chinese_readmes_have_the_same_badges_and_targets() -> None:
    english = _badges(ROOT / "README.md")
    chinese = _badges(ROOT / "README.zh-CN.md")

    assert len(english) == 15
    assert chinese == english


def test_badge_targets_are_real_local_files_and_badges_are_not_live_status() -> None:
    for _, target in _badges(ROOT / "README.md"):
        assert not target.startswith(("https://", "http://"))
        assert (ROOT / target).exists(), target

    readmes = "\n".join(
        (ROOT / filename).read_text(encoding="utf-8")
        for filename in ("README.md", "README.zh-CN.md")
    )
    assert "static configuration" in readmes
    assert "静态配置" in readmes
    assert "shields.io/pypi" not in readmes
    assert "github.com/gentle1999/CDXML-OM/actions/workflows" not in readmes
    assert "0.1.0.dev0" not in readmes


def test_badges_state_configured_checks_and_source_scoped_counts() -> None:
    badge_urls = "\n".join(url for url, _ in _badges(ROOT / "README.md"))

    for expected in (
        "Python-%E2%89%A53.11",
        "License-MIT",
        "Version-single--source%20configuration",
        "Pyright%20%2B%20mypy%20strict",
        "Ruff-lint%20%2B%20format%20configured",
        "Tests-pytest%20configured",
        "GitHub%20Actions%20configured",
        "53%20elements%20%2F%20762%20pairs",
        "PCDATA%20%2B%20SDK-2%2F2%20%2B%2023%2F23%20round--trip",
        "ChemDraw%20app%20verification-none",
    ):
        assert expected in badge_urls

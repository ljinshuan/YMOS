"""Centralised path definitions for YMOS."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    root: Path  # YMOS project root

    # ── data/ ──────────────────────────────────────────
    @property
    def data(self) -> Path:
        return self.root / "data"

    @property
    def state(self) -> Path:
        return self.data / "state"

    @property
    def holdings_state(self) -> Path:
        return self.state / "holdings.md"

    @property
    def watchlist_state(self) -> Path:
        return self.state / "watchlist.md"

    @property
    def preferences(self) -> Path:
        return self.state / "preferences.md"

    @property
    def memo_view(self) -> Path:
        return self.state / "memo-view.md"

    @property
    def stocks(self) -> Path:
        return self.data / "stocks"

    @property
    def holdings_dir(self) -> Path:
        return self.stocks / "holdings"

    @property
    def watchlist_dir(self) -> Path:
        return self.stocks / "watchlist"

    # ── data/reports/ ──────────────────────────────────
    @property
    def reports(self) -> Path:
        return self.data / "reports"

    @property
    def market_insight(self) -> Path:
        return self.reports / "market-insight"

    @property
    def radar(self) -> Path:
        return self.reports / "radar"

    @property
    def strategy(self) -> Path:
        return self.reports / "strategy"

    # ── data/dashboard/ ────────────────────────────────
    @property
    def dashboard(self) -> Path:
        return self.data / "dashboard"

    # ── references/ ────────────────────────────────────
    @property
    def references(self) -> Path:
        return self.root / "references"

    @property
    def sops(self) -> Path:
        return self.references / "sops"

    @property
    def prompts(self) -> Path:
        return self.references / "prompts"

    @property
    def templates(self) -> Path:
        return self.references / "templates"

    # ── helpers ────────────────────────────────────────
    def month_dir(self, base: Path, date_value) -> Path:
        return base / date_value.strftime("%Y-%m")

    def radar_raw_dir(self, date_tag: str) -> Path:
        month_tag = f"{date_tag[:4]}-{date_tag[4:6]}"
        return self.radar / month_tag

    def market_raw_dir(self, date_tag: str) -> Path:
        month_tag = f"{date_tag[:4]}-{date_tag[4:6]}"
        return self.market_insight / month_tag

    def ensure_dirs(self) -> list[Path]:
        """Create all standard data/ sub-directories. Returns created paths."""
        dirs = [
            self.state,
            self.stocks,
            self.holdings_dir,
            self.watchlist_dir,
            self.reports,
            self.market_insight,
            self.radar,
            self.strategy,
            self.dashboard,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
        return dirs


def find_ymos_root() -> Path:
    """Walk up from cli/core/ to find the directory containing CLAUDE.md."""
    current = Path(__file__).resolve().parents[2]  # cli/core → cli → root
    for parent in [current] + list(current.parents):
        if (parent / "CLAUDE.md").exists():
            return parent
    return current


def get_paths() -> Paths:
    return Paths(root=find_ymos_root())

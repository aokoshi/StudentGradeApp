"""Thin wrapper around :class:`rich.console.Console` with helpers."""
from __future__ import annotations

import os
from typing import Iterable

from rich.console import Console
from rich.panel  import Panel
from rich.prompt import Prompt
from rich.text   import Text


class ConsoleUI:
    """Single source of rich rendering primitives used across the app."""

    def __init__(self) -> None:
        self.console = Console()

    # ---------- screen --------------------------------------------------

    def clear(self) -> None:
        """Clear the terminal screen (cross-platform)."""
        os.system("cls" if os.name == "nt" else "clear")

    def banner(self, breadcrumbs: Iterable[str]) -> None:
        """Render the app banner with a breadcrumb trail.

        ``breadcrumbs`` is something like ``["Home", "Students", "Details"]``.
        """
        crumbs = " › ".join(breadcrumbs)
        title  = Text("StudentGradeAPP v2", style="bold cyan")
        sub    = Text(crumbs, style="dim")
        self.console.print(Panel.fit(Text.assemble(title, "\n", sub), border_style="cyan"))

    # ---------- messages ------------------------------------------------

    def success(self, msg: str) -> None:
        self.console.print(f"[bold green]✓[/bold green] {msg}")

    def error(self, msg: str) -> None:
        self.console.print(f"[bold red]✗[/bold red] {msg}")

    def info(self, msg: str) -> None:
        self.console.print(f"[bold blue]i[/bold blue] {msg}")

    def pause(self) -> None:
        self.console.input("\n[dim]Press Enter to continue…[/dim]")

    # ---------- input ---------------------------------------------------

    def ask(self, prompt: str, *, default: str | None = None) -> str:
        return Prompt.ask(prompt, default=default)

    def ask_choice(self, prompt: str, choices: list[str]) -> str:
        return Prompt.ask(prompt, choices=choices, show_choices=False)

"""Reusable decorators for the UI layer."""
from __future__ import annotations

import functools
from typing import Any, Callable

from rich.console import Console

_console = Console()


def confirm_action(prompt: str = "Are you sure?") -> Callable:
    """Decorator that asks the user to confirm before running the wrapped function.

    The wrapped function is only invoked if the user types ``y``/``yes``.
    Used for destructive operations like deleting a student or course.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            answer = _console.input(f"[yellow]{prompt} (y/N): [/yellow]").strip().lower()
            if answer not in {"y", "yes"}:
                _console.print("[dim]Cancelled.[/dim]")
                return None
            return func(*args, **kwargs)

        return wrapper

    return decorator


def catch_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    """Catch ``ValueError`` / ``KeyError`` and print them as friendly messages.

    Keeps the menu loop alive instead of crashing on bad input.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError) as exc:
            _console.print(f"[red]Error:[/red] {exc}")
        except KeyboardInterrupt:
            _console.print("\n[dim]Cancelled.[/dim]")
        return None

    return wrapper

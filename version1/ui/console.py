"""Console UI helpers — pretty-print tables and prompt for input.

"""


def prompt(label: str) -> str:
    return input(f"{label}: ").strip()


def prompt_int(label: str) -> int:
    while True:
        raw = prompt(label)
        try:
            return int(raw)
        except ValueError:
            print(f"  '{raw}' is not a valid integer, try again.")


def prompt_float(label: str, lo: float = 0, hi: float = 100) -> float:
    while True:
        raw = prompt(label)
        try:
            value = float(raw)
        except ValueError:
            print(f"  '{raw}' is not a valid number, try again.")
            continue
        if not lo <= value <= hi:
            print(f"  value must be between {lo} and {hi}.")
            continue
        return value


def print_table(headers: list[str], rows: list[list]) -> None:
    """Minimal pretty-printer for a 2D table."""
    widths = [len(h) for h in headers]
    str_rows = [[str(c) for c in row] for row in rows]
    for row in str_rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    sep = "+".join("-" * (w + 2) for w in widths)
    print(sep)
    print("|".join(f" {h.ljust(w)} " for h, w in zip(headers, widths)))
    print(sep)
    for row in str_rows:
        print("|".join(f" {c.ljust(w)} " for c, w in zip(row, widths)))
    print(sep)


def menu(title: str, options: list[str]) -> int:
    """Show a numbered menu and return the chosen index (0-based)."""
    print()
    print(f"=== {title} ===")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = prompt("Choose")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice) - 1
        print(f"  enter a number between 1 and {len(options)}.")

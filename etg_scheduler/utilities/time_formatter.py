def format_number(value: float) -> str:
    text = f"{value:.2f}"
    return text.rstrip("0").rstrip(".")


def format_money(value: float) -> str:
    return f"{value:.2f}"


def format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"

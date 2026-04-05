"""Output formatting utilities using Rich library."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Dict, Any, Optional


console = Console()


def format_result(
    title: str,
    inputs: Dict[str, Any],
    result: Dict[str, Any],
    formula: Optional[str] = None,
    notes: Optional[str] = None
) -> None:
    """
    Format and display calculation results in a beautiful table.

    Args:
        title: Title of the calculation
        inputs: Dictionary of input parameters
        result: Dictionary of result values
        formula: Optional formula string to display
        notes: Optional notes or assumptions
    """
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Label", style="cyan")
    table.add_column("Value", style="green")

    # Add inputs section
    if inputs:
        table.add_row("[bold]Inputs:[/bold]", "")
        for key, value in inputs.items():
            formatted_value = _format_value(value)
            table.add_row(f"  {key}", formatted_value)
        table.add_row("", "")

    # Add results section
    if result:
        table.add_row("[bold]Result:[/bold]", "")
        for key, value in result.items():
            formatted_value = _format_value(value)
            table.add_row(f"  {key}", formatted_value)

    # Add formula if provided
    if formula:
        table.add_row("", "")
        table.add_row("[bold]Formula:[/bold]", formula)

    # Add notes if provided
    if notes:
        table.add_row("", "")
        table.add_row("[bold]Notes:[/bold]", notes)

    panel = Panel(table, title=f"[bold]{title}[/bold]", border_style="blue")
    console.print(panel)


def _format_value(value: Any) -> str:
    """Format a value for display."""
    if isinstance(value, float):
        # Format as currency if it looks like a dollar amount
        if abs(value) >= 0.01:
            return f"${value:,.2f}" if value >= 0 else f"-${abs(value):,.2f}"
        # Format as percentage if it's a small decimal
        elif abs(value) < 1:
            return f"{value * 100:.2f}%"
        else:
            return f"{value:.4f}"
    elif isinstance(value, int):
        return f"{value:,}"
    elif isinstance(value, str):
        return value
    else:
        return str(value)


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[bold blue]ℹ[/bold blue] {message}")

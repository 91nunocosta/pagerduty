"""Provide the command line interface prototype_python_library."""
import typer

from pagerduty import fib

app: typer.Typer = typer.Typer()


@app.command()
def fibbonacy(position: int) -> None:
    """Compute the number at a certain position in the fibbonacy sequence.

    Args:
        position (int): position of fibbonacy sequence to compute.
    """
    typer.echo(fib(position))

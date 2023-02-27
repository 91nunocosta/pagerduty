"""Provide the command line interface for PagerDuty API."""
import os

import typer

from pagerduty import PagerDutyClient

pagerduty: typer.Typer = typer.Typer()
pagerduty_abilities: typer.Typer = typer.Typer()
pagerduty.add_typer(pagerduty_abilities, name="abilities")


def create_pagerduty_client() -> PagerDutyClient:
    """Create a PagerDuty client configured from environment variables.

    Returns:
        A PagerDuty client instance.
    """
    return PagerDutyClient(auth_token=os.environ["PAGERDUTY_TOKEN"])


@pagerduty_abilities.command(name="list")
def list_abilities() -> None:
    """List account ablilities."""
    pagerduty_client = create_pagerduty_client()
    typer.echo("The account has the following abilities: ")
    typer.echo_via_pager(os.linesep.join(pagerduty_client.get_abilities()))


@pagerduty_abilities.command(name="test")
def test_ability(ability: str) -> None:
    """Test if the account has an ablility."""
    pagerduty_client = create_pagerduty_client()
    typer.echo_via_pager("yes" if pagerduty_client.test_ability(ability) else "no")

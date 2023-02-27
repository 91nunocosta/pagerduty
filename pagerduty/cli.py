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


@pagerduty.command(name="users")
def users() -> None:
    """Test getting users"""
    pagerduty_client = create_pagerduty_client()
    typer.echo_via_pager(
        os.linesep.join(str(user) for user in pagerduty_client.get_users())
    )


@pagerduty.command(name="contacts")
def contacts(user_id: str) -> None:
    """Test getting user contacts"""
    pagerduty_client = create_pagerduty_client()
    user = pagerduty_client.get_user(user_id)
    user_contacts = [
        pagerduty_client.get_contact_method(user_id, contact["id"])
        for contact in user["contact_methods"]
    ]
    typer.echo_via_pager(os.linesep.join(str(contact) for contact in user_contacts))

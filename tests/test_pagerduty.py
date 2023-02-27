"""Test pagerduty module."""
import os

import pytest

import pagerduty


@pytest.fixture(name="pagerduty_client")
def create_pagerduty_client() -> pagerduty.PagerDutyClient:
    """Create a PagerDuty client loading auth token from environment variable.

    Returns:
        A PagerDuty client instance.
    """
    return pagerduty.PagerDutyClient(auth_token=os.environ["PAGERDUTY_TOKEN"])


def test_create_pagerduty_client(pagerduty_client: pagerduty.PagerDutyClient) -> None:
    """Test creating PagerDutyClient instance."""
    assert isinstance(pagerduty_client, pagerduty.PagerDutyClient)
    assert isinstance(pagerduty_client.auth_token, str)
    assert len(pagerduty_client.auth_token) > 0


def test_pagerduty__request(pagerduty_client: pagerduty.PagerDutyClient) -> None:
    """Test PagerDutyClient request."""
    response = pagerduty_client._request(  # pylint: disable=protected-access
        "GET", "/abilities"
    )
    assert response.status_code == 200


def test_pagerduty_get_abilities(pagerduty_client: pagerduty.PagerDutyClient) -> None:
    """Test listing abilities with PagerDutyClient."""
    abilities = pagerduty_client.get_abilities()
    assert len(abilities) > 0


def test_pagerduty_test_abilities(pagerduty_client: pagerduty.PagerDutyClient) -> None:
    """Test testing an ability with PagerDutyClient."""
    assert pagerduty_client.test_ability("teams")

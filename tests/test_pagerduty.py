"""Test pagerduty module."""
import os

import pytest

import pagerduty

RESOURCE_WITH_MULTIVALUE_QUERY = pagerduty.PagerDutyResource(
    ["addons"],
    query={
        "limit": 10,
        "offset": 10,
        "total": True,
        "filter": "full_page_addon",
        # "include": ["services", "services"],
        "services_ids": ["PKX7619", "PKX7620"],
    },
)


def test_create_resource() -> None:
    """Test creating a REST resource."""
    resource = pagerduty.PagerDutyResource(["analytics", "metrics", "incidents", "all"])
    assert resource.uri() == "https://api.pagerduty.com/analytics/metrics/incidents/all"

    resource = RESOURCE_WITH_MULTIVALUE_QUERY
    assert (
        resource.uri() == "https://api.pagerduty.com/addons?"
        "limit=10&offset=10&total=True&filter=full_page_addon&"
        "services_ids=%5B%27PKX7619%27%2C+%27PKX7620%27%5D"
    )


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
        "GET",
        pagerduty.PagerDutyResource(["abilities"]),
    )
    assert response.status_code == 200

    with pytest.raises(RuntimeError):
        pagerduty_client._request(  # pylint: disable=protected-access
            "GET",
            pagerduty.PagerDutyResource(["addons"], query={"limit": -1}),
        )

    response = pagerduty_client._request(  # pylint: disable=protected-access
        "GET",
        RESOURCE_WITH_MULTIVALUE_QUERY,
    )
    assert response.status_code == 200


def test_pagerduty_get_abilities(pagerduty_client: pagerduty.PagerDutyClient) -> None:
    """Test listing abilities with PagerDutyClient."""
    abilities = pagerduty_client.get_abilities()
    assert len(abilities) > 0


def test_pagerduty_test_abilities(pagerduty_client: pagerduty.PagerDutyClient) -> None:
    """Test testing an ability with PagerDutyClient."""
    assert pagerduty_client.test_ability("teams")

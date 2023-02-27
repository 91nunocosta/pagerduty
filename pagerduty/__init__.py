"""PagerDuty client API for the interview."""
from typing import Any, List

import requests

__version__ = "0.1.0"


class PagerDutyClient:
    """PagerDuty API client."""

    def __init__(self, auth_token: str) -> None:
        """Initialize the client for a certain account.

        Args:
            auth_token (str): the account's authentication token
        """
        self.auth_token: str = auth_token

    def _request(self, method: str, resource: str, **kwargs: Any) -> requests.Response:
        """Sends an authenticated HTTP request to PagerDuty API server.

        Args:
            method (str): the HTTP method to apply to the resource.
            resource (str): the request path
                            identifying the resource that the request targets.
            kwargs: requests.request method kwargs

        Returns:
            The requests.Response received from the PagerDuty server.
        """
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["Authorization"] = f"Token token={self.auth_token}"
        return requests.request(
            method, url=f"https://api.pagerduty.com/{resource}", timeout=4, **kwargs
        )

    def get_abilities(self) -> List[str]:
        """List the abilities for the account.

        Returns:
            The list of this account's abilities.
        """
        response: requests.Response = self._request("GET", "/abilities")
        ablilities: List[str] = response.json()["abilities"]
        return ablilities

    def test_ability(self, ability: str) -> bool:
        """Test whether the account has a given ability.

        Args:
            ability (str): the ability to test.

        Returns:
            True iff the account has the ability.
        """
        response = self._request("GET", f"/abilities/{ability}")
        return response.status_code == 204

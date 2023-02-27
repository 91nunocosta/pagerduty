"""PagerDuty client API for the interview."""
import urllib.parse
from typing import Any, Dict, List, Optional

import requests

__version__ = "0.1.0"


PAGERDUTY_API_BASE_URI = "https://api.pagerduty.com"


# pylint: disable=too-few-public-methods
class PagerDutyResource:
    """Represents a PagerDuty REST API resource."""

    def __init__(self, path: List[str], query: Optional[Dict[str, Any]] = None) -> None:
        """Initializes a PagerDuty REST API resource.

        Args:
            path: Resource path.
            query: The query parameters.

        """
        self.path: List[str] = path
        self.query: Optional[Dict[str, Any]] = query

    def uri(self) -> str:
        """
        Returns:
            PagerDuty REST API Resource uri.
        """
        uri: str = PAGERDUTY_API_BASE_URI + "/" + "/".join(self.path)
        if self.query:
            uri += "?" + urllib.parse.urlencode(self.query)
        return uri


class PagerDutyClient:
    """PagerDuty API client."""

    def __init__(self, auth_token: str) -> None:
        """Initialize the client for a certain account.

        Args:
            auth_token (str): the account's authentication token
        """
        self.auth_token: str = auth_token

    def _request(
        self, method: str, resource: PagerDutyResource, **kwargs: Any
    ) -> requests.Response:
        """Sends an authenticated HTTP request to PagerDuty API server.

        Args:
            method (str): the HTTP method to apply to the resource.
            resource (PagerDutyResource): the resource identifier
            kwargs: requests.request method kwargs

        Raises:
            RuntimeError: if receives an HTTP error status code.

        Returns:
            The requests.Response received from the PagerDuty server.
        """
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["Authorization"] = f"Token token={self.auth_token}"
        response: requests.Response = requests.request(
            method,
            url=resource.uri(),
            timeout=4,
            **kwargs,
        )
        if response.status_code >= 400:
            raise RuntimeError(
                f"""Failed to request {method} {resource.uri()}:
                        {response.status_code, response.json()}
                """
            )
        return response

    def get_abilities(self) -> List[str]:
        """List the abilities for the account.

        Returns:
            The list of this account's abilities.
        """
        response: requests.Response = self._request(
            "GET",
            PagerDutyResource(["abilities"]),
        )
        ablilities: List[str] = response.json()["abilities"]
        return ablilities

    def test_ability(self, ability: str) -> bool:
        """Test whether the account has a given ability.

        Args:
            ability (str): the ability to test.

        Returns:
            True iff the account has the ability.
        """
        response = self._request(
            "GET",
            PagerDutyResource(["abilities", ability]),
        )
        return response.status_code == 204

    def get_users(self) -> List[Dict[str, Any]]:
        """List users.

        Returns:
            List of users.
        """
        response = self._request("GET", PagerDutyResource(["users"]))

        return [
            {
                "id": user["id"],
                "name": user["name"],
                "contacts": user["contact_methods"],
            }
            for user in response.json()["users"]
        ]

    def get_user(self, _id: str) -> Any:
        """Get a user.

        Returns:
            A user's details.
        """
        response = self._request(
            "GET",
            PagerDutyResource(["users", _id]),
        )
        return response.json()["user"]

    def get_contact_method(self, user_id: str, _id: str) -> Any:
        """Get a user contact method.

        Returns:
            A user's contact method details.
        """
        response = self._request(
            "GET",
            PagerDutyResource(["users", user_id, "contact_methods", _id]),
        )
        return response.json()

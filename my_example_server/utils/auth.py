"""Authentication utilities for My Example Server."""

import os

import httpx

from mcp.gumstack import get_credentials as gumstack_get_credentials
from mcp.gumstack.auth import AuthProvider, TokenResponse


class GitHubAuthProvider(AuthProvider):
    """OAuth provider for github.

    Implements the OAuth flow for github.
    The gumstack backend calls these methods to orchestrate the flow.
    """

    name = "github"

    def get_url(self, redirect_uri: str, state: str) -> str:
        """Generate the OAuth authorization URL."""
        client_id = os.environ.get("GITHUB_CLIENT_ID", "")
        # TODO: Update with correct OAuth URL and scopes for github
        return (
            f"https://github.example.com/oauth/authorize"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&state={state}"
            f"&response_type=code"
            f"&scope=read,write"
        )

    async def exchange(self, code: str, redirect_uri: str) -> TokenResponse:
        """Exchange authorization code for tokens."""
        client_id = os.environ.get("GITHUB_CLIENT_ID", "")
        client_secret = os.environ.get("GITHUB_CLIENT_SECRET", "")

        # TODO: Update with correct token endpoint for github
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://github.example.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "client_id": client_id,
                    "client_secret": client_secret,
                },
            )
            response.raise_for_status()
            data = response.json()

        return TokenResponse(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            expires_in=data.get("expires_in"),
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        """Refresh an expired access token."""
        client_id = os.environ.get("GITHUB_CLIENT_ID", "")
        client_secret = os.environ.get("GITHUB_CLIENT_SECRET", "")

        # TODO: Update with correct token endpoint for github
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://github.example.com/oauth/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": client_id,
                    "client_secret": client_secret,
                },
            )
            response.raise_for_status()
            data = response.json()

        return TokenResponse(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            expires_in=data.get("expires_in"),
        )

    async def get_nickname(self, access_token: str) -> str:
        """Get display name for the connected account."""
        # TODO: Update with correct user info endpoint for github
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://github.example.com/api/user",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
            data = response.json()

        return data.get("email", data.get("name", "Unknown"))


# Provider name constant for use with get_credentials()
PROVIDER_NAME = "github"


async def get_credentials(provider: str = PROVIDER_NAME) -> dict[str, str]:
    """
    Get OAuth credentials from gumstack backend.

    After OAuth flow completes, tokens are stored by backend.
    This retrieves the stored access_token for API calls.

    Args:
        provider: The provider name (defaults to "github").
    """
    if os.environ.get("ENVIRONMENT") == "local":
        return {
            "access_token": os.environ.get("LOCAL_ACCESS_TOKEN", ""),
        }

    return await gumstack_get_credentials(provider)

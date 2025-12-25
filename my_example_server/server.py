import argparse
import logging
import os

from mcp.gumstack import GumstackHost
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from my_example_server.utils.auth import GitHubAuthProvider, get_credentials


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Get port from environment variable (default 8000 for local, 8080 for Knative)
PORT = int(os.environ.get("PORT", 8000))

mcp = FastMCP("My Example Server", host="0.0.0.0", port=PORT)

# Health check endpoint for Knative readiness/liveness probes
@mcp.custom_route("/health_check", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})

@mcp.tool()
async def example_tool(query: str) -> str:
    """
    Example tool using OAuth credentials.

    Args:
        query: The query to process
    """
    # get_credentials() returns OAuth tokens stored by backend after OAuth exchange
    creds = await get_credentials()
    access_token = creds.get("access_token", "")
    logger.info("Processing with OAuth token: %s...", access_token[:8] if access_token else "none")
    return f"Processed: {query}"


def main():
    parser = argparse.ArgumentParser(description="My Example Server MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="streamable-http",
        help="Transport to use (default: streamable-http)",
    )
    args = parser.parse_args()

    if os.environ.get("ENVIRONMENT") != "local":
        host = GumstackHost(mcp)

        # Register OAuth provider for github
        host.register_auth(GitHubAuthProvider())

        # Use gumstack host which handles middleware, interceptors, and auth routes
        host.run(host="0.0.0.0", port=PORT)
    else:
        # Local development without gumstack
        mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
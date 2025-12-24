# My Example Server

An example MCP server

## Setup

```bash
# Install dependencies
uv sync

# Copy environment file
cp example.env .env

# Edit .env with your values
```

## Local Development

```bash
# Run the server
./run.sh

# Or directly
uv run python -m src.server
```


## Authentication

This server uses user-provided credentials. In local development, set `ENVIRONMENT=local` and `LOCAL_API_KEY` in your `.env` file.

When deployed to Gumstack, users will enter their api_key in the Gumstack UI.


## Tools

- `example_tool` - Example tool demonstrating credential usage

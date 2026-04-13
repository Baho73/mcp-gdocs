# mcp-gdocs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MCP server for creating Google Docs from Markdown with full formatting support. Designed for AI agents — any MCP-compatible client (Claude Code, Claude Desktop, etc.) can create, update, and search Google Docs.

## Tools

| Tool | Description |
|---|---|
| `markdown_to_gdoc` | Convert Markdown to a Google Doc, get back a URL |
| `update_google_doc` | Update existing Google Doc with new Markdown content |
| `list_google_docs` | Search your Google Docs by name |

## Supported Markdown

- Headings (h1-h4)
- **Bold**, *italic*, `inline code`
- Bullet lists (nested)
- Tables with headers
- Links

## Prerequisites

1. **Python 3.10+**
2. **Google Cloud project** with these APIs enabled:
   - [Google Docs API](https://console.cloud.google.com/apis/library/docs.googleapis.com)
   - [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com)
3. **OAuth 2.0 credentials** (Desktop app type) — download from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

## Installation

```bash
# Clone the repository
git clone https://github.com/Baho73/mcp-gdocs.git
cd mcp-gdocs

# Create virtual environment and install
python -m venv .venv
.venv/Scripts/activate  # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -e .
```

## Setup

### 1. Add Google OAuth credentials

```bash
mkdir credentials
cp /path/to/your/client_secret.json credentials/client_secret.json
```

### 2. Authenticate (first run)

```bash
python -m mcp_gdocs.server
```

This opens a browser for Google OAuth consent. After authorization, the token is cached in `credentials/token.json`.

### 3. Add to Claude Code

```bash
claude mcp add mcp-gdocs -- /path/to/mcp-gdocs/.venv/Scripts/python -m mcp_gdocs.server
```

Or add to `.claude.json` manually:

```json
{
  "mcpServers": {
    "mcp-gdocs": {
      "type": "stdio",
      "command": "/path/to/mcp-gdocs/.venv/Scripts/python",
      "args": ["-m", "mcp_gdocs.server"],
      "env": {
        "GDOCS_CREDENTIALS_PATH": "/path/to/credentials/client_secret.json",
        "GDOCS_TOKEN_PATH": "/path/to/credentials/token.json"
      }
    }
  }
}
```

### 4. Add to Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-gdocs": {
      "command": "/path/to/mcp-gdocs/.venv/Scripts/python",
      "args": ["-m", "mcp_gdocs.server"],
      "env": {
        "GDOCS_CREDENTIALS_PATH": "/path/to/credentials/client_secret.json",
        "GDOCS_TOKEN_PATH": "/path/to/credentials/token.json"
      }
    }
  }
}
```

## Usage Examples

Once connected, any MCP client can use these tools:

**Create a document:**
> "Create a Google Doc from this markdown with title 'Meeting Notes'"

**Search documents:**
> "Find my Google Docs about 'project plan'"

**Update a document:**
> "Update the Google Doc with ID xxx with this new content"

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `GDOCS_CREDENTIALS_PATH` | `credentials/client_secret.json` | Path to Google OAuth client secret |
| `GDOCS_TOKEN_PATH` | `credentials/token.json` | Path to cached OAuth token |

## Architecture

Built with [GRACE framework](https://github.com/Baho73/mcp-gdocs/tree/main/docs). Four modules:

- **M-AUTH** — OAuth2 authentication with token caching
- **M-CONVERTER** — Markdown to DOCX conversion (python-docx + mistune)
- **M-GDRIVE** — Google Drive API client (upload, update, list)
- **M-SERVER** — MCP server (FastMCP, stdio transport)

## Tech Stack

- Python 3.10+
- [MCP SDK](https://github.com/modelcontextprotocol/python-sdk) — Model Context Protocol
- [python-docx](https://python-docx.readthedocs.io/) — DOCX generation
- [mistune](https://github.com/lepture/mistune) — Markdown parsing
- Google Drive API v3

## License

MIT

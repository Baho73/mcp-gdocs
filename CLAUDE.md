# GRACE Framework — mcp-gdocs

## Keywords
MCP, Google Docs, Google Drive, Markdown, DOCX, python-docx, OAuth2, agent tools

## Annotation
MCP-сервер для конвертации Markdown в Google Docs с форматированием: создание, обновление и поиск документов через Google Drive API.

## Core Principles
Inherited from GRACE framework (see parent project hh_answer/CLAUDE.md).

## File Structure
```
src/mcp_gdocs/
  __init__.py
  server.py        — M-SERVER: MCP server (stdio), 3 tools
  auth.py          — M-AUTH: OAuth2 + token caching
  converter.py     — M-CONVERTER: Markdown → DOCX
  gdrive.py        — M-GDRIVE: Google Drive upload/update/list
credentials/       — .gitignored, client_secret.json + token.json
docs/
  knowledge-graph.xml
  development-plan.xml
pyproject.toml     — package config, entry point
```

## Setup
1. Place `client_secret.json` in `credentials/`
2. `pip install -e .`
3. Run `mcp-gdocs` — first run opens browser for OAuth
4. Add to Claude Code: `claude mcp add mcp-gdocs -- D:/Python/mcp-gdocs/.venv/Scripts/python -m mcp_gdocs.server`

## Environment Variables (optional)
- `GDOCS_CREDENTIALS_PATH` — path to client_secret.json
- `GDOCS_TOKEN_PATH` — path to token.json

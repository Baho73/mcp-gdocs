# START_MODULE_CONTRACT
# MODULE_NAME: M-SERVER
# PURPOSE: MCP-сервер на stdio transport, регистрация tools
# INPUTS: MCP tool calls от агента
# OUTPUTS: JSON results (url, doc_id, title)
# DEPENDS: M-AUTH, M-CONVERTER, M-GDRIVE
# END_MODULE_CONTRACT

"""MCP server exposing Google Docs tools to AI agents."""

import os
import logging

from mcp.server.fastmcp import FastMCP

from .auth import get_credentials
from .converter import markdown_to_docx
from .gdrive import upload_as_gdoc, update_gdoc, list_gdocs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-gdocs")

# START_BLOCK_SERVER_INIT
mcp = FastMCP(
    "mcp-gdocs",
    instructions="Create and manage Google Docs from Markdown. Converts Markdown to formatted Google Docs with headings, tables, lists, bold/italic.",
)
# END_BLOCK_SERVER_INIT


def _get_creds():
    """Get credentials using env vars or defaults."""
    creds_path = os.environ.get("GDOCS_CREDENTIALS_PATH")
    token_path = os.environ.get("GDOCS_TOKEN_PATH")
    return get_credentials(creds_path, token_path)


# START_BLOCK_TOOL_CREATE
@mcp.tool()
def markdown_to_gdoc(
    markdown: str,
    title: str = "Untitled Document",
    folder_id: str = "",
) -> dict:
    """Convert Markdown text to a Google Doc with formatting.

    Creates a new Google Doc from Markdown content with full formatting support:
    headings, bold, italic, code, tables, bullet lists.

    Args:
        markdown: Markdown-formatted text to convert.
        title: Title for the Google Doc.
        folder_id: Optional Google Drive folder ID to place the document in.

    Returns:
        Dictionary with doc_id, url, and title of the created document.
    """
    logger.info(f"Creating Google Doc: {title}")
    creds = _get_creds()
    docx_path = markdown_to_docx(markdown)
    try:
        result = upload_as_gdoc(
            creds, docx_path, title,
            folder_id=folder_id if folder_id else None,
        )
        logger.info(f"Created: {result['url']}")
        return result
    finally:
        if os.path.exists(docx_path):
            os.unlink(docx_path)
# END_BLOCK_TOOL_CREATE


# START_BLOCK_TOOL_UPDATE
@mcp.tool()
def update_google_doc(
    doc_id: str,
    markdown: str,
) -> dict:
    """Update an existing Google Doc with new Markdown content.

    Replaces the entire content of the document.

    Args:
        doc_id: The Google Doc ID to update.
        markdown: New Markdown content.

    Returns:
        Dictionary with doc_id, url, and title.
    """
    logger.info(f"Updating Google Doc: {doc_id}")
    creds = _get_creds()
    docx_path = markdown_to_docx(markdown)
    try:
        result = update_gdoc(creds, doc_id, docx_path)
        logger.info(f"Updated: {result['url']}")
        return result
    finally:
        if os.path.exists(docx_path):
            os.unlink(docx_path)
# END_BLOCK_TOOL_UPDATE


# START_BLOCK_TOOL_LIST
@mcp.tool()
def list_google_docs(
    query: str = "",
    max_results: int = 20,
) -> list[dict]:
    """Search for Google Docs in your Drive.

    Args:
        query: Optional search term to filter by document name.
        max_results: Maximum number of documents to return (default 20).

    Returns:
        List of documents with doc_id, title, url, and modified_time.
    """
    logger.info(f"Listing Google Docs, query={query!r}")
    creds = _get_creds()
    return list_gdocs(creds, query=query if query else None, max_results=max_results)
# END_BLOCK_TOOL_LIST


# START_BLOCK_MAIN
def main():
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
# END_BLOCK_MAIN

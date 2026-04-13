# START_MODULE_CONTRACT
# MODULE_NAME: M-GDRIVE
# PURPOSE: Upload DOCX → Google Drive с конвертацией в Google Doc
# INPUTS: docx_path (str), title (str), folder_id (str | None)
# OUTPUTS: { doc_id: str, url: str, title: str }
# ERRORS: UploadError, PermissionError
# END_MODULE_CONTRACT

"""Google Drive client for uploading DOCX and converting to Google Docs."""

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials


# START_BLOCK_UPLOAD
def upload_as_gdoc(
    creds: Credentials,
    docx_path: str,
    title: str,
    folder_id: str | None = None,
) -> dict:
    """Upload a DOCX file to Google Drive and convert it to a Google Doc.

    Args:
        creds: Google API credentials.
        docx_path: Path to the DOCX file.
        title: Title for the Google Doc.
        folder_id: Optional Google Drive folder ID.

    Returns:
        Dict with doc_id, url, and title.
    """
    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": title,
        "mimeType": "application/vnd.google-apps.document",
    }
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(
        docx_path,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        resumable=True,
    )

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name, webViewLink",
    ).execute()

    return {
        "doc_id": file["id"],
        "url": file["webViewLink"],
        "title": file["name"],
    }
# END_BLOCK_UPLOAD


# START_BLOCK_UPDATE
def update_gdoc(
    creds: Credentials,
    doc_id: str,
    docx_path: str,
) -> dict:
    """Replace content of an existing Google Doc by uploading a new DOCX.

    Creates a new revision of the document.
    """
    service = build("drive", "v3", credentials=creds)

    media = MediaFileUpload(
        docx_path,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        resumable=True,
    )

    file = service.files().update(
        fileId=doc_id,
        media_body=media,
        fields="id, name, webViewLink",
    ).execute()

    return {
        "doc_id": file["id"],
        "url": file["webViewLink"],
        "title": file["name"],
    }
# END_BLOCK_UPDATE


# START_BLOCK_LIST
def list_gdocs(
    creds: Credentials,
    query: str | None = None,
    max_results: int = 20,
) -> list[dict]:
    """List Google Docs from Drive.

    Args:
        creds: Google API credentials.
        query: Optional search query (searches name).
        max_results: Maximum number of results.

    Returns:
        List of dicts with doc_id, title, url, modified_time.
    """
    service = build("drive", "v3", credentials=creds)

    q_parts = ["mimeType='application/vnd.google-apps.document'"]
    if query:
        q_parts.append(f"name contains '{query}'")
    q = " and ".join(q_parts)

    results = service.files().list(
        q=q,
        pageSize=max_results,
        fields="files(id, name, webViewLink, modifiedTime)",
        orderBy="modifiedTime desc",
    ).execute()

    return [
        {
            "doc_id": f["id"],
            "title": f["name"],
            "url": f["webViewLink"],
            "modified_time": f.get("modifiedTime", ""),
        }
        for f in results.get("files", [])
    ]
# END_BLOCK_LIST

"""
Google Drive integration for uploading and managing exam papers.
"""

import os
import json
import io
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account

from config import GOOGLE_DRIVE_CREDENTIALS, GOOGLE_DRIVE_FOLDER_ID

SCOPES = ['https://www.googleapis.com/auth/drive']


def get_drive_service():
    """Create and return Google Drive API service."""
    if not os.path.exists(GOOGLE_DRIVE_CREDENTIALS):
        raise FileNotFoundError(
            f"Google Drive credentials not found at {GOOGLE_DRIVE_CREDENTIALS}\n"
            "Please follow the setup instructions to create a service account."
        )
    
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_DRIVE_CREDENTIALS, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=credentials)
    return service


def upload_to_drive(file_path, custom_name=None, file_type="pdf"):
    """
    Upload a file to Google Drive.
    
    Args:
        file_path: Local path to the file
        custom_name: Custom name for the file (without extension)
        file_type: 'pdf' or 'docx'
    
    Returns:
        dict with file info (id, name, webViewLink, webContentLink)
    """
    if not GOOGLE_DRIVE_FOLDER_ID:
        raise ValueError("GOOGLE_DRIVE_FOLDER_ID not set in .env")
    
    service = get_drive_service()
    
    # Determine MIME type
    mime_types = {
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    }
    mime_type = mime_types.get(file_type, 'application/octet-stream')
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if custom_name:
        filename = f"{custom_name}.{file_type}"
    else:
        filename = f"exam_{timestamp}.{file_type}"
    
    # File metadata
    file_metadata = {
        'name': filename,
        'parents': [GOOGLE_DRIVE_FOLDER_ID],
    }
    
    # Upload
    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink, webContentLink, createdTime, size'
    ).execute()
    
    # Make file viewable by anyone with the link
    service.permissions().create(
        fileId=file['id'],
        body={'type': 'anyone', 'role': 'reader'},
    ).execute()
    
    # Get updated file info with sharing link
    file = service.files().get(
        fileId=file['id'],
        fields='id, name, webViewLink, webContentLink, createdTime, size'
    ).execute()
    
    return {
        'id': file['id'],
        'name': file['name'],
        'view_link': file.get('webViewLink', ''),
        'download_link': file.get('webContentLink', ''),
        'created_time': file.get('createdTime', ''),
        'size': file.get('size', '0'),
    }


def list_drive_files(max_results=50):
    """
    List all exam files in the Google Drive folder.
    
    Returns:
        List of file info dicts
    """
    if not GOOGLE_DRIVE_FOLDER_ID:
        return []
    
    try:
        service = get_drive_service()
        
        query = f"'{GOOGLE_DRIVE_FOLDER_ID}' in parents and trashed = false"
        
        results = service.files().list(
            q=query,
            pageSize=max_results,
            fields="files(id, name, webViewLink, webContentLink, createdTime, size, mimeType)",
            orderBy="createdTime desc"
        ).execute()
        
        files = results.get('files', [])
        
        return [{
            'id': f['id'],
            'name': f['name'],
            'view_link': f.get('webViewLink', ''),
            'download_link': f.get('webContentLink', ''),
            'created_time': f.get('createdTime', ''),
            'size': f.get('size', '0'),
            'type': 'pdf' if 'pdf' in f.get('mimeType', '') else 'docx',
        } for f in files]
        
    except Exception as e:
        print(f"Error listing Drive files: {e}")
        return []


def delete_drive_file(file_id):
    """Delete a file from Google Drive."""
    try:
        service = get_drive_service()
        service.files().delete(fileId=file_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


def get_drive_file_info(file_id):
    """Get info about a specific file."""
    try:
        service = get_drive_service()
        file = service.files().get(
            fileId=file_id,
            fields='id, name, webViewLink, webContentLink, createdTime, size, mimeType'
        ).execute()
        return {
            'id': file['id'],
            'name': file['name'],
            'view_link': file.get('webViewLink', ''),
            'download_link': file.get('webContentLink', ''),
            'created_time': file.get('createdTime', ''),
            'size': file.get('size', '0'),
            'type': 'pdf' if 'pdf' in file.get('mimeType', '') else 'docx',
        }
    except Exception as e:
        print(f"Error getting file info: {e}")
        return None

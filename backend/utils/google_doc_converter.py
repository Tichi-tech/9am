"""
Google Doc Converter Utility

Converts Google Docs journal entries into structured JSON format
"""
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
import re
from datetime import datetime

# Scopes required for reading Google Docs
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def get_google_docs_service():
    """
    Authenticate and return Google Docs API service

    For MVP, this uses OAuth flow. In production, use service accounts.
    """
    creds = None

    # Token file stores the user's access and refresh tokens
    token_path = os.path.join(os.path.dirname(__file__), '..', 'token.pickle')
    creds_path = os.getenv('GOOGLE_DOCS_CREDENTIALS_PATH', 'credentials.json')

    # Load existing credentials if available
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # For MVP: This requires manual OAuth flow
            # In production, use service account
            if os.path.exists(creds_path):
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)
            else:
                raise Exception(
                    "Google Docs credentials not found. "
                    "Download credentials.json from Google Cloud Console"
                )

        # Save credentials for next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('docs', 'v1', credentials=creds)

def extract_doc_id_from_url(url):
    """Extract document ID from Google Docs URL"""
    match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', url)
    if match:
        return match.group(1)
    # If no match, assume the string itself is the doc ID
    return url

def parse_doc_content(doc_content):
    """
    Parse document content into structured format

    Expected format in Google Doc:
    Date: 2025-01-12
    Time: 22:30

    Journal entry text goes here...
    """
    full_text = ""

    # Extract text from document structure
    for element in doc_content:
        if 'paragraph' in element:
            paragraph_text = ""
            if 'elements' in element['paragraph']:
                for text_elem in element['paragraph']['elements']:
                    if 'textRun' in text_elem:
                        paragraph_text += text_elem['textRun']['content']
            full_text += paragraph_text

    # Parse date and time from content
    date_match = re.search(r'Date:\s*(\d{4}-\d{2}-\d{2})', full_text, re.IGNORECASE)
    time_match = re.search(r'Time:\s*(\d{2}:\d{2})', full_text, re.IGNORECASE)

    # Extract the journal text (everything after Date and Time)
    text_start = 0
    if date_match:
        text_start = max(text_start, date_match.end())
    if time_match:
        text_start = max(text_start, time_match.end())

    journal_text = full_text[text_start:].strip()

    return {
        'date': date_match.group(1) if date_match else None,
        'time': time_match.group(1) if time_match else None,
        'text': journal_text
    }

def convert_google_doc_to_json(doc_url, entry_date=None):
    """
    Main function to convert Google Doc to JSON format

    Args:
        doc_url: Google Docs URL or document ID
        entry_date: Optional date override in YYYY-MM-DD format

    Returns:
        Dictionary with structured journal entry
    """
    try:
        # For MVP, we can also accept plain text instead of requiring Google Docs API
        # This allows testing without Google credentials
        if not doc_url.startswith('http'):
            # Assume it's plain text for testing
            return {
                'date': entry_date or datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M'),
                'text': doc_url
            }

        # Extract document ID
        doc_id = extract_doc_id_from_url(doc_url)

        # Get Google Docs service
        service = get_google_docs_service()

        # Retrieve the document
        document = service.documents().get(documentId=doc_id).execute()

        # Parse content
        parsed = parse_doc_content(document.get('body', {}).get('content', []))

        # Use provided date if parsing didn't find one
        if not parsed['date'] and entry_date:
            parsed['date'] = entry_date

        # Validate date format
        if not parsed['date']:
            parsed['date'] = datetime.now().strftime('%Y-%m-%d')

        # Default time if not found
        if not parsed['time']:
            parsed['time'] = '00:00'

        return parsed

    except Exception as e:
        # For MVP: if Google Docs API fails, return error with helpful message
        raise Exception(
            f"Failed to convert Google Doc: {str(e)}. "
            f"For testing without Google Docs API, pass plain text instead of URL."
        )

def convert_text_to_json(text, entry_date=None, entry_time=None):
    """
    Simple converter for plain text (useful for MVP testing)

    Args:
        text: Journal entry text
        entry_date: Date in YYYY-MM-DD format
        entry_time: Time in HH:MM format

    Returns:
        Dictionary with structured journal entry
    """
    return {
        'date': entry_date or datetime.now().strftime('%Y-%m-%d'),
        'time': entry_time or datetime.now().strftime('%H:%M'),
        'text': text
    }

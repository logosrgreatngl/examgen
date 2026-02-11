"""Configuration for the web app."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
A4F_API_KEY = os.environ.get("A4F_API_KEY", "")
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", "K85187082488957")

# API Settings
A4F_API_URL = "https://api.a4f.co/v1/chat/completions"
A4F_MODEL = "provider-5/gemini-3-pro"
OCR_API_URL = "https://api.ocr.space/parse/image"

# File Settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")
CREDENTIALS_FOLDER = os.path.join(BASE_DIR, "credentials")
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tiff", "webp"}
AUTO_DELETE_DAYS = 7

# Academy Name
ACADEMY_NAME = "GHORI ACADEMY"

# Google Drive Settings
GOOGLE_DRIVE_CREDENTIALS = os.path.join(CREDENTIALS_FOLDER, "google_drive_key.json")
GOOGLE_DRIVE_FOLDER_ID = os.environ.get("GOOGLE_DRIVE_FOLDER_ID", "")  # Set this in .env
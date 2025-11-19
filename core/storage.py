from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class CustomStorage(FileSystemStorage):
    """Custom storage for CKEditor 5 to handle file uploads properly"""
    
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if base_url is None:
            base_url = os.path.join(settings.MEDIA_URL, 'uploads/')
        super().__init__(location, base_url)
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from persons.models import validate_file_type, ALLOWED_FILE_EXTENSIONS

print("Validators imported successfully")
print("Allowed extensions:", ALLOWED_FILE_EXTENSIONS)

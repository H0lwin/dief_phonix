#!/usr/bin/env python
import os
import django
import sys
import io
import json
from urllib.parse import urlencode

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from django.test import Client

client = Client()

print("=" * 80)
print("TESTING API ENDPOINT: /persons/api/services-by-category/")
print("=" * 80)

service_types = ['commercial', 'registration', 'legal', 'leasing', 'loan']

for service_type in service_types:
    url = f'/persons/api/services-by-category/?service_type={service_type}'
    print(f"\nTesting: {url}")
    response = client.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Content Type: {response.get('Content-Type')}")
    
    try:
        data = json.loads(response.content)
        print(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw Response: {response.content}")

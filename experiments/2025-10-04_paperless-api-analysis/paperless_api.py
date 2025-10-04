#!/usr/bin/env python3
"""
Paperless-ngx API utility for querying document statistics and metadata.
"""

import requests
import json
from collections import defaultdict

class PaperlessAPI:
    def __init__(self, base_url, token=None, username=None, password=None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

        if token:
            self.session.headers.update({'Authorization': f'Token {token}'})
        elif username and password:
            # Try to authenticate and get token
            auth_response = self.session.post(f'{self.base_url}/api/auth/', {
                'username': username,
                'password': password
            })
            if auth_response.status_code == 200:
                token = auth_response.json().get('token')
                self.session.headers.update({'Authorization': f'Token {token}'})
            else:
                raise Exception(f"Authentication failed: {auth_response.text}")

    def get_document_types(self):
        """Get all document types from paperless."""
        response = self.session.get(f'{self.base_url}/api/document_types/')
        response.raise_for_status()
        return response.json()

    def get_documents(self, page_size=100, document_type=None):
        """Get documents, optionally filtered by document type."""
        url = f'{self.base_url}/api/documents/'
        params = {'page_size': page_size}

        if document_type:
            params['document_type__id'] = document_type

        all_documents = []
        next_url = url

        while next_url:
            if next_url == url:
                response = self.session.get(next_url, params=params)
            else:
                response = self.session.get(next_url)

            response.raise_for_status()
            data = response.json()

            all_documents.extend(data['results'])
            next_url = data.get('next')

            print(f"Fetched {len(all_documents)} documents so far...")

        return all_documents

    def get_document_type_stats(self):
        """Get statistics on documents by type."""
        print("Fetching document types...")
        doc_types = self.get_document_types()

        print("Fetching all documents...")
        documents = self.get_documents()

        # Count documents by type
        type_counts = defaultdict(int)
        type_names = {dt['id']: dt['name'] for dt in doc_types['results']}

        # Add "No Type" for documents without a type
        type_names[None] = "No Type"

        for doc in documents:
            doc_type_id = doc.get('document_type')
            type_counts[doc_type_id] += 1

        # Prepare results
        results = []
        for type_id, count in type_counts.items():
            results.append({
                'id': type_id,
                'name': type_names.get(type_id, f"Unknown (ID: {type_id})"),
                'count': count
            })

        # Sort by count descending
        results.sort(key=lambda x: x['count'], reverse=True)

        return {
            'total_documents': len(documents),
            'total_types': len(doc_types['results']),
            'type_stats': results
        }

    def get_correspondents(self):
        """Get all correspondents."""
        response = self.session.get(f'{self.base_url}/api/correspondents/')
        response.raise_for_status()
        return response.json()

    def get_tags(self):
        """Get all tags."""
        response = self.session.get(f'{self.base_url}/api/tags/')
        response.raise_for_status()
        return response.json()

def main():
    # Configuration from previous experiment (EXPERIMENTS.md)
    PAPERLESS_URL = "http://192.168.1.7:8000"

    # Try to get token from environment variable (as used in previous experiment)
    import os
    TOKEN = os.getenv('PAPERLESS_API_KEY')

    # Fallback options
    USERNAME = None  # Set if using username/password
    PASSWORD = None  # Set if using username/password

    if not any([TOKEN, (USERNAME and PASSWORD)]):
        print("Authentication required:")
        print("- Set PAPERLESS_API_KEY environment variable, OR")
        print("- Set USERNAME and PASSWORD in the script")
        print(f"- From EXPERIMENTS.md: Previous format was 'Authorization: Token ${{PAPERLESS_API_KEY}}'")
        return

    try:
        # Connect to paperless
        print(f"Connecting to paperless at {PAPERLESS_URL}...")
        api = PaperlessAPI(PAPERLESS_URL, token=TOKEN, username=USERNAME, password=PASSWORD)

        # Get document type statistics
        print("\nGetting document type statistics...")
        stats = api.get_document_type_stats()

        print(f"\n=== Document Type Statistics ===")
        print(f"Total Documents: {stats['total_documents']}")
        print(f"Total Document Types: {stats['total_types']}")
        print("\nDocuments by Type:")
        print("-" * 50)

        for type_stat in stats['type_stats']:
            type_name = type_stat['name']
            count = type_stat['count']
            percentage = (count / stats['total_documents']) * 100
            print(f"{type_name:<30} {count:>5} ({percentage:>5.1f}%)")

        # Also show some additional stats
        print(f"\n=== Additional Information ===")

        # Get correspondents count
        correspondents = api.get_correspondents()
        print(f"Total Correspondents: {correspondents['count']}")

        # Get tags count
        tags = api.get_tags()
        print(f"Total Tags: {tags['count']}")

    except requests.exceptions.ConnectionError:
        print(f"ERROR: Could not connect to paperless at {PAPERLESS_URL}")
        print("Make sure paperless is running and the URL is correct")
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP error occurred: {e}")
        print("Check your authentication credentials")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    main()
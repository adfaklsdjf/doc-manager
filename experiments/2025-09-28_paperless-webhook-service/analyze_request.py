#!/usr/bin/env python3
"""
Utility script to analyze saved webhook requests.
Helps extract and work with the multipart data from paperless webhooks.
"""

import os
import sys
from email import message_from_bytes
from email.mime.multipart import MIMEMultipart
import re

def parse_http_request(file_path):
    """Parse a saved HTTP request file."""
    with open(file_path, 'rb') as f:
        content = f.read()

    # Split headers and body
    header_end = content.find(b'\r\n\r\n')
    if header_end == -1:
        print(f"Error: Could not find header/body separator in {file_path}")
        return None, None

    headers_section = content[:header_end].decode('utf-8')
    body = content[header_end + 4:]  # Skip the \r\n\r\n

    # Parse request line and headers
    lines = headers_section.split('\r\n')
    request_line = lines[0]
    headers = {}

    for line in lines[1:]:
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()

    return {
        'request_line': request_line,
        'headers': headers,
        'body': body
    }

def extract_multipart_data(headers, body):
    """Extract form data and files from multipart body."""
    content_type = headers.get('Content-Type', '')
    if not content_type.startswith('multipart/form-data'):
        print("Not a multipart request")
        return None

    # Extract boundary
    boundary_match = re.search(r'boundary=([^;\s]+)', content_type)
    if not boundary_match:
        print("Could not find multipart boundary")
        return None

    boundary = boundary_match.group(1)

    # Parse multipart data using email library
    # Reconstruct as MIME message
    mime_content = f"Content-Type: {content_type}\r\n\r\n".encode() + body

    try:
        msg = message_from_bytes(mime_content)
        parts = []

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue

                disposition = part.get('Content-Disposition', '')
                if 'form-data' in disposition:
                    # Extract name and filename
                    name_match = re.search(r'name="([^"]+)"', disposition)
                    filename_match = re.search(r'filename="([^"]+)"', disposition)

                    part_info = {
                        'name': name_match.group(1) if name_match else None,
                        'filename': filename_match.group(1) if filename_match else None,
                        'content_type': part.get_content_type(),
                        'content': part.get_payload(decode=True)
                    }
                    parts.append(part_info)

        return parts

    except Exception as e:
        print(f"Error parsing multipart data: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_request.py <request_file>")
        print("\nAvailable request files:")
        saved_dir = "saved_requests"
        if os.path.exists(saved_dir):
            for f in sorted(os.listdir(saved_dir)):
                if f.endswith(('.txt', '.http')):
                    print(f"  {f}")
        return

    file_path = sys.argv[1]
    if not file_path.startswith('saved_requests/'):
        file_path = f"saved_requests/{file_path}"

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Analyzing: {file_path}")
    print("=" * 50)

    # Parse the HTTP request
    request_data = parse_http_request(file_path)
    if not request_data:
        return

    print(f"Request: {request_data['request_line']}")
    print(f"Content-Type: {request_data['headers'].get('Content-Type', 'unknown')}")
    print(f"Content-Length: {request_data['headers'].get('Content-Length', 'unknown')}")
    print()

    # If it's multipart, extract the parts
    if 'multipart/form-data' in request_data['headers'].get('Content-Type', ''):
        print("Extracting multipart data...")
        parts = extract_multipart_data(request_data['headers'], request_data['body'])

        if parts:
            for i, part in enumerate(parts):
                print(f"\nPart {i + 1}:")
                print(f"  Name: {part['name']}")
                print(f"  Filename: {part['filename']}")
                print(f"  Content-Type: {part['content_type']}")
                print(f"  Size: {len(part['content']) if part['content'] else 0} bytes")

                # If it's a PDF, offer to save it
                if part['filename'] and part['filename'].endswith('.pdf'):
                    save_path = f"extracted_{part['filename']}"
                    with open(save_path, 'wb') as f:
                        f.write(part['content'])
                    print(f"  ✓ Saved PDF to: {save_path}")

    print("\nAnalysis complete!")

if __name__ == '__main__':
    main()
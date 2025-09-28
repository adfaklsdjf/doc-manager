#!/usr/bin/env python3
"""
Debug PDF text extraction using pypdf (newer library)
"""

import pypdf

def debug_pypdf_extraction():
    pdf_path = "/Users/brianweaver/code/doc-manager/samples/09162025_RESPONSE REQUESTED BY September 16,2025.pdf"

    print(f"Analyzing PDF with pypdf: {pdf_path}")

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            print(f"Total pages: {len(pdf_reader.pages)}")

            for i, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                print(f"\n=== PAGE {i} ===")
                print(f"Character count: {len(text)}")
                if text.strip():
                    print(f"Text preview (first 300 chars):")
                    print(text[:300])
                else:
                    print("No text extracted")
                print("=" * 50)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_pypdf_extraction()
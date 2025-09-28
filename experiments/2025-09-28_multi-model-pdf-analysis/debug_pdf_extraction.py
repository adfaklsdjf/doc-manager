#!/usr/bin/env python3
"""
Debug PDF text extraction to see what PyPDF2 is actually reading
"""

import PyPDF2

def debug_pdf_extraction():
    pdf_path = "/Users/brianweaver/code/doc-manager/samples/09162025_RESPONSE REQUESTED BY September 16,2025.pdf"

    print(f"Analyzing PDF: {pdf_path}")

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            print(f"Total pages: {len(pdf_reader.pages)}")

            for i, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                print(f"\n=== PAGE {i} ===")
                print(f"Character count: {len(text)}")
                print(f"First 200 characters:")
                print(repr(text[:200]))
                print(f"Text preview:")
                print(text[:300])
                print("=" * 50)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_pdf_extraction()
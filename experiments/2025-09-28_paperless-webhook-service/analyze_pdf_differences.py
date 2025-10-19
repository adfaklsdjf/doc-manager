#!/usr/bin/env python3
"""
Analyze differences between original PDF and paperless-processed PDF
to understand why text extraction is failing.
"""

import os
import sys
from pathlib import Path

def analyze_file_properties(file_path):
    """Analyze basic file properties."""
    path = Path(file_path)
    if not path.exists():
        return None

    stat = path.stat()
    return {
        'size': stat.st_size,
        'name': path.name,
        'exists': True,
        'readable': os.access(file_path, os.R_OK)
    }

def read_pdf_metadata(file_path):
    """Try to read PDF metadata using different methods."""
    results = {}

    # Try with pypdf first (lightweight)
    try:
        import pypdf
        with open(file_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            results['pypdf'] = {
                'pages': len(reader.pages),
                'metadata': reader.metadata,
                'encrypted': reader.is_encrypted,
                'success': True
            }
    except Exception as e:
        results['pypdf'] = {'error': str(e), 'success': False}

    # Try with pdfplumber (more robust)
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            results['pdfplumber'] = {
                'pages': len(pdf.pages),
                'metadata': pdf.metadata,
                'success': True
            }
    except Exception as e:
        results['pdfplumber'] = {'error': str(e), 'success': False}

    return results

def extract_text_sample(file_path, method='pypdf'):
    """Extract a sample of text using specified method."""
    try:
        if method == 'pypdf':
            import pypdf
            with open(file_path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                if len(reader.pages) > 0:
                    text = reader.pages[0].extract_text()
                    return {
                        'method': method,
                        'text_length': len(text),
                        'first_100_chars': text[:100],
                        'success': True,
                        'full_text': text  # For detailed analysis
                    }

        elif method == 'pdfplumber':
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                if len(pdf.pages) > 0:
                    text = pdf.pages[0].extract_text()
                    return {
                        'method': method,
                        'text_length': len(text) if text else 0,
                        'first_100_chars': text[:100] if text else '',
                        'success': True,
                        'full_text': text  # For detailed analysis
                    }

    except Exception as e:
        return {'method': method, 'error': str(e), 'success': False}

def analyze_binary_differences(file1_path, file2_path):
    """Compare binary content of two files."""
    try:
        with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
            content1 = f1.read()
            content2 = f2.read()

            # Check if files are identical
            identical = content1 == content2

            # Look at headers
            header1 = content1[:100]
            header2 = content2[:100]

            return {
                'identical': identical,
                'size_diff': len(content2) - len(content1),
                'header1': header1,
                'header2': header2,
                'header_identical': header1 == header2
            }
    except Exception as e:
        return {'error': str(e)}

def main():
    # File paths
    original_file = "../../samples/FirstEnergy-110160220841-090827483643-.pdf"
    paperless_file = "../../samples/2025-10-03-Unlesbarer-Dokumentinhalt.pdf"

    print("=== PDF Analysis: Original vs Paperless ===\n")

    # Analyze file properties
    print("File Properties:")
    orig_props = analyze_file_properties(original_file)
    paper_props = analyze_file_properties(paperless_file)

    print(f"Original:  {orig_props}")
    print(f"Paperless: {paper_props}")
    print()

    if not orig_props or not paper_props:
        print("ERROR: One or both files not found!")
        return

    # Analyze binary differences
    print("Binary Comparison:")
    binary_diff = analyze_binary_differences(original_file, paperless_file)
    print(f"Files identical: {binary_diff.get('identical', False)}")
    print(f"Size difference: {binary_diff.get('size_diff', 'unknown')} bytes")
    print(f"Headers identical: {binary_diff.get('header_identical', False)}")
    print()

    # PDF metadata analysis
    print("PDF Metadata Analysis:")
    print("\nOriginal file:")
    orig_meta = read_pdf_metadata(original_file)
    for method, data in orig_meta.items():
        if data.get('success'):
            print(f"  {method}: {data.get('pages', 'unknown')} pages, encrypted: {data.get('encrypted', 'unknown')}")
        else:
            print(f"  {method}: ERROR - {data.get('error', 'unknown')}")

    print("\nPaperless file:")
    paper_meta = read_pdf_metadata(paperless_file)
    for method, data in paper_meta.items():
        if data.get('success'):
            print(f"  {method}: {data.get('pages', 'unknown')} pages, encrypted: {data.get('encrypted', 'unknown')}")
        else:
            print(f"  {method}: ERROR - {data.get('error', 'unknown')}")
    print()

    # Text extraction comparison
    print("Text Extraction Comparison:")
    methods = ['pypdf', 'pdfplumber']

    for method in methods:
        print(f"\n--- Using {method} ---")

        print("Original file:")
        orig_text = extract_text_sample(original_file, method)
        if orig_text.get('success'):
            print(f"  Length: {orig_text.get('text_length', 0)} characters")
            print(f"  First 100: {repr(orig_text.get('first_100_chars', ''))}")
        else:
            print(f"  ERROR: {orig_text.get('error', 'unknown')}")

        print("Paperless file:")
        paper_text = extract_text_sample(paperless_file, method)
        if paper_text.get('success'):
            print(f"  Length: {paper_text.get('text_length', 0)} characters")
            print(f"  First 100: {repr(paper_text.get('first_100_chars', ''))}")
        else:
            print(f"  ERROR: {paper_text.get('error', 'unknown')}")

    # Detailed character analysis
    print("\n=== Detailed Character Analysis ===")

    # Get full text from both files for analysis
    orig_text_full = extract_text_sample(original_file, 'pypdf')
    paper_text_full = extract_text_sample(paperless_file, 'pypdf')

    if orig_text_full.get('success') and paper_text_full.get('success'):
        orig_text = orig_text_full.get('full_text', '')
        paper_text = paper_text_full.get('full_text', '')

        print(f"Original text length: {len(orig_text)}")
        print(f"Paperless text length: {len(paper_text)}")

        # Character frequency analysis
        if paper_text:
            # Count special characters
            special_chars = {}
            for char in paper_text[:500]:  # First 500 chars
                if ord(char) > 127 or char in '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f':
                    special_chars[char] = special_chars.get(char, 0) + 1

            print(f"Special characters in paperless text: {len(special_chars)}")
            if special_chars:
                print("Most common special characters:")
                for char, count in sorted(special_chars.items(), key=lambda x: x[1], reverse=True)[:10]:
                    print(f"  {repr(char)}: {count} times")

        # Show actual text comparison
        print(f"\nFirst 200 characters comparison:")
        print(f"Original: {repr(orig_text[:200])}")
        print(f"Paperless: {repr(paper_text[:200])}")

if __name__ == '__main__':
    main()
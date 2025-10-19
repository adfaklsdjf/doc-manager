#!/usr/bin/env python3
"""
Compare text extraction between WESTFIELD.pdf and WESTFIELD_ABBYY_OCR.pdf
"""

import pypdf

def extract_and_compare():
    files = [
        "/Users/brianweaver/code/doc-manager/samples/2024-12-28_WESTFIELD.pdf",
        "/Users/brianweaver/code/doc-manager/samples/2024-12-28_WESTFIELD_ABBYY_OCR.pdf"
    ]

    results = {}

    for pdf_path in files:
        filename = pdf_path.split('/')[-1]
        print(f"\n{'='*60}")
        print(f"ANALYZING: {filename}")
        print('='*60)

        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                pages_data = []
                total_chars = 0

                print(f"Total pages: {len(pdf_reader.pages)}")

                for i, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    char_count = len(text)
                    total_chars += char_count

                    pages_data.append({
                        'page': i,
                        'char_count': char_count,
                        'text': text
                    })

                    print(f"\nPage {i}: {char_count} characters")
                    if char_count > 0:
                        # Show first 200 characters
                        preview = text[:200].replace('\n', '\\n')
                        print(f"Preview: {preview}")
                        if char_count > 200:
                            print("...")
                    else:
                        print("No text extracted")

                results[filename] = {
                    'total_pages': len(pdf_reader.pages),
                    'total_characters': total_chars,
                    'pages': pages_data
                }

                print(f"\nSUMMARY for {filename}:")
                print(f"  Total characters extracted: {total_chars}")
                print(f"  Average per page: {total_chars / len(pdf_reader.pages):.1f}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            results[filename] = {'error': str(e)}

    # Compare results
    print(f"\n{'='*60}")
    print("COMPARISON")
    print('='*60)

    file1, file2 = list(results.keys())

    if 'error' not in results[file1] and 'error' not in results[file2]:
        chars1 = results[file1]['total_characters']
        chars2 = results[file2]['total_characters']

        print(f"{file1}: {chars1} total characters")
        print(f"{file2}: {chars2} total characters")
        print(f"Difference: {chars2 - chars1} characters")

        if chars1 == 0 and chars2 > 0:
            print("🎯 CLEAR DIFFERENCE: OCR version has extractable text!")
        elif chars1 > 0 and chars2 > 0:
            print("📄 Both have extractable text, comparing quality...")
        elif chars1 == 0 and chars2 == 0:
            print("❌ Neither has extractable text")

        # Show sample content from OCR version if available
        if chars2 > 0:
            print(f"\nSample content from {file2}:")
            print("-" * 40)
            sample_text = results[file2]['pages'][0]['text'][:500]
            print(sample_text)
            if len(results[file2]['pages'][0]['text']) > 500:
                print("...")

    return results

if __name__ == "__main__":
    extract_and_compare()
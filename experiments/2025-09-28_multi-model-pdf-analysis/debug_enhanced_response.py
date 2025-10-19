#!/usr/bin/env python3
"""
Debug the enhanced analysis response to see what's being returned
"""

from llm_document_analyzer import DocumentAnalyzer

def debug_response():
    """Debug what the enhanced analysis is returning."""

    pdf_path = "/Users/brianweaver/code/doc-manager/samples/2024-12-28_WESTFIELD_ABBYY_OCR.pdf"

    print("🔍 Debug Enhanced Analysis Response")
    print("=" * 40)

    try:
        analyzer = DocumentAnalyzer()
        result = analyzer.analyze_with_text_extraction(pdf_path, "claude-3-5-haiku-latest")

        print("Raw result keys:", list(result.keys()))

        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
            return

        if 'response' in result:
            print("\n📄 RAW RESPONSE:")
            print("-" * 30)
            print(repr(result['response'][:200]))  # First 200 chars with escapes visible
            print("\n📄 FORMATTED RESPONSE:")
            print("-" * 30)
            print(result['response'][:500])  # First 500 chars
            if len(result['response']) > 500:
                print("\n... [truncated] ...")
                print(result['response'][-200:])  # Last 200 chars

        else:
            print("❌ No 'response' key in result")

    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_response()
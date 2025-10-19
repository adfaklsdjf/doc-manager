#!/usr/bin/env python3
"""
Test enhanced analysis with ABBYY OCR PDF and updated prompts
"""

import json
import time
from llm_document_analyzer import DocumentAnalyzer

def test_enhanced_analysis():
    """Test the enhanced analysis on ABBYY OCR PDF."""

    pdf_path = "/Users/brianweaver/code/doc-manager/samples/2024-12-28_WESTFIELD_ABBYY_OCR.pdf"

    print("🧪 Enhanced Analysis Test")
    print("=" * 50)
    print(f"Target: WESTFIELD_ABBYY_OCR.pdf")
    print(f"Model: claude-3-5-haiku-latest")
    print(f"Method: Text extraction with enhanced prompts")
    print()

    try:
        analyzer = DocumentAnalyzer()

        print("📄 Starting analysis...")
        start_time = time.time()

        result = analyzer.analyze_with_text_extraction(pdf_path, "claude-3-5-haiku-latest")

        processing_time = time.time() - start_time

        print(f"⏱️  Processing time: {processing_time:.2f} seconds")
        print()

        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
            return

        print("📊 ANALYSIS RESULTS:")
        print("=" * 30)

        # Parse the response
        try:
            if 'response' in result:
                analysis = json.loads(result['response'])

                print(f"🎯 Confidence: {analysis.get('analysis_confidence', 'N/A')}%")
                print(f"📄 Document Count: {analysis.get('document_count', 'N/A')}")
                print(f"📋 Total Pages: {analysis.get('total_pages', 'N/A')}")
                print(f"⚠️  Importance: {analysis.get('document_importance', 'N/A')}")
                print(f"🚨 Action Required: {analysis.get('action_required', 'N/A')}")
                print()

                print("📝 KEY SUMMARY:")
                print(f"   {analysis.get('key_summary', 'N/A')}")
                print()

                print("🔄 REORDERING ASSESSMENT:")
                reordering = analysis.get('reordering_needed', {})
                print(f"   Required: {reordering.get('required', 'N/A')}")
                if reordering.get('required'):
                    print(f"   Suggested Order: {reordering.get('suggested_order', 'N/A')}")
                    print(f"   Reasoning: {reordering.get('reasoning', 'N/A')}")
                print()

                print("📋 RECOMMENDED ACTIONS:")
                actions = analysis.get('recommended_actions', [])
                for i, action in enumerate(actions, 1):
                    print(f"   {i}. Action: {action.get('action', 'N/A')}")
                    print(f"      Pages: {action.get('pages', 'N/A')}")
                    print(f"      Type: {action.get('document_type', 'N/A')}")
                    print(f"      Filename: {action.get('suggested_filename', 'N/A')}")
                    print(f"      Tags: {action.get('tags', 'N/A')}")
                    print(f"      Reasoning: {action.get('reasoning', 'N/A')}")
                    print()

                print("🔍 DUPLICATES DETECTED:")
                duplicates = analysis.get('duplicates_detected', [])
                if duplicates:
                    for i, dup in enumerate(duplicates, 1):
                        print(f"   {i}. Pages: {dup.get('pages', 'N/A')}")
                        print(f"      Similarity: {dup.get('similarity', 'N/A')}")
                        print(f"      Reasoning: {dup.get('reasoning', 'N/A')}")
                        print()
                else:
                    print("   None detected")

                # Save detailed results
                output_file = "enhanced_analysis_results.json"
                with open(output_file, 'w') as f:
                    json.dump({
                        "test_metadata": {
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "pdf_file": pdf_path,
                            "model": "claude-3-5-haiku-latest",
                            "processing_time": processing_time
                        },
                        "raw_result": result,
                        "parsed_analysis": analysis
                    }, f, indent=2)

                print(f"💾 Detailed results saved to: {output_file}")

            else:
                print("❌ No response in result")
                print("Raw result:", result)

        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print("Raw response:", result.get('response', 'No response'))

    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_enhanced_analysis()
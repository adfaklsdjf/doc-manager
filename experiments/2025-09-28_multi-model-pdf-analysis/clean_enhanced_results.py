#!/usr/bin/env python3
"""
Extract and display clean enhanced analysis results
"""

import json
import re
from llm_document_analyzer import DocumentAnalyzer

def extract_json_from_response(response_text):
    """Extract JSON from response that may have extra text."""
    # Find the first { and last }
    start = response_text.find('{')
    if start == -1:
        return None

    # Count braces to find the matching closing brace
    brace_count = 0
    end = start
    for i, char in enumerate(response_text[start:], start):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i + 1
                break

    return response_text[start:end]

def run_clean_analysis():
    """Run enhanced analysis and display clean results."""

    pdf_path = "/Users/brianweaver/code/doc-manager/samples/2024-12-28_WESTFIELD_ABBYY_OCR.pdf"

    print("🎯 Enhanced Analysis - Clean Results")
    print("=" * 45)

    try:
        analyzer = DocumentAnalyzer()
        result = analyzer.analyze_with_text_extraction(pdf_path, "claude-3-5-haiku-latest")

        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
            return

        response_text = result.get('response', '')
        json_text = extract_json_from_response(response_text)

        if not json_text:
            print("❌ No JSON found in response")
            return

        try:
            analysis = json.loads(json_text)

            print("✅ SUCCESSFUL ANALYSIS:")
            print(f"🎯 Confidence: {analysis['analysis_confidence']}%")
            print(f"📄 Documents: {analysis['document_count']}")
            print(f"📋 Pages: {analysis['total_pages']}")
            print(f"⚠️  Importance: {analysis['document_importance'].upper()}")
            print(f"🚨 Action Required: {'YES' if analysis['action_required'] else 'NO'}")
            print()

            print("📝 SUMMARY:")
            print(f"   {analysis['key_summary']}")
            print()

            print("🔄 REORDERING:")
            reorder = analysis['reordering_needed']
            print(f"   Required: {'YES' if reorder['required'] else 'NO'}")
            print(f"   Order: {reorder['suggested_order']}")
            print(f"   Reason: {reorder['reasoning']}")
            print()

            print("📋 ACTIONS:")
            for action in analysis['recommended_actions']:
                print(f"   • {action['action'].upper()}: Pages {action['pages']}")
                print(f"     Type: {action['document_type']}")
                print(f"     File: {action['suggested_filename']}")
                print(f"     Tags: {', '.join(action['tags'])}")
                print(f"     Why: {action['reasoning']}")
                print()

            print("🔍 DUPLICATES:")
            if analysis['duplicates_detected']:
                for dup in analysis['duplicates_detected']:
                    print(f"   • Pages {dup['pages']}: {dup['similarity']} similarity")
                    print(f"     Reason: {dup['reasoning']}")
            else:
                print("   None detected")
            print()

            # Check for extra observations
            if len(response_text) > len(json_text):
                extra_text = response_text[len(json_text):].strip()
                if extra_text:
                    print("💡 ADDITIONAL OBSERVATIONS:")
                    print(f"   {extra_text}")
                    print()

            # Save clean results
            clean_results = {
                "timestamp": "2025-09-28",
                "model": "claude-3-5-haiku-latest",
                "pdf": "WESTFIELD_ABBYY_OCR.pdf",
                "analysis": analysis,
                "extra_observations": response_text[len(json_text):].strip() if len(response_text) > len(json_text) else None
            }

            with open("enhanced_analysis_clean.json", 'w') as f:
                json.dump(clean_results, f, indent=2)

            print("💾 Clean results saved to: enhanced_analysis_clean.json")

        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print("Extracted JSON text:")
            print(json_text)

    except Exception as e:
        print(f"❌ Analysis failed: {e}")

if __name__ == "__main__":
    run_clean_analysis()
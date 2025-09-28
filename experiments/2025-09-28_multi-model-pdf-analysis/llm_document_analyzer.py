#!/usr/bin/env python3
"""
LLM Document Analyzer - Programmatic API Testing
Tests different approaches for PDF analysis using Anthropic's API
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import anthropic
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed. Run: pip install anthropic")
    exit(1)

try:
    import PyPDF2
except ImportError:
    print("Warning: PyPDF2 not installed. Text extraction method will be skipped.")
    print("To install: pip install PyPDF2")
    PyPDF2 = None


class DocumentAnalyzer:
    """Analyzes PDF documents using different LLM models and input methods."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Anthropic API key from environment or parameter."""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = Anthropic(api_key=self.api_key)

    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict[str, str]]:
        """Extract text from PDF using PyPDF2."""
        if not PyPDF2:
            return []

        pages = []
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for i, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    pages.append({
                        'page_number': i,
                        'text': text,
                        'char_count': len(text)
                    })
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")

        return pages

    def analyze_with_text_extraction(self, pdf_path: str, model: str = "claude-3-haiku-20240307") -> Dict:
        """Analyze PDF by first extracting text, then sending to LLM."""
        start_time = time.time()

        # Extract text
        pages = self.extract_text_from_pdf(pdf_path)
        if not pages:
            return {"error": "Failed to extract text from PDF"}

        # Prepare text for analysis
        text_content = "\\n\\n".join([
            f"=== PAGE {page['page_number']} ===\\n{page['text']}"
            for page in pages
        ])

        prompt = f"""You are analyzing a PDF document for intelligent processing. Below is the text content extracted from each page of the document.

Your task is to:
1. Identify distinct documents within this PDF
2. Detect duplicate pages or content
3. Find blank, illegible, or artifact pages
4. Recommend specific actions (keep/remove/split pages)
5. Suggest appropriate filenames for extracted documents
6. Provide confidence level (0-100%)

Format your response as structured JSON with the following schema:
{{
  "analysis_confidence": <number>,
  "document_count": <number>,
  "total_pages": <number>,
  "recommended_actions": [
    {{
      "action": "extract|remove|keep",
      "pages": [list of page numbers],
      "document_type": "description",
      "suggested_filename": "filename.pdf",
      "tags": ["tag1", "tag2"],
      "reasoning": "explanation"
    }}
  ],
  "duplicates_detected": [
    {{
      "pages": [page numbers],
      "similarity": "exact|high|partial",
      "reasoning": "explanation"
    }}
  ]
}}

PDF Text Content:
{text_content}"""

        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=4000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )

            processing_time = time.time() - start_time

            return {
                "method": "text_extraction",
                "model": model,
                "processing_time": processing_time,
                "input_tokens": len(prompt.split()),
                "response": response.content[0].text,
                "usage": response.usage._asdict() if hasattr(response, 'usage') else None
            }

        except Exception as e:
            return {
                "method": "text_extraction",
                "model": model,
                "error": str(e),
                "processing_time": time.time() - start_time
            }

    def analyze_with_direct_pdf(self, pdf_path: str, model: str = "claude-3-haiku-20240307") -> Dict:
        """Attempt to analyze PDF by sending file directly to LLM."""
        start_time = time.time()

        prompt = """You are analyzing a PDF document for intelligent processing.

Your task is to:
1. Identify distinct documents within this PDF
2. Detect duplicate pages or content
3. Find blank, illegible, or artifact pages
4. Recommend specific actions (keep/remove/split pages)
5. Suggest appropriate filenames for extracted documents
6. Provide confidence level (0-100%)

Format your response as structured JSON with the following schema:
{
  "analysis_confidence": <number>,
  "document_count": <number>,
  "total_pages": <number>,
  "recommended_actions": [
    {
      "action": "extract|remove|keep",
      "pages": [list of page numbers],
      "document_type": "description",
      "suggested_filename": "filename.pdf",
      "tags": ["tag1", "tag2"],
      "reasoning": "explanation"
    }
  ],
  "duplicates_detected": [
    {
      "pages": [page numbers],
      "similarity": "exact|high|partial",
      "reasoning": "explanation"
    }
  ]
}"""

        try:
            # Read PDF file
            with open(pdf_path, 'rb') as f:
                pdf_data = f.read()

            # Note: This approach may not work as Anthropic's API might not accept raw PDF
            # This is more of a test to see what happens
            response = self.client.messages.create(
                model=model,
                max_tokens=4000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            processing_time = time.time() - start_time

            return {
                "method": "direct_pdf",
                "model": model,
                "processing_time": processing_time,
                "response": response.content[0].text,
                "usage": response.usage._asdict() if hasattr(response, 'usage') else None
            }

        except Exception as e:
            return {
                "method": "direct_pdf",
                "model": model,
                "error": str(e),
                "processing_time": time.time() - start_time
            }

    def analyze_page_by_page(self, pdf_path: str, model: str = "claude-3-haiku-20240307") -> Dict:
        """Analyze each page separately, then aggregate results."""
        start_time = time.time()

        pages = self.extract_text_from_pdf(pdf_path)
        if not pages:
            return {"error": "Failed to extract text from PDF"}

        page_analyses = []

        for page in pages:
            page_prompt = f"""Analyze this single page from a PDF document.

Page {page['page_number']} content:
{page['text']}

Determine:
1. What type of document/content is this?
2. Is this a complete document or part of a multi-page document?
3. Does this appear to be a duplicate of something?
4. Is this page blank, illegible, or artifact?
5. What company/organization is this from?

Respond with a brief JSON analysis:
{{
  "page_number": {page['page_number']},
  "document_type": "description",
  "is_complete_document": true/false,
  "likely_duplicate": true/false,
  "quality": "good|poor|blank",
  "organization": "company name",
  "key_content": "brief summary"
}}"""

            try:
                response = self.client.messages.create(
                    model=model,
                    max_tokens=1000,
                    temperature=0.1,
                    messages=[{"role": "user", "content": page_prompt}]
                )

                page_analyses.append({
                    "page": page['page_number'],
                    "analysis": response.content[0].text
                })

            except Exception as e:
                page_analyses.append({
                    "page": page['page_number'],
                    "error": str(e)
                })

        # Now aggregate the results
        aggregate_prompt = f"""Based on the individual page analyses below, provide an overall document processing recommendation.

Page analyses:
{json.dumps(page_analyses, indent=2)}

Provide a comprehensive analysis in this JSON format:
{{
  "analysis_confidence": <number>,
  "document_count": <number>,
  "total_pages": {len(pages)},
  "recommended_actions": [
    {{
      "action": "extract|remove|keep",
      "pages": [list of page numbers],
      "document_type": "description",
      "suggested_filename": "filename.pdf",
      "tags": ["tag1", "tag2"],
      "reasoning": "explanation"
    }}
  ],
  "duplicates_detected": [
    {{
      "pages": [page numbers],
      "similarity": "exact|high|partial",
      "reasoning": "explanation"
    }}
  ]
}}"""

        try:
            final_response = self.client.messages.create(
                model=model,
                max_tokens=4000,
                temperature=0.1,
                messages=[{"role": "user", "content": aggregate_prompt}]
            )

            processing_time = time.time() - start_time

            return {
                "method": "page_by_page",
                "model": model,
                "processing_time": processing_time,
                "page_analyses": page_analyses,
                "final_analysis": final_response.content[0].text,
                "usage": final_response.usage._asdict() if hasattr(final_response, 'usage') else None
            }

        except Exception as e:
            return {
                "method": "page_by_page",
                "model": model,
                "error": str(e),
                "page_analyses": page_analyses,
                "processing_time": time.time() - start_time
            }


def main():
    """Run comprehensive testing of different analysis methods."""

    # Configuration
    pdf_path = "/Users/brianweaver/code/doc-manager/samples/09162025_RESPONSE REQUESTED BY September 16,2025.pdf"
    output_dir = Path("/Users/brianweaver/code/doc-manager/experiments")

    # Test models (start with Haiku, optionally test Sonnet)
    models_to_test = [
        "claude-3-haiku-20240307",
        # "claude-3-5-sonnet-20241022"  # Uncomment to test Sonnet
    ]

    results = {
        "test_metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "pdf_file": pdf_path,
            "models_tested": models_to_test
        },
        "test_results": []
    }

    print("Starting PDF Analysis API Testing...")
    print(f"Target file: {pdf_path}")

    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return

    try:
        analyzer = DocumentAnalyzer()

        for model in models_to_test:
            print(f"\\nTesting model: {model}")

            # Test 1: Text extraction method
            print("  Method 1: Text extraction...")
            result1 = analyzer.analyze_with_text_extraction(pdf_path, model)
            results["test_results"].append(result1)

            # Test 2: Direct PDF method (likely to fail, but worth testing)
            print("  Method 2: Direct PDF...")
            result2 = analyzer.analyze_with_direct_pdf(pdf_path, model)
            results["test_results"].append(result2)

            # Test 3: Page-by-page analysis
            print("  Method 3: Page-by-page analysis...")
            result3 = analyzer.analyze_page_by_page(pdf_path, model)
            results["test_results"].append(result3)

            print(f"  Completed testing {model}")

    except Exception as e:
        print(f"Error during testing: {e}")
        results["error"] = str(e)

    # Save results
    output_file = output_dir / "api_test_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\\nResults saved to: {output_file}")

    # Print summary
    print("\\n=== TEST SUMMARY ===")
    for result in results["test_results"]:
        if "error" in result:
            print(f"{result.get('model', 'unknown')} - {result.get('method', 'unknown')}: ERROR - {result['error']}")
        else:
            print(f"{result.get('model', 'unknown')} - {result.get('method', 'unknown')}: SUCCESS - {result.get('processing_time', 0):.2f}s")


if __name__ == "__main__":
    main()
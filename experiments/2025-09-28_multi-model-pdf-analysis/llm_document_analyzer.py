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
        self.prompt_dir = Path(__file__).parent / "prompts"

    def load_prompt(self, prompt_name: str) -> str:
        """Load a prompt template from the prompts directory."""
        prompt_file = self.prompt_dir / f"{prompt_name}.txt"
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

        return prompt_file.read_text().strip()

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

        prompt_template = self.load_prompt("text_extraction_analysis")
        prompt = prompt_template.format(text_content=text_content)

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
                "usage": {
                    "input_tokens": response.usage.input_tokens if hasattr(response, 'usage') else None,
                    "output_tokens": response.usage.output_tokens if hasattr(response, 'usage') else None
                } if hasattr(response, 'usage') else None
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

        prompt = self.load_prompt("direct_pdf_analysis")

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
                "usage": {
                    "input_tokens": response.usage.input_tokens if hasattr(response, 'usage') else None,
                    "output_tokens": response.usage.output_tokens if hasattr(response, 'usage') else None
                } if hasattr(response, 'usage') else None
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
            page_prompt_template = self.load_prompt("page_analysis")
            page_prompt = page_prompt_template.format(
                page_number=page['page_number'],
                page_text=page['text']
            )

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
        aggregate_prompt_template = self.load_prompt("aggregate_analysis")
        aggregate_prompt = aggregate_prompt_template.format(
            page_analyses=json.dumps(page_analyses, indent=2),
            total_pages=len(pages)
        )

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
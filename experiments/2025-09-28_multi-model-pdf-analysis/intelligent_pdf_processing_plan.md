# Experiment Plan: Multi-Model PDF Document Analysis for Paperless-NGX Integration

## Overview
This experiment tests the ability of different LLM models (Haiku, Sonnet) to intelligently analyze PDF documents and provide actionable instructions for document management. The goal is to develop a system that can serve as a webhook for paperless-ngx, providing automated document processing recommendations.

## Test Document
**File**: `samples/09162025_RESPONSE REQUESTED BY September 16,2025.pdf`
**Pages**: 7 total
**Expected Content Analysis** (Opus baseline):
- Pages 1-4: Duplicate HomeServe insurance marketing letters (2 copies of same 2-page letter)
- Page 5: Response form for HomeServe (should be kept with one copy of the letter)
- Page 6: Blank/artifact page (should be removed)
- Page 7: Unrelated medical billing statement (should be split to separate file)

## Phase 1: Model Comparison Testing

### Test 1: Haiku Subagent Analysis
**Objective**: Test Haiku's ability to analyze PDF structure without guidance

**Instructions for Haiku Subagent**:
1. Read the PDF file at `/Users/brianweaver/code/doc-manager/samples/09162025_RESPONSE REQUESTED BY September 16,2025.pdf`
2. Analyze the document structure and content across all pages
3. Identify distinct documents within the PDF
4. Detect duplicate content, blank pages, or unrelated documents
5. Recommend specific actions (keep/remove/split pages)
6. Provide reasoning for each recommendation
7. Report conclusions back with confidence levels

**Success Criteria**:
- Correctly identifies 2 distinct document types
- Detects duplicate pages (3-4 are copies of 1-2)
- Identifies blank/artifact page (6)
- Recognizes unrelated document (page 7)
- Provides clear, actionable recommendations

### Test 2: Programmatic API Testing
**Objective**: Test direct API integration and multiple input methods

**Implementation**: `experiments/llm_document_analyzer.py`

**Test Approaches**:
1. **Direct PDF submission** (if supported by Anthropic API)
2. **Text extraction + submission** (using PyPDF2 or similar)
3. **Page-by-page analysis** with aggregated reasoning

**Testing Sequence**:
1. **Haiku Testing**:
   - Test all input methods
   - Compare accuracy across methods
   - Measure processing time and token usage
   - Document response quality

2. **Sonnet Testing** (if Haiku results insufficient):
   - Same methodology as Haiku
   - Compare model performance
   - Document cost/quality tradeoffs

## Phase 2: Output Format Design

### Target JSON Schema for Paperless-NGX Integration
```json
{
  "analysis_confidence": 0.95,
  "document_count": 2,
  "recommended_actions": [
    {
      "action": "extract",
      "pages": [1, 2, 5],
      "document_type": "insurance_offer",
      "suggested_filename": "homeserve_water_line_protection_2025.pdf",
      "tags": ["insurance", "utilities", "water"],
      "reasoning": "Main insurance offer letter with response form"
    },
    {
      "action": "extract",
      "pages": [7],
      "document_type": "medical_bill",
      "suggested_filename": "syntero_medical_bill_2025.pdf",
      "tags": ["medical", "billing"],
      "reasoning": "Unrelated medical billing statement"
    },
    {
      "action": "remove",
      "pages": [3, 4, 6],
      "reasoning": "Duplicate content and blank pages"
    }
  ]
}
```

### Action Types
- **extract**: Create new document from specified pages
- **remove**: Delete specified pages (duplicates, blank pages)
- **keep**: Retain pages in original document
- **split**: Alternative to multiple extracts

## Phase 3: Webhook Service Architecture (Documentation Only)

### Future Integration Design
- **Endpoint**: `/analyze-document`
- **Input**: PDF file or paperless-ngx document ID
- **Processing**: LLM analysis using best-performing model
- **Output**: JSON instructions for paperless-ngx actions
- **Integration**: How paperless-ngx would consume and act on recommendations

### Workflow
1. Paperless-ngx receives document
2. Webhook calls document analyzer
3. LLM processes document and returns recommendations
4. Paperless-ngx executes recommended actions
5. User review for low-confidence cases

## Success Criteria

### Primary Requirements (This Experiment)
- [ ] Haiku subagent completes analysis independently
- [ ] Correct identification of document structure:
  - [ ] Two distinct document types identified
  - [ ] Duplicate pages detected (3-4 vs 1-2)
  - [ ] Blank/artifact page identified (6)
  - [ ] Unrelated document recognized (page 7)
- [ ] API integration successfully processes PDF
- [ ] Clear, actionable JSON output format generated
- [ ] Model performance comparison documented

### Validation Baseline
**Opus Analysis** (target accuracy):
- Pages 1-2: HomeServe letter (keep)
- Pages 3-4: Duplicate of 1-2 (remove)
- Page 5: Response form for HomeServe (keep with 1-2)
- Page 6: Blank/artifact (remove)
- Page 7: Medical bill (extract to separate document)

### Future Work (Documented but Not Implemented)
- [ ] Actual PDF splitting implementation using PyPDF2/pypdf
- [ ] Paperless-ngx webhook service deployment
- [ ] Batch processing capabilities
- [ ] Confidence thresholds for automated vs manual review
- [ ] Performance optimization and caching

## Technical Requirements

### Dependencies
```python
# Core dependencies
anthropic>=0.34.0
PyPDF2>=3.0.0  # or pypdf
requests>=2.31.0

# Optional for advanced processing
pdf2image>=1.16.0
Pillow>=10.0.0
```

### File Structure
```
experiments/
├── intelligent_pdf_processing_plan.md  # This file
├── llm_document_analyzer.py            # API testing script
├── haiku_analysis_results.json         # Subagent test results
├── model_comparison_report.md          # Performance analysis
└── paperless_integration_schema.json  # API specification
```

## Timeline
1. **Day 1**: Haiku subagent test + initial API script
2. **Day 2**: Complete API testing, model comparison
3. **Day 3**: Documentation, results analysis, next steps planning

## Expected Outcomes
1. **Model Performance Data**: Accuracy, speed, cost comparison
2. **Integration Specification**: Clear API design for paperless-ngx
3. **Processing Patterns**: Reusable logic for future document types
4. **Implementation Roadmap**: Next steps for production deployment

---

**Created**: 2025-09-28
**Branch**: feature/intelligent-pdf-processing
**Status**: Planning Complete - Ready for Implementation
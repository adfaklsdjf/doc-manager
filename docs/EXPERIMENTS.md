# Experiments Log

## Overview
This document tracks all experiments, prototypes, and learnings during development. Each experiment should document:
- **Goal**: What we're trying to learn
- **Approach**: How we tested it
- **Results**: What happened
- **Learnings**: What we learned
- **Decision**: What we'll do based on this

---

## Experiment Template

### Experiment #N: [Name]
**Date**: YYYY-MM-DD  
**Owner**: [User/Claude Code]  
**Status**: [Planned/In Progress/Complete]

**Goal**:
What question are we answering?

**Approach**:
- Step 1
- Step 2
- Step 3

**Results**:
```
Concrete data/output
```

**Learnings**:
- Learning 1
- Learning 2

**Decision**:
What we'll do differently based on this

**Files**:
- `experiments/relevant_script.py`

---

## Planned Experiments

### Experiment #1: Document Pattern Analysis
**Date**: TBD  
**Owner**: Claude Code  
**Status**: Planned

**Goal**:
Understand the types and patterns of documents in the existing archive to inform categorization rules.

**Approach**:
- Parse `etc-documents-20250921-1432.txt`
- Group files by apparent type
- Extract date patterns
- Identify naming conventions

---

### Experiment #2: OCR Quality Assessment
**Date**: TBD  
**Owner**: User  
**Status**: Planned

**Goal**:
Validate that ScanSnap OCR quality is sufficient for LLM processing.

**Approach**:
- Scan 5 different document types
- Extract text from PDFs
- Test readability with LLM
- Check for common OCR errors

---

### Experiment #3: paperless-ngx API Test
**Date**: TBD  
**Owner**: Claude Code  
**Status**: Planned

**Goal**:
Verify we can programmatically interact with paperless-ngx for document storage and retrieval.

**Approach**:
- Connect to API
- Upload test document
- Apply tags
- Search and retrieve

---

### Experiment #4: LLM Classification Accuracy
**Date**: TBD  
**Owner**: Claude Code  
**Status**: Planned

**Goal**:
Determine if LLM can accurately categorize documents and extract key information.

**Approach**:
- Create prompt template
- Test on 20 diverse documents
- Measure accuracy
- Iterate on prompt

---

## Completed Experiments

### Experiment #1: Paperless-NGX Initial Setup and API Connectivity
**Date**: 2025-09-22
**Owner**: Claude Code
**Status**: Complete

**Goal**:
Establish working connection to paperless-ngx instance and verify API functionality for future document processing.

**Approach**:
- Test MCP server connection to paperless-ngx
- Verify direct API access via curl
- Explore folder structure and existing documents
- Research OCR configuration options, particularly Tesseract neural networks

**Results**:
```
✅ MCP server connection: Working at 192.168.1.7:8000
✅ Direct API connection: Working with format "Authorization: Token ${PAPERLESS_API_KEY}"
✅ Fresh instance confirmed: 0 documents, tags, correspondents, document types
✅ Folder structure ready: /Volumes/etc/Documents/paperless/ with consume/ and media/ folders
✅ Source material available: ~1000 existing documents in parent Documents folder
```

**Learnings**:
- Initial IP address confusion (192.168.0.7 vs 192.168.1.7) required full client restart
- Curl token format is critical: `${PAPERLESS_API_KEY}` not `$PAPERLESS_API_KEY`
- MCP server provides cleaner interface than direct API calls for most operations
- Fresh paperless-ngx instances have no default configuration

**Decision**:
- Use MCP server for document management operations
- Reserve direct API calls for configuration that MCP doesn't support
- Proceed with OCR configuration research completed

**OCR Configuration Research Summary**:
Key environment variables for Tesseract neural networks:
- `PAPERLESS_OCR_LANGUAGE`: Language selection (default: "eng", supports "deu+eng" combinations)
- `PAPERLESS_OCR_MODE`: When to OCR ("skip", "redo", "force")
- `PAPERLESS_OCR_CLEAN`: Use unpaper preprocessing ("clean", "clean-final", "none")
- `PAPERLESS_OCR_LANGUAGES`: Install additional language packs
- `PAPERLESS_OCR_USER_ARGS`: Advanced OCRmyPDF arguments in JSON format

**Files**:
- Environment configured via `.envrc` and `.mcp.json`

---

## Lessons Learned

### Technical Insights
*To be populated*

### Process Insights
*To be populated*

### Tool Limitations
*To be populated*

---

## Failed Approaches

*Document what didn't work and why - failure is valuable data*

---

## Open Questions

1. Can we reliably extract dates from documents where the date isn't in the filename?
2. How do we handle multi-page documents that are actually multiple documents?
3. What's the minimum OCR quality needed for reliable LLM classification?
4. How do we handle documents in landscape orientation?
5. Can we detect and handle duplicate scans of the same document?

---

## Performance Benchmarks

*To be populated with timing data*

| Operation | Documents | Time | Rate |
|-----------|-----------|------|------|
| TBD | TBD | TBD | TBD |

---

## Code Snippets

### Useful Patterns Discovered

*To be populated with reusable code patterns we discover*

---

## Tool Configuration

### Optimal Settings Found

*To be populated with configuration settings that work well*

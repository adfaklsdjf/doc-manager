# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An intelligent document management system that automatically processes, categorizes, and organizes scanned documents using LLM-powered classification. The goal is to eliminate friction in dealing with physical mail and paperwork for someone with ADHD.

**Current Phase**: Discovery & Validation (Phase 0)

## Repository Structure

```
/
├── docs/                     # Comprehensive project documentation
│   ├── VISION.md            # Problem statement and long-term goals
│   ├── ARCHITECTURE.md      # System design and data flow
│   ├── ROADMAP.md           # Development phases and milestones
│   ├── REQUIREMENTS.md      # Functional requirements
│   ├── EXPERIMENTS.md       # Learning log and test results
│   └── IMPLEMENTATION_PLAN.md # Current task breakdown
├── experiments/              # Proof-of-concept code and prototypes
├── src/                      # Production code (currently empty)
├── tests/                    # Test suite (currently empty)
└── Documents/               # Sample document directory for testing
```

## Architecture Overview

**Document Flow**: ScanSnap ix1600 → Windows VM (OCR) → `/Documents/scanner/` → Python daemon → LLM classification → Organized storage + paperless-ngx

**Key Components**:
- **Intake Service**: Python daemon with file watcher
- **Classification**: Anthropic Claude API for document understanding
- **Storage**: File system organization + paperless-ngx for search
- **Processing**: Queue-based pipeline with error handling

## Development Commands

This is a Python project without formal build tools yet. Common development patterns:

```bash
# Development setup (when ready)
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Running experiments
cd experiments
python document_analysis.py
python paperless_test.py
python llm_classifier.py

# Testing (when implemented)
python -m pytest tests/
python -m pytest tests/test_specific.py::TestClass::test_method
```

## Key Design Principles

1. **Incremental by default** - Build features that don't break existing ones
2. **Log everything** - Enable debugging and iterative improvement
3. **Fail gracefully** - Defer/flag rather than miscategorize
4. **Real files, real problems** - Test against actual documents
5. **Human in the loop** - Start manual, gradually automate

## Technology Stack

- **Language**: Python 3.11+ (for ML ecosystem)
- **LLM**: Anthropic Claude API
- **Document Store**: paperless-ngx (running on Unraid)
- **File Processing**: PyPDF2, pdf2image, pytesseract (planned)
- **Infrastructure**: Docker containers on Unraid server
- **Database**: SQLite (MVP) → PostgreSQL (production)

## Current Focus Areas

**Week 1 Tasks** (per docs/IMPLEMENTATION_PLAN.md):
1. Document sample analysis - categorize existing 1000+ documents
2. ScanSnap output validation - test OCR quality
3. paperless-ngx API integration
4. LLM classification prototype (target >70% accuracy)

## Working with This Codebase

### Experimentation Workflow
- Create standalone scripts in `experiments/` directory
- Test against real files from Documents folder (use carefully - contains actual documents)
- Log all attempts and findings in `docs/EXPERIMENTS.md`
- Don't optimize prematurely - focus on learning

### Development Workflow
- Write small, focused functions with docstrings and type hints
- Create tests alongside production code in `src/`
- Update relevant documentation files
- Commit frequently with descriptive messages

### File Organization
- `experiments/` - Throwaway proof-of-concept code
- `src/` - Production-ready modules and services
- `tests/` - Comprehensive test suite
- Document processing results and learnings in `docs/EXPERIMENTS.md`

## Important Notes

- **Security**: All documents stay on local network, no cloud storage
- **Performance**: LLM API rate limits will constrain processing speed
- **Error Handling**: Better to defer than miscategorize - manual review queue essential
- **Testing**: Use real documents but be mindful of private content in logs
- **Target User**: ADHD-friendly workflows - minimize manual steps and decision fatigue

## Context Files

- `etc-documents-20250921-1432.txt` - Complete directory listing of Documents folder (~1000 files, 20k+ tokens - use sparingly)
- All `.md` files in `docs/` contain essential project context
- `principles.md` - Contains previous CLAUDE.md content (now superseded by this file)
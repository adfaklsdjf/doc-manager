# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A living document management system designed to automatically process, categorize, and organize scanned documents, with LLM-powered intelligence. The primary goal is to eliminate the friction of dealing with physical mail and paperwork through intelligent automation.

**Current Phase**: Experimentation, Discovery, Validation (Phase 0)
**Current Focus**: Getting documents scanned, characterized, and searchable.

## Core Design Principles
1. **Incremental by default** - Develop in small steps with limited failure modes and confirm as you go
2. **Log everything** - Enable replay, debugging, and iterative improvement
3. **Fail gracefully** - Better to defer/flag than miscategorize
4. **Real files, real problems** - Test against actual documents, not hypotheticals
5. **Human in the loop** - Start manual, gradually automate

## Technology Stack
- **Language**: Python 3.11+ (for ML ecosystem)
- **LLM Integration**: Anthropic API (initially)
- **Document Store**: paperless-ngx (running on Unraid)
- **File Processing**: PyPDF2, pdf2image, pytesseract (planned)
- **Infrastructure**: Docker containers on Unraid server
- **Infrastructure**: Unraid server (self-hosted)
- **Database**: SQLite (MVP) → PostgreSQL (production)

## Current State
- **Scanner**: Ricoh ScanSnap ix1600 → Windows VM → `/Documents/scanner/` folder
- **OCR**: Handled by ScanSnap software (produces searchable PDFs)
- **Storage**: ~1000 existing documents in `/Documents/` folder
- **Processing**: Manual (not happening - this is the problem we're solving)

## Current Focus Areas
**Week 1 Tasks** (per docs/IMPLEMENTATION_PLAN.md):
1. Analyze sample documents to understand patterns
2. Test OCR extraction quality
3. paperless-ngx API discovery
4. LLM document classification prototyping (target >70% accuracy)

## Critical Guidelines for Claude Code

### Experimentation Workflow
- Create standalone scripts in `experiments/` directory
- Test against real files from the Documents folder
- Log all attempts and findings in `docs/EXPERIMENTS.md`
- Don't optimize prematurely - focus on learning

### When Building Features
- Write small, focused functions
- Include docstrings and type hints
- Create tests alongside code
- Update relevant documentation
- Commit frequently with descriptive messages

### When You're Unsure
- Ask for clarification rather than assuming
- Propose alternatives with trade-offs
- Reference existing patterns in the codebase

## Architecture Overview

**Document Flow**: ScanSnap ix1600 → Windows VM (OCR) → `/Documents/scanner/` → Python daemon → LLM classification → Organized storage + paperless-ngx

**Planned Components**:
- **Intake Service**: Python daemon with file watcher
- **Classification**: Anthropic Claude API for document understanding
- **Storage**: File system organization + paperless-ngx for search
- **Processing**: Queue-based pipeline with error handling

## Repository Structure
```
/
├── CLAUDE.md                   # This file - essential context for Claude Code
├── README.md                   # Project overview
├── docs/                       # Comprehensive project documentation
│   ├── VISION.md               # Problem statement and long-term goals
│   ├── ARCHITECTURE.md         # System design and data flow
│   ├── ROADMAP.md              # Development phases and milestones
│   ├── REQUIREMENTS.md         # Functional requirements
│   ├── EXPERIMENTS.md          # Learning log and test results
│   └── IMPLEMENTATION_PLAN.md  # Current task breakdown
├── experiments/                # Proof-of-concept code and prototypes
├── src/                        # Production code (currently empty)
├── tests/                      # Test suite (currently empty)
└── Documents/                  # Sample files for testing - distinct from
    └── etc-documents-20250921-1432.txt               # Initial Documents folder file list (20k+ tokens, use sparingly)
```


## Important Notes

- **Security**: All documents stay on local network, no cloud storage
- **Performance**: Be mindful of LLM API rate limits
- **Error Handling**: Better to defer than miscategorize - manual review queue essential
- **Target User**: ADHD-friendly workflows - minimize manual steps and decision fatigue

- System must work incrementally - avoid big bang approaches
- Logging is critical for iterative improvement
- Start conservative, increase automation gradually


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

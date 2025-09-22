# Document Management System

An intelligent document management system designed to automatically process, categorize, and organize scanned documents using LLM-powered classification.

## Problem Statement

Managing physical mail and paper documents with ADHD creates overwhelming friction. Documents pile up unopened, important deadlines get missed, and finding anything becomes impossible. This system eliminates that friction by automating the entire document pipeline from scanning to organization.

## Current Status

🚧 **Phase 0: Foundation & Discovery** - Building initial prototypes and validating approach

## Key Features (Planned)

- ✅ **Zero-friction scanning** - Single button press to digitize
- 📋 **Automatic categorization** - LLM-powered document understanding
- 📋 **Smart naming** - Semantic filenames that make sense
- 📋 **Organized storage** - Logical folder structure maintained automatically
- 📋 **Full-text search** - Find anything instantly
- 📋 **Action extraction** - Know what needs attention

## Architecture

- **Scanner**: Ricoh ScanSnap ix1600
- **OCR**: ScanSnap software (via Windows VM)
- **Processing**: Python service with LLM integration
- **Storage**: paperless-ngx + organized file system
- **Intelligence**: Anthropic Claude API (initially)

## Documentation

- [`CLAUDE.md`](CLAUDE.md) - Quick context for Claude Code
- [`docs/VISION.md`](docs/VISION.md) - Problem and long-term goals
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) - System design
- [`docs/ROADMAP.md`](docs/ROADMAP.md) - Development phases
- [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md) - Detailed requirements
- [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) - Current tasks
- [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) - Learning log

## Quick Start

*Coming soon - MVP under development*

## Development

This project is being developed iteratively using Claude Code as a development partner. The focus is on incremental progress with continuous learning and refinement.

### Principles

1. **Incremental by default** - Small steps, continuous progress
2. **Real files, real problems** - Test against actual documents
3. **Fail gracefully** - Better to defer than miscategorize
4. **Log everything** - Enable learning and improvement

### Structure

```
/
├── docs/           # Project documentation
├── experiments/    # Prototypes and tests
├── src/           # Production code
└── tests/         # Test suite
```

## License

Private project - not for distribution


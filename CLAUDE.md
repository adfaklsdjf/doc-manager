# Document Management System - Claude Code Context

## What This Is
A living document management system designed to automatically process, categorize, and organize scanned documents. The primary goal is to eliminate the friction of dealing with physical mail and paperwork through intelligent automation.

**Current Focus**: Getting documents scanned, characterized, and searchable.

## Repository Structure
```
/
├── CLAUDE.md                 # This file - essential context for Claude Code
├── docs/                     # Project documentation
│   ├── VISION.md            # Problem statement and long-term goals
│   ├── ARCHITECTURE.md      # System design and components
│   ├── ROADMAP.md           # Phases and milestones
│   ├── REQUIREMENTS.md      # Functional and behavioral requirements
│   ├── EXPERIMENTS.md       # Log of what we've tried and learned
│   └── IMPLEMENTATION_PLAN.md # Current phase breakdown
├── experiments/              # Throwaway proof-of-concept code
├── src/                      # Production code (when ready)
└── tests/                    # Test suite
```

## Key Design Principles
1. **Incremental by default** - Every feature should be addable without breaking existing ones
2. **Log everything** - Enable replay, debugging, and iterative improvement  
3. **Fail gracefully** - Better to defer/flag than miscategorize
4. **Real files, real problems** - Test against actual documents, not hypotheticals
5. **Human in the loop** - Start manual, gradually automate

## Current State
- **Scanner**: Ricoh ScanSnap ix1600 → Windows VM → `/Documents/scanner/` folder
- **OCR**: Handled by ScanSnap software (produces searchable PDFs)
- **Storage**: ~1000 existing documents in `/Documents/` folder
- **Processing**: Manual (not happening - this is the problem we're solving)

## Technology Stack
- **Language**: Python (for ML ecosystem compatibility)
- **Document Store**: paperless-ngx (running on Unraid)
- **LLM Integration**: Anthropic API (initially)
- **Infrastructure**: Unraid server (self-hosted)

## Working Guidelines for Claude Code

### API and Command-Line Tools
- **curl and JSON**: Don't pipe curl to `jq` - Claude Code's tooling already formats JSON automatically, and piping introduces unnecessary complexity and potential failures
- Use simple, direct commands when possible

### When Experimenting
- **Read `docs/EXPERIMENTS.md` first** to understand existing experiments and organization
- Create dated subdirectories: `experiments/YYYY-MM-DD_brief-description/`
- Start with standalone scripts in the experiment subdirectory
- Test against real files from the Documents folder
- Log all attempts and outcomes to EXPERIMENTS.md
- Don't worry about perfection - we're learning

### When Building Features
- Write small, focused functions
- Include docstrings and type hints
- Create tests alongside code
- Update relevant documentation

### When You're Unsure
- Ask for clarification rather than assuming
- Propose alternatives with trade-offs
- Reference existing patterns in the codebase

### Defensive File Operations
- **ALWAYS run `pwd` before file operations** to confirm working directory
- Check file paths exist before attempting operations
- Use absolute paths when possible to avoid confusion

## Next Immediate Tasks
1. Analyze sample documents to understand patterns
2. Connect to paperless-ngx API
3. Build initial document classifier prototype
4. Test OCR extraction quality

## Important Context Files
- `etc-documents-20250921-1432.txt` - Full directory listing of Documents folder (20k+ tokens, use sparingly)

## Owner Notes
- User has ADHD - optimize for low-friction workflows
- System must work incrementally - avoid big bang approaches
- Logging is critical for iterative improvement
- Start conservative, increase automation gradually

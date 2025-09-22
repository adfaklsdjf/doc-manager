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

### Experiment #1: Entity Recognition Validation
**Date**: TBD  
**Owner**: Claude Code  
**Status**: Planned

**Goal**:
Test extraction of the top 10 entities from filenames and validate recognition accuracy.

**Approach**:
- Create regex patterns for: AEP, Columbia Gas, Wells Fargo, 1and1, Pantheon, Vanguard, OSU, Anthem, Progressive, E-Trade
- Test on 100 sample filenames
- Measure precision and recall
- Handle variations (e.g., "AEP" vs "AEPBill" vs "AEP Ohio")

**Test Cases**:
- `AEPBill_2022-11-11.pdf` → AEP
- `Columbia Gas - 2022-11.pdf` → Columbia Gas
- `Wells Fargo - 2021-01-03.pdf` → Wells Fargo
- `IN_202010120361.pdf` (1and1 invoice) → 1and1

---

### Experiment #2: Date Pattern Extraction
**Date**: TBD  
**Owner**: Claude Code  
**Status**: Planned

**Goal**:
Extract and normalize dates from various filename patterns to YYYY-MM-DD format.

**Approach**:
- Implement parsers for each pattern identified:
  - YYYY-MM-DD (keep as-is)
  - YYYYMMDD (add hyphens)
  - MM-DD-YYYY (reorder)
  - Month YYYY (parse month name)
- Test on real filenames from each pattern type
- Handle edge cases (invalid dates, ambiguous formats)

**Test Cases**:
- `03012025_DERIVATIVES AND INTEGRALS.pdf` → 2025-03-01
- `Columbia Gas 2020-04-22.pdf` → 2020-04-22
- `Wells Fargo - 2019-02-01.pdf` → 2019-02-01
- `statement-Apr-2022.pdf` → 2022-04-01

---

### Experiment #3: Scanner Output Classification
**Date**: TBD  
**Owner**: User + Claude Code  
**Status**: Planned

**Goal**:
Test LLM classification on actual ScanSnap outputs with problematic names.

**Approach**:
- User scans 5 documents with typical scanner names
- Extract text via OCR
- Send to LLM for classification
- Compare to known document type
- Iterate on prompt engineering

**Test Documents**:
1. Recent utility bill (should → Utilities)
2. Bank statement (should → Financial-Banking)
3. Medical EOB (should → Health-Medical)
4. Store receipt (should → Receipts-Purchases)
5. Tax form (should → Financial-Taxes)

---

### Experiment #4: Folder Structure Mapping
**Date**: TBD  
**Owner**: Claude Code  
**Status**: Planned

**Goal**:
Map existing folder structure to new categorization system.

**Approach**:
- Parse existing paths from document list
- Map current folders to new categories
- Identify conflicts and ambiguities
- Create migration rules

**Key Mappings**:
- `/Account Statements/AEP/` → Utilities
- `/Account Statements/Wells Fargo/` → Financial-Banking
- `/tax docus/` → Financial-Taxes
- `/work/Pantheon/` → Employment-Pantheon
- `/etc/` → Archive-Legacy (needs review)

---

### Experiment #5: High-Priority Document Detection
**Date**: TBD  
**Owner**: Claude Code  
**Status**: Planned

**Goal**:
Identify documents requiring immediate action based on content.

**Approach**:
- Define priority indicators:
  - "PAST DUE", "FINAL NOTICE"
  - "Response Required By"
  - "Tax Deadline"
  - Recent dates with "Bill" or "Invoice"
- Test on sample of recent documents
- Measure false positive/negative rates

---

## Completed Experiments

*None yet - this section will grow as we conduct experiments*

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

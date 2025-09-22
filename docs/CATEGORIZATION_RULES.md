# Document Categorization Rules

Based on analysis of 1000+ existing documents in the archive.

## Primary Categories (12)

1. **Financial-Banking** - Bank statements, account documents
2. **Financial-Investments** - Brokerage, 401k, cryptocurrency
3. **Financial-Taxes** - Tax returns, W2s, 1099s, supporting docs
4. **Utilities** - Electric (AEP), gas (Columbia), water, telecom
5. **Insurance** - Auto (Progressive), health (Anthem), home, life
6. **Real-Estate** - Property purchases, mortgages, property docs
7. **Employment** - Work documents organized by employer
8. **Health-Medical** - Medical records, therapy notes, prescriptions
9. **Receipts-Purchases** - Retail receipts, product manuals, warranties
10. **Legal-Government** - Court documents, licenses, official forms
11. **Personal-Projects** - Code, technical documentation, hobbies
12. **Archive-Legacy** - Old files, unclear purpose, needs review

## Naming Pattern Rules

### Target Format
`<Entity> - YYYY-MM-DD - <Description>.ext`

Examples:
- `AEP - 2024-03-15 - March Electric Bill.pdf`
- `Wells Fargo - 2024-03-01 - Mortgage Statement.pdf`
- `Anthem - 2024-02-28 - EOB Claim 12345.pdf`

### Date Extraction Patterns
1. `YYYY-MM-DD` (preferred, already used in ~30% of files)
2. `YYYYMMDD` (scanner default, needs reformatting)
3. `MM-DD-YYYY` or `MM.DD.YYYY` (American format)
4. `Month YYYY` (written out, needs parsing)
5. Document content extraction (when filename lacks date)

## Entity Recognition

### Top 10 Most Frequent Entities
1. **AEP** (American Electric Power) - 100+ files
2. **Columbia Gas** - 80+ files
3. **Wells Fargo** - 60+ files
4. **1and1** (hosting) - 50+ files
5. **Pantheon** (employer) - 30+ files
6. **Vanguard** - 15+ files
7. **OSU** (Ohio State University) - 20+ files
8. **Anthem** (health insurance) - 15+ files
9. **Progressive** (auto insurance) - 10+ files
10. **E-Trade** - 10+ files

## Classification Heuristics

### High Confidence Rules (>90% accuracy expected)

**Utilities**
- Contains: "AEP", "AEPBill", "AEPOhio" → Electric
- Contains: "Columbia Gas" → Gas
- Contains: "Cleveland Water" → Water

**Financial-Banking**
- Contains: "Wells Fargo" AND ("statement" OR "mortgage") → Banking
- Contains: "Fifth Third", "53", "Chase" → Banking

**Financial-Investments**
- Contains: "Vanguard", "401k", "retirement" → Investments
- Contains: "E-Trade", "Etrade", "brokerage" → Investments
- Contains: "Coinbase", "Bittrex", "crypto" → Investments

**Financial-Taxes**
- Contains: "W2", "W-2", "1099", "1098" → Taxes
- Contains: "tax", "IRS", "return" → Taxes
- Path contains: "/tax docus/" → Taxes

**Insurance**
- Contains: "Progressive" AND ("auto" OR "vehicle") → Insurance
- Contains: "Anthem", "Westfield", "insurance" → Insurance

**Employment**
- Path contains: "/work/HFC/" → Employment-HFC
- Path contains: "/work/OSU/" → Employment-OSU
- Path contains: "/work/Pantheon/" → Employment-Pantheon

### Medium Confidence Rules (70-90% accuracy)

**Health-Medical**
- Contains: "EOB", "claim", "medical" → Health-Medical
- Contains: "therapy", "prescription", "doctor" → Health-Medical
- Path contains: "/health/" → Health-Medical

**Receipts-Purchases**
- Contains: "receipt", "invoice", "order" → Receipts
- Contains: "manual", "warranty", "guide" → Receipts
- Path contains: "/product-manuals/" → Receipts

### Low Confidence / Fallback

**Personal-Projects**
- Extension: ".js", ".py", ".html", ".key" → Personal-Projects
- Contains technical terms without clear category → Personal-Projects

**Archive-Legacy**
- Modified date > 5 years old AND no clear category → Archive-Legacy
- Cryptic filename AND no entity match → Archive-Legacy
- Scanner default name without clear content → Archive-Legacy

## Special Handling

### Problem Patterns to Address

1. **Scanner Dumps**
   - Pattern: `MMDDYYYY_<garbled text>.pdf`
   - Action: Extract date, attempt OCR for content classification

2. **Duplicates**
   - Pattern: Same name with " 2", "(1)", "copy"
   - Action: Compare file hashes, consolidate if identical

3. **Multi-page Scans**
   - Pattern: Academic papers mixed with receipts
   - Action: Flag for potential document splitting

4. **Encrypted/Encoded**
   - Pattern: `.gpg`, `.base64` extensions
   - Action: Queue for manual review

## Processing Priority

### Priority 1 - Financial Critical
- Tax documents (especially during tax season)
- Current year financial statements
- Investment documents

### Priority 2 - Time-Sensitive
- Insurance documents
- Recent utility bills
- Employment records

### Priority 3 - Reference
- Product manuals
- Old receipts
- Historical statements (>1 year)

### Priority 4 - Archive
- Legacy files
- Personal projects
- Unclear purpose documents

## Success Metrics

- **Entity Recognition**: 95% accuracy on top 10 entities
- **Date Extraction**: 85% accuracy across all formats
- **Category Assignment**: 80% accuracy on high-confidence rules
- **Processing Speed**: <5 seconds per document average

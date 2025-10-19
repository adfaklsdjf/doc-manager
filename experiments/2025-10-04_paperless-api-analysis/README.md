# Paperless API Analysis Experiment

**Date:** 2025-10-04
**Goal:** Investigate discrepancies in paperless document type reporting and analyze raw API data

## Background

Initial API query showed many documents categorized as "Unknown (ID: X)" types, but the paperless UI shows all documents have assigned document types. This experiment aims to understand this discrepancy by capturing and analyzing raw API request/response data.

## Current Findings

### Initial API Query Results (2025-10-04)

```
Total Documents: 142
Total Document Types: 25

Top Categories:
- Unknown (ID: 17): 36 documents (25.4%)
- Bill: 13 documents (9.2%)
- Account Statement: 9 documents (6.3%)
- Unknown (ID: 56): 6 documents (4.2%)
```

### Discrepancy Identified

- **API Response**: Shows many "Unknown (ID: X)" document types
- **UI Display**: All documents appear to have proper document type assignments
- **Question**: Are document type names not being resolved properly, or is there a data consistency issue?

## Investigation Approach

### Enhanced API Tool

Created `paperless_api.py` with raw data capture capabilities:

**Features:**
- Saves all HTTP requests to `raw_data/` folder
- Timestamps: `YYYYMMDD_HHMMSS_mmm` format for chronological sorting
- File naming: `{timestamp}_{method}_{endpoint}_{request|response}.json`
- Captures headers, parameters, and full response content

**Example Files:**
```
raw_data/
├── 20251004_143022_456_get_document_types_request.json
├── 20251004_143022_456_get_document_types_response.json
├── 20251004_143023_123_get_documents_request.json
└── 20251004_143023_123_get_documents_response.json
```

### Data Capture Strategy

1. **Document Types API** - Capture full document type definitions
2. **Documents API** - Capture document metadata with type associations
3. **Cross-reference** - Match document type IDs to names manually
4. **Identify** - Root cause of "Unknown" categorizations

## Technical Implementation

### Raw Data Structure

**Request Files:**
```json
{
  "timestamp": "20251004_143022_456",
  "method": "GET",
  "url": "http://192.168.1.7:8000/api/document_types/",
  "headers": {"Authorization": "Token ...", ...},
  "params": {...},
  "data": {...}
}
```

**Response Files:**
```json
{
  "timestamp": "20251004_143022_456",
  "status_code": 200,
  "headers": {"Content-Type": "application/json", ...},
  "url": "http://192.168.1.7:8000/api/document_types/",
  "content": "{\"count\": 25, \"results\": [...]}"
}
```

## Questions to Answer

1. **Document Type Resolution**: Why are document type names showing as "Unknown (ID: X)"?
2. **Data Consistency**: Is there a mismatch between the API and UI data sources?
3. **ID Mapping**: Are document type IDs being properly resolved to names?
4. **Database Issues**: Could there be orphaned document type references?

## Expected Outcomes

1. **Root Cause Identification**: Understand why document types appear as "Unknown"
2. **Data Quality Assessment**: Determine actual document categorization state
3. **API Behavior Documentation**: Document how paperless API handles document types
4. **Classification Opportunities**: Identify documents that truly need better categorization

## Files Generated

- `paperless_api.py` - Enhanced API client with raw data capture
- `raw_data/` - Directory containing all HTTP request/response pairs
- `README.md` - This documentation

## Next Steps

1. **Run Enhanced Tool** - Execute with raw data capture enabled
2. **Analyze Raw Data** - Examine actual API responses for type information
3. **Cross-Reference** - Map document type IDs to names manually
4. **Document Findings** - Update this README with discoveries
5. **Propose Solutions** - Recommend fixes for any issues found

## Usage

```bash
cd experiments/2025-10-04_paperless-api-analysis
python paperless_api.py
```

Raw request/response data will be saved to `raw_data/` for detailed analysis.
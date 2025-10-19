# Paperless MCP and API Testing Session

**Date:** 2025-10-18
**Goal:** Understand paperless-mcp capabilities and Paperless-ngx API for managing document notes

## Context

Working on a document management workflow where we need to:
1. Evaluate OCR quality of existing documents
2. Move original (potentially poor quality) text content to notes
3. Re-OCR documents with GPT-4o-mini for better quality
4. Preserve original text for forensics/comparison

## Key Findings

### Paperless-ngx MCP Server Capabilities

**Document Filtering:**
- The `list_documents` tool supports filtering by:
  - `tag` (single tag ID)
  - `correspondent` (single ID)
  - `document_type` (single ID)
  - `storage_path` (single ID)
  - `created__date__gte` and `created__date__lte` (date ranges)
  - `search` (free-text content search)
  - `ordering` (sort order)
  - `page` and `page_size` (pagination)

**Limitations:**
- No support for complex queries (e.g., "NOT tagged with X", "tagged with Y OR Z")
- No support for custom field filtering
- No access to saved Paperless "views"
- **No support for managing notes** (read-only via `get_document`)

**Implication:** For complex document queries (like "documents without any year tag"), we'll need to:
1. Fetch larger document sets via the MCP tools
2. Filter client-side in Python scripts or subagents
3. Consider creating reusable scripts for common patterns rather than specialized subagents

### Notes Management via Paperless API

**Discovery:** Notes are NOT managed through the MCP server, but the Paperless API supports them directly.

**API Endpoints:**
- **GET** `/api/documents/{id}/notes/` - List all notes for a document
- **POST** `/api/documents/{id}/notes/` - Create a new note
  - Request body: `{"note": "text content here"}`
  - Returns: Array with newly created note object including `id`, `created`, `user`
- **DELETE** `/api/documents/{id}/notes/?id={note_id}` - Delete a specific note

**Note Structure:**
```json
{
  "id": 11,
  "note": "Text content of the note",
  "created": "2025-10-18T12:03:27.688792-04:00",
  "user": {
    "id": 3,
    "username": "amygdala",
    "first_name": "Amy",
    "last_name": "Dala"
  }
}
```

**How notes appear in document responses:**
- When fetching a document via `GET /api/documents/{id}/` or the MCP `get_document` tool
- Notes are embedded as an array: `"notes": [...]`
- Not referenced by ID - full note objects included inline

### Curl and JSON Formatting Observations

**Issue discovered:** When Claude Code runs curl commands, there's tooling that intercepts and formats JSON output automatically.

**Evidence:**
1. Curl showed "progress" output without `-s` flag even when not piped
2. JSON was nicely formatted without using `jq`
3. Piping to `jq` introduced unnecessary complexity and potential failure points

**Recommendation:** Don't pipe curl to `jq` when working with Claude Code - the JSON is already parsed/formatted by underlying tooling, and LLMs don't need whitespace formatting for readability.

## Testing Performed

### Environment Setup
- Verified `PAPERLESS_URL=http://192.168.1.7:8000`
- Verified `PAPERLESS_API_KEY` is set (token authentication working)

### API Tests
1. **Basic connectivity:** `curl -v "$PAPERLESS_URL"` → 302 redirect (expected)
2. **Unauthenticated access:** `curl http://192.168.1.7:8000/api/documents/562/` → 401 (expected)
3. **Authenticated document fetch:** Successfully retrieved document 562 with embedded notes
4. **Note creation:** Successfully created test note (ID 12) on document 563

### Document Analysis
- Examined document 562 (Breezeline bill) - digitally composed PDF
- Text extraction has issues:
  - Interleaved columns (left/right content mixed line-by-line)
  - Barcode/POSTNET encoding artifacts (DFTAD character sequences)
  - Semantically useless despite being technically accurate
- This validates the need for GPT-4o-mini re-OCR workflow

## Next Steps

### Immediate TODO
1. Create workflow to move document content → note and clear content field
2. Test re-OCR with GPT-4o-mini and compare quality
3. Consider extending paperless-mcp to support notes management

### For MCP Enhancement
The paperless-mcp server could be extended to support notes:
- Add `create_note` tool: POST to `/api/documents/{id}/notes/`
- Add `delete_note` tool: DELETE to `/api/documents/{id}/notes/?id={note_id}`
- Add `list_notes` tool: GET `/api/documents/{id}/notes/` (though notes are already in document response)

**Code locations in paperless-mcp repo:**
- Tool definitions: `src/tools/documents.ts` (lines 304-369 for `update_document`)
- API client: `src/api/PaperlessAPI.ts` (line 151 for `updateDocument`)
- Type definitions: `src/api/types.ts` (lines 72-77 for `Note` interface, line 100 for `notes` in `Document`)
- OpenAPI spec: `Paperless_ngx_REST_API.yaml` (lines 1618-1675 for notes endpoint, line 6618 for request schema)

## References
- Paperless-ngx API documentation (via OpenAPI spec in repo)
- paperless-mcp GitHub: https://github.com/jbouder/paperless-mcp (forked locally)

# Paperless-ngx Webhook Service Experiment

**Date:** 2025-09-28
**Goal:** Create a webhook service to receive and analyze paperless-ngx workflow webhook actions

## Summary

Built a Flask-based webhook service to capture and analyze paperless-ngx workflow webhook actions. Discovered that paperless workflows can send files but have limited metadata capabilities.

## What We Built

### Webhook Service Features

- **Multiple Endpoints**: Dedicated endpoints for each paperless workflow trigger type
- **Request Logging**: Comprehensive logging with headers, body, and metadata
- **File Saving**: Raw HTTP requests saved to `.http` files for analysis
- **Multipart Parsing**: Extracts files and form data from multipart requests
- **Analysis Tools**: Script to parse saved requests and extract PDF files

### Service Endpoints

```
GET  /                     - Service info and endpoint list
POST /webhook              - General webhook (backward compatibility)
POST /consumption-started  - "Consumption Started" trigger webhooks
POST /document-added       - "Document Added" trigger webhooks
POST /document-updated     - "Document Updated" trigger webhooks
POST /scheduled           - "Scheduled" trigger webhooks
GET  /health              - Health check
```

**Access:** Service runs on `http://192.168.1.96:5000` (accessible from Unraid server)

## Key Findings

### Paperless-ngx Webhook Limitations

1. **No Native Webhooks**: Paperless-ngx doesn't have built-in webhook functionality yet
2. **Workflow Actions Only**: Webhooks are implemented as "actions" within workflows
3. **Limited Metadata**: Workflow webhooks don't include document metadata (ID, tags, etc.)
4. **File-Only Payload**: "Document Added" triggers send only the PDF file, no metadata
5. **PosixPath Bug**: "Consumption Started" triggers fail when including documents

### Paperless Workflow Configuration

**Current Setup:**
- **Consumption Started**: Triggers on document consumption, no file (due to bug)
- **Document Added**: Triggers when document is fully processed, includes PDF file

**Available Triggers:**
- Consumption Started
- Document Added
- Document Updated
- Scheduled

**Webhook Action Options:**
- URL configuration
- Toggle: Use parameters for webhook body
- Toggle: Send webhook payload as JSON
- Workflow params: Key-value pairs (appear to be static text)
- Webhook headers: Key-value pairs (appear to be static text)
- Toggle: Include document

## Technical Details

### File Structure

```
/experiments/2025-09-28_paperless-webhook-service/
├── webhook_service.py          # Main Flask service
├── analyze_request.py          # Request analysis utility
├── requirements.txt            # Python dependencies
├── .gitignore                 # Excludes .http files and logs
├── saved_requests/            # Raw HTTP request files (.http)
├── venv/                      # Python virtual environment
└── webhook_requests.log       # Service logs
```

### Request Analysis

**Example Document Added Webhook:**
```
POST /webhook HTTP/1.1
Content-Type: multipart/form-data; boundary=...
Content-Length: 324713

--boundary
Content-Disposition: form-data; name="file"; filename="07072025_WESTFIELD.pdf"
Content-Type: application/pdf

[PDF binary data...]
```

**Captured Data:**
- Form fields: 0
- Files: 1 (PDF, 324KB, 2 pages)
- No document metadata (ID, tags, correspondent, etc.)

## Analysis Tools

### analyze_request.py

Utility to parse saved webhook requests:

```bash
python analyze_request.py <request_file>
```

**Features:**
- Parses HTTP headers and multipart body
- Extracts file metadata (name, size, content-type)
- Automatically saves PDF files as `extracted_*.pdf`
- Lists all form fields and files

### Example Usage

```bash
# List available request files
python analyze_request.py

# Analyze specific request
python analyze_request.py consumption-started_2025-09-28T18-40-11_239255.http
```

## Workflow Integration Approaches

Since paperless webhooks have limited metadata, consider these approaches:

### 1. API Polling
- React to webhook as "something happened" signal
- Use paperless REST API to fetch document details
- More reliable than depending on webhook metadata

### 2. Custom Post-Consumption Script
- Hook into paperless consumption pipeline
- Access to full document context
- Can send custom webhook with complete metadata

### 3. Workflow Parameters
- Test adding static key-value pairs in workflow config
- May provide way to pass custom metadata
- Appears to be static text only (no variables)

### 4. Wait for Native Webhooks
- Community actively requesting this feature
- Future paperless versions may include proper webhook events
- Would include document ID, metadata, etc.

## Next Steps

1. **Test Workflow Parameters**: Add key-value pairs to see if any metadata can be passed
2. **API Integration**: Build service to poll paperless API when webhook received
3. **Document Update Testing**: Trigger document updates to test that workflow type
4. **Custom Script Exploration**: Investigate post-consumption script alternatives

## Configuration Notes

**Network Access:**
- Service binds to `0.0.0.0:5000`
- Accessible from localhost: `http://127.0.0.1:5000`
- Accessible from network: `http://192.168.1.96:5000`
- Paperless server (Unraid): `192.168.1.7`

**Security Considerations:**
- Raw request files may contain sensitive documents
- `.http` files excluded from git via `.gitignore`
- Service intended for development/testing only

## Known Issues

1. **PosixPath Error**: "Consumption Started" triggers fail when including documents
   ```
   [ERROR] Failed attempt sending webhook: expected string or bytes-like object, got 'PosixPath'
   ```

2. **No Document Metadata**: Workflows don't provide document IDs, tags, or other metadata

3. **Static Parameters**: Workflow parameters appear to be static text only, no variable substitution

## Files and Logs

- **Service Logs**: `webhook_requests.log` (comprehensive request logging)
- **Raw Requests**: `saved_requests/*.http` (complete HTTP requests with binary data)
- **Extracted Files**: `extracted_*.pdf` (PDFs extracted from multipart requests)
- **Git Exclusions**: Large binary files excluded via `.gitignore`

## Conclusion

Successfully built a comprehensive webhook analysis system that revealed the current limitations of paperless-ngx webhook functionality. While workflows can trigger webhooks, they lack the metadata richness needed for advanced document processing. The service provides a solid foundation for testing future paperless webhook improvements or building API-based alternatives.
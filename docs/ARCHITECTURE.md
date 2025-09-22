# System Architecture

## High-Level Architecture

```
┌─────────────────┐
│   Paper Input   │
└────────┬────────┘
         │
         ▼
┌──────────────────┐       ┌───────────────┐
│  ScanSnap ix1600 ├───────►  Windows VM   │
└──────────────────┘       │  (OCR Engine) │
                           └──────┬────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │ /Documents/scanner/    │
                     │   (Network Share)      │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │   Intake Service       │
                     │   (Python Daemon)      │
                     └────────────┬───────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 ▼                ▼                ▼
         ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
         │ Classifier   │ │   Extractor  │ │ Deduplicator │
         │ (LLM-based)  │ │ (LLM-based)  │ │ (Hash+Fuzzy) │
         └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
                └────────────────┼────────────────┘
                                 ▼
                     ┌────────────────────────┐
                     │   Document Router      │
                     └────────────┬───────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 ▼                ▼                ▼
         ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
         │ File System  │ │paperless-ngx │ │ Notification │
         │ (Organized)  │ │   (Search)   │ │   Service    │
         └──────────────┘ └──────────────┘ └──────────────┘
```

## Component Details

### Scanner Layer
**Purpose**: Physical to digital conversion
- **ScanSnap ix1600**: Hardware scanner with WiFi
- **Windows VM**: Runs ScanSnap software for OCR
- **Output**: Searchable PDFs in network share

### Intake Service
**Purpose**: Monitor and process new documents
- **Technology**: Python daemon with file system watcher
- **Responsibilities**:
  - Detect new files in scanner folder
  - Queue for processing
  - Manage processing pipeline
  - Handle errors gracefully

### Classification Engine
**Purpose**: Understand document type and content
- **Technology**: Anthropic Claude API (initially)
- **Categories** (tentative):
  - Utilities (gas, electric, water, internet)
  - Financial (bank statements, credit cards)
  - Insurance (health, auto, home)
  - Medical (test results, bills, records)
  - Government (taxes, notices, licenses)
  - Receipts (purchases, services)
  - Legal (contracts, agreements)
  - Correspondence (letters, notices)
  - Other (uncategorized)

### Information Extractor
**Purpose**: Pull structured data from documents
- **Extracted Fields**:
  - Document date
  - Parties involved
  - Amounts (if applicable)
  - Account numbers (masked)
  - Due dates
  - Key terms

### Document Router
**Purpose**: Send processed documents to appropriate destinations
- **File System**: Organized folder structure
- **paperless-ngx**: Full-text search and tagging
- **Notification Queue**: Alerts and summaries

### Storage Layer

#### File System Structure
```
/Documents/
├── Archive/
│   └── YYYY/
│       └── MM/
│           └── [Categorized documents]
├── Pending/
│   └── [Documents requiring action]
├── Reference/
│   └── [Long-term documents]
└── scanner/
    └── [Intake folder]
```

#### paperless-ngx
- Full-text search
- Tag management
- Document versioning
- Web interface

## Data Flow

### Standard Document Flow
1. Paper placed on scanner
2. Button pressed → PDF created
3. File appears in `/Documents/scanner/`
4. Intake service detects new file
5. LLM classifies document type
6. LLM extracts key information
7. Document renamed and moved to organized location
8. Metadata stored in database
9. Document indexed in paperless-ngx
10. Notification sent (if configured)

### Error Handling Flow
1. Processing failure detected
2. Document moved to `/Documents/Pending/`
3. Error logged with details
4. Retry scheduled (with backoff)
5. Manual review triggered after N failures

## Integration Points

### APIs
- **Anthropic Claude**: Document understanding
- **paperless-ngx REST API**: Document management
- **Telegram Bot API**: Notifications (future)
- **Email SMTP**: Digest notifications

### File System
- **Input**: `/Documents/scanner/`
- **Output**: `/Documents/Archive/`
- **Errors**: `/Documents/Pending/`

### Database Schema (Proposed)
```sql
-- Documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    original_filename TEXT,
    final_filename TEXT,
    file_hash TEXT,
    category TEXT,
    document_date DATE,
    processed_date TIMESTAMP,
    status TEXT,
    metadata JSONB
);

-- Processing log
CREATE TABLE processing_log (
    id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(id),
    timestamp TIMESTAMP,
    action TEXT,
    result TEXT,
    details JSONB
);
```

## Security Considerations

### Data Protection
- All documents remain on local network
- No cloud storage of documents
- LLMs see content but don't store it
- Sensitive data masked in logs

### Access Control
- Scanner VM isolated to network share
- Services run with minimal permissions
- Web interfaces behind authentication

## Scalability Considerations

### Current Limitations
- Single scanner input
- Serial document processing
- LLM API rate limits

### Future Scaling
- Queue-based processing for parallelization
- Multiple LLM providers for redundancy
- Caching for duplicate detection
- Batch processing for historical documents

## Technology Stack

### Core
- **Language**: Python 3.11+
- **Framework**: FastAPI (for web services)
- **Queue**: Python Queue (initially), Redis (future)
- **Database**: SQLite (MVP), PostgreSQL (production)

### Libraries
- **Document Processing**: PyPDF2, pdf2image, pytesseract
- **LLM Integration**: anthropic-sdk, langchain
- **File Watching**: watchdog
- **Notifications**: smtp, telegram-bot

### Infrastructure
- **Host OS**: Unraid
- **Containerization**: Docker
- **Document Store**: paperless-ngx
- **File Storage**: Network shares

## Deployment Strategy

### MVP Deployment
- Single Python service on Unraid
- SQLite database
- Local file system
- Manual monitoring

### Production Deployment
- Docker containers
- PostgreSQL database
- Health checks and auto-restart
- Prometheus metrics
- Grafana dashboards

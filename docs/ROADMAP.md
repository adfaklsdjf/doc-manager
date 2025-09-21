# Development Roadmap

## Phase 0: Foundation & Discovery (Current)
**Goal**: Understand the problem space and validate approach

### Completed ✅
- Scanner hardware setup (ScanSnap ix1600)
- Windows VM for OCR processing
- Basic workflow: Scan → OCR → `/Documents/scanner/`
- paperless-ngx deployed on Unraid

### In Progress 🔄
- Document analysis and categorization patterns
- paperless-ngx API exploration
- Initial experiments with document classification

### Upcoming 📋
- OCR quality assessment
- LLM prompt engineering for document understanding
- Prototype document naming algorithm

## Phase 1: MVP - Basic Intelligence
**Goal**: Documents automatically organized and findable
**Success Metric**: 80% of scanned documents correctly named and filed

### Core Features
- [ ] Document intake watcher service
- [ ] Automatic categorization (10-15 main categories)
- [ ] Semantic naming (`<Party> - YYYY-MM-DD - <Description>`)
- [ ] Organized folder structure
- [ ] Basic duplicate detection
- [ ] Ingestion into paperless-ngx

### Technical Components
- Python service running on Unraid
- Anthropic API for classification
- File system operations
- paperless-ngx API integration
- Comprehensive logging

## Phase 2: Version 1.0 - Active Intelligence
**Goal**: System provides actionable insights
**Success Metric**: Never miss a bill or important deadline

### New Capabilities
- [ ] Information extraction (amounts, dates, account numbers)
- [ ] Daily/weekly digest notifications
- [ ] Action detection ("Response Required", "Payment Due")
- [ ] Chronological timeline interface
- [ ] Batch reprocessing of historical documents

### Infrastructure
- Notification system (email/Telegram)
- Database for metadata
- Web UI for document review
- Backup and recovery procedures

## Phase 3: Automation & Learning
**Goal**: System takes approved actions autonomously

### Features
- [ ] Bill payment tracking
- [ ] Autopay detection and monitoring
- [ ] Duplicate consolidation with source tracking
- [ ] Custom extraction rules per document type
- [ ] Anomaly detection (unusual charges, usage spikes)

## Phase 4: Advanced Intelligence
**Goal**: Comprehensive document assistant

### Capabilities
- [ ] Natural language queries ("Show me all insurance documents from 2023")
- [ ] Tax preparation assistance
- [ ] Contract term extraction and reminders
- [ ] Integration with calendar for document-driven events
- [ ] Multi-model approach (local for sensitive, cloud for complex)

## Phase 5: Ecosystem Integration
**Goal**: Part of broader personal AI infrastructure

### Integration Points
- [ ] Personal AI assistant can access document knowledge
- [ ] Voice queries about documents
- [ ] Automated correspondence drafting
- [ ] Financial analytics across all documents
- [ ] Predictive filing based on patterns

## Ideas Parking Lot 🚗
*Captured for future consideration, not committed*

- Handwriting recognition for notes/forms
- Receipt processing with expense categorization  
- Medical record organization with appointment tracking
- Legal document analysis with key date extraction
- Warranty tracking with expiration alerts
- Travel document management
- Educational transcript organization
- Contract comparison tools
- Insurance claim automation
- Mobile app for remote document access
- Family member access with permissions
- Document retention policies
- GDPR/privacy compliance tools

## Decision Log

### Decided ✅
- Python as primary language (ML ecosystem)
- Start with Anthropic API (best quality now, migrate later)
- paperless-ngx as document store
- Incremental development approach

### Under Consideration 🤔
- Database choice for metadata
- Web framework for UI
- Notification prioritization logic
- Batch vs stream processing

### Rejected ❌
- Node.js for backend (Python better for ML)
- Immediate local LLM usage (quality gap too large)
- Manual review for every document (defeats purpose)

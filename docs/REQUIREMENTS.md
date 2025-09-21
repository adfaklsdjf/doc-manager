# Requirements Specification

## Functional Requirements

### Core Document Processing

#### FR-1: Document Intake
- **FR-1.1**: System SHALL monitor `/Documents/scanner/` for new files
- **FR-1.2**: System SHALL process PDF, PNG, and JPG formats
- **FR-1.3**: System SHALL handle multiple documents in parallel
- **FR-1.4**: System SHALL preserve original files during processing

#### FR-2: Document Classification
- **FR-2.1**: System SHALL categorize documents into predefined types
- **FR-2.2**: System SHALL handle ambiguous documents with "Unknown" category
- **FR-2.3**: System SHALL support minimum 15 document categories
- **FR-2.4**: System SHALL provide confidence scores for classifications

#### FR-3: Information Extraction
- **FR-3.1**: System SHALL extract document date (if present)
- **FR-3.2**: System SHALL identify parties/companies involved
- **FR-3.3**: System SHALL extract monetary amounts (if applicable)
- **FR-3.4**: System SHALL identify action items (payment due, response required)

#### FR-4: Document Naming
- **FR-4.1**: System SHALL rename documents following pattern: `<Party> - YYYY-MM-DD - <Description>`
- **FR-4.2**: System SHALL handle conflicts with incremental numbering
- **FR-4.3**: System SHALL sanitize filenames for filesystem compatibility
- **FR-4.4**: System SHALL preserve file extensions

#### FR-5: Document Organization
- **FR-5.1**: System SHALL move documents to category-based folders
- **FR-5.2**: System SHALL maintain chronological structure (YYYY/MM)
- **FR-5.3**: System SHALL separate pending from processed documents
- **FR-5.4**: System SHALL create folders as needed

### Search and Retrieval

#### FR-6: Document Search
- **FR-6.1**: System SHALL provide full-text search capability
- **FR-6.2**: System SHALL search by date range
- **FR-6.3**: System SHALL search by category
- **FR-6.4**: System SHALL search by extracted metadata

#### FR-7: paperless-ngx Integration
- **FR-7.1**: System SHALL ingest documents into paperless-ngx
- **FR-7.2**: System SHALL sync tags with categories
- **FR-7.3**: System SHALL maintain bidirectional references
- **FR-7.4**: System SHALL handle paperless-ngx unavailability gracefully

### Monitoring and Notification

#### FR-8: Processing Logs
- **FR-8.1**: System SHALL log all processing attempts
- **FR-8.2**: System SHALL record success/failure status
- **FR-8.3**: System SHALL capture processing duration
- **FR-8.4**: System SHALL maintain audit trail

#### FR-9: Notifications (Post-MVP)
- **FR-9.1**: System SHALL send daily processing summaries
- **FR-9.2**: System SHALL alert on processing failures
- **FR-9.3**: System SHALL notify of high-priority documents
- **FR-9.4**: System SHALL support email and Telegram

## Non-Functional Requirements

### Performance

#### NFR-1: Processing Speed
- **NFR-1.1**: System SHALL process standard document in <30 seconds
- **NFR-1.2**: System SHALL handle queue of 50 documents without degradation
- **NFR-1.3**: System SHALL support batch reprocessing at 100+ docs/hour

### Reliability

#### NFR-2: Availability
- **NFR-2.1**: System SHALL auto-restart after failures
- **NFR-2.2**: System SHALL preserve queue during restarts
- **NFR-2.3**: System SHALL not lose documents during crashes

#### NFR-3: Error Handling
- **NFR-3.1**: System SHALL retry failed operations with exponential backoff
- **NFR-3.2**: System SHALL quarantine problematic documents
- **NFR-3.3**: System SHALL continue processing despite individual failures

### Scalability

#### NFR-4: Growth
- **NFR-4.1**: System SHALL handle 10,000+ documents in archive
- **NFR-4.2**: System SHALL support adding new document categories
- **NFR-4.3**: System SHALL allow new extraction rules without code changes

### Security

#### NFR-5: Data Protection
- **NFR-5.1**: System SHALL NOT store documents in cloud
- **NFR-5.2**: System SHALL mask sensitive data in logs
- **NFR-5.3**: System SHALL use secure API connections
- **NFR-5.4**: System SHALL respect file permissions

### Maintainability

#### NFR-6: Code Quality
- **NFR-6.1**: System SHALL have >80% test coverage
- **NFR-6.2**: System SHALL follow Python PEP-8 standards
- **NFR-6.3**: System SHALL include comprehensive logging
- **NFR-6.4**: System SHALL use type hints throughout

## Behavioral Requirements (ADHD-Optimized)

### BR-1: Minimal Friction
- **BR-1.1**: Document scanning SHALL require single button press
- **BR-1.2**: System SHALL NOT require manual categorization
- **BR-1.3**: System SHALL NOT block on user input
- **BR-1.4**: Default actions SHALL be safe (defer vs. miscategorize)

### BR-2: Fault Tolerance
- **BR-2.1**: System SHALL handle papers in any orientation
- **BR-2.2**: System SHALL process crumpled/folded documents
- **BR-2.3**: System SHALL handle multiple documents in single scan
- **BR-2.4**: System SHALL accept documents 24/7 without preparation

### BR-3: Feedback
- **BR-3.1**: System SHALL provide visual confirmation of processing
- **BR-3.2**: System SHALL NOT require monitoring during operation
- **BR-3.3**: Errors SHALL be actionable, not just informative
- **BR-3.4**: Success SHALL be assumed unless notified otherwise

### BR-4: Recovery
- **BR-4.1**: System SHALL allow reprocessing of any document
- **BR-4.2**: Original files SHALL always be recoverable
- **BR-4.3**: Misfilings SHALL be correctable without data loss
- **BR-4.4**: System SHALL support "undo" for recent operations

## Constraints

### Technical Constraints
- **TC-1**: Must run on Unraid server
- **TC-2**: Must integrate with existing ScanSnap workflow
- **TC-3**: Must use Python for primary development
- **TC-4**: Must be self-hosted (no cloud dependencies for core function)

### Resource Constraints
- **RC-1**: Scanner VM uses ~6GB RAM (unchangeable)
- **RC-2**: LLM API calls have rate limits
- **RC-3**: Single scanner input device
- **RC-4**: Windows VM dependency for OCR (current)

### Operational Constraints
- **OC-1**: No manual maintenance requirements
- **OC-2**: Must handle power failures gracefully
- **OC-3**: Must work with intermittent internet (LLM fallback)
- **OC-4**: Must preserve existing document organization

## Success Metrics

### Primary Metrics
- **M-1**: 80% of documents correctly categorized
- **M-2**: 90% of documents searchable within 1 minute
- **M-3**: Zero documents lost during processing
- **M-4**: <5 minutes weekly maintenance required

### Secondary Metrics
- **M-5**: 95% of bills identified before due date
- **M-6**: 100% of government notices flagged as priority
- **M-7**: <1% false positive rate on duplicate detection
- **M-8**: 90% reduction in time to find specific document

## Acceptance Criteria

### MVP Acceptance
- [ ] Can scan and auto-organize 10 diverse documents
- [ ] Documents are findable by content search
- [ ] No manual intervention required for standard documents
- [ ] System recovers from crashes without data loss
- [ ] Processing logs are comprehensive and useful

### Production Acceptance
- [ ] Handles 100+ document backlog successfully
- [ ] Maintains performance over 1000+ documents
- [ ] Correctly processes 8/10 document types
- [ ] Provides actionable daily summaries
- [ ] Integrates seamlessly with paperless-ngx

# Architecture Documentation

## System Overview

The Real-Time Moderation and Compliance Engine is a middleware service that intercepts and moderates AI chatbot responses before they reach end users. It ensures compliance with regional regulations (GDPR, HIPAA) and content policies.

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                         Frontend Layer                        │
│                         (React.js)                            │
└───────────────────────────┬──────────────────────────────────┘
                            │ REST API
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                      Backend API Layer                        │
│                       (FastAPI)                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Chat API Endpoint                          │  │
│  │         /api/v1/chat (POST)                            │  │
│  └────────────────┬───────────────────────────────────────┘  │
│                   │                                           │
│                   ▼                                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │           Chatbot Service                              │  │
│  │      (Generate Response)                               │  │
│  └────────────────┬───────────────────────────────────────┘  │
│                   │                                           │
│                   ▼                                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │         Moderation Service                             │  │
│  │   (Core Moderation Logic)                              │  │
│  │                                                         │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  1. Fetch Active Rules (Region-Specific)        │  │  │
│  │  │  2. Apply Each Rule                               │  │  │
│  │  │  3. Aggregate Results                             │  │  │
│  │  │  4. Determine Block/Allow                         │  │  │
│  │  │  5. Generate Fallback if Blocked                  │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────┬───────────────────────────────────────┘  │
│                   │                                           │
│                   ├──────────► ML Detector Service            │
│                   │            (Toxicity, PII)                │
│                   │                                           │
│                   ├──────────► Database Layer                 │
│                   │            (Rules, Audit Logs)            │
│                   │                                           │
│                   └──────────► Response                       │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Admin API Endpoints                        │  │
│  │  - GET/POST/PUT/DELETE /admin/rules                    │  │
│  │  - GET /admin/audit-logs                               │  │
│  │  - GET /admin/stats                                    │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                      Data Layer                               │
│                    (PostgreSQL)                               │
│                                                               │
│  Tables:                                                      │
│  - moderation_rules                                           │
│  - audit_logs                                                 │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                      ML Models Layer                          │
│                                                               │
│  - Detoxify (Toxicity Detection)                              │
│  - Custom Regex (PII Detection)                               │
└──────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (React.js)

**Location:** `/frontend/src/`

**Components:**
- `App.js` - Main application component with view routing
- `ChatInterface.js` - Chat UI with message handling
- `AdminPanel.js` - Admin dashboard for rules and logs

**Key Features:**
- Real-time chat interface
- Region selector for compliance rules
- Admin panel with rule management
- Audit log viewer
- Statistics dashboard

### 2. Backend API (FastAPI)

**Location:** `/backend/`

**Main File:** `main.py`

**Key Features:**
- RESTful API endpoints
- CORS middleware for frontend communication
- Automatic OpenAPI documentation
- Request/response validation with Pydantic

**Endpoints:**

#### Chat API
```
POST /api/v1/chat
- Accepts: {message, region, session_id}
- Returns: {response, request_id, is_moderated, moderation_info}
- Process: User message → Bot response → Moderation → Final response
```

#### Admin API
```
GET    /api/v1/admin/rules          - List all rules
POST   /api/v1/admin/rules          - Create rule
GET    /api/v1/admin/rules/{id}     - Get specific rule
PUT    /api/v1/admin/rules/{id}     - Update rule
DELETE /api/v1/admin/rules/{id}     - Delete rule
GET    /api/v1/admin/audit-logs     - Get audit logs
GET    /api/v1/admin/stats          - Get statistics
```

### 3. Moderation Service

**Location:** `/backend/app/services/moderation_service.py`

**Core Logic:**

```python
def moderate_response():
    1. Get active rules for region (sorted by priority)
    2. For each rule:
       - Apply rule logic
       - Check if flagged
       - Collect scores
    3. Determine if response should be blocked
    4. Generate fallback message if blocked
    5. Create audit log
    6. Return moderation result
```

**Key Features:**
- Priority-based rule execution
- Region-specific filtering
- Latency tracking
- Comprehensive audit logging

### 4. ML Detector Service

**Location:** `/backend/app/services/ml_detector.py`

**Detection Methods:**

#### Toxicity Detection
- **Model:** Detoxify (transformers-based)
- **Categories:** toxicity, severe_toxicity, obscene, threat, insult, identity_hate
- **Threshold:** Configurable (default: 0.7)

#### PII Detection
- **Method:** Regex patterns
- **Detects:** Email, phone, SSN, credit card, IP address
- **Patterns:** Pre-defined regex for each PII type

#### Financial Terms Detection
- **Method:** Keyword matching
- **Purpose:** Block restricted financial advice

#### Medical Terms Detection
- **Method:** Keyword matching
- **Purpose:** HIPAA compliance (US region)

### 5. Database Layer

**Technology:** PostgreSQL

**Schema:**

#### moderation_rules
```sql
- id: Primary key
- name: Rule name
- description: Rule description
- rule_type: ENUM (pii, toxicity, keyword, regex, financial, medical)
- region: ENUM (global, us, eu, uk, apac)
- patterns: JSONB array of keywords/patterns
- threshold: Float (0-1) for ML models
- config: JSONB for additional configuration
- is_active: Boolean
- priority: Integer (higher = checked first)
- created_at, updated_at: Timestamps
- created_by, updated_by: Audit fields
```

#### audit_logs
```sql
- id: Primary key
- request_id: Unique identifier for each request
- user_message: Original user message
- bot_response: Generated bot response
- is_flagged: Boolean
- is_blocked: Boolean
- flagged_rules: JSONB array of triggered rules
- moderation_scores: JSONB with ML model scores
- moderation_latency_ms: Float
- region: String
- final_response: Response sent to user
- timestamp: Timestamp
- client_ip, user_agent, session_id: Context fields
```

## Data Flow

### Chat Flow (100% Interception)

```
1. User sends message via frontend
   ↓
2. Frontend POST /api/v1/chat
   ↓
3. Chatbot service generates response
   ↓
4. START MODERATION (100% interception)
   ↓
5. Moderation service:
   a. Fetch active rules for region
   b. Apply each rule (priority order)
   c. Collect flags and scores
   d. Decide: allow or block
   e. Generate fallback if blocked
   f. Record start time → Calculate latency
   ↓
6. Create audit log entry
   ↓
7. Return moderated response to frontend
   ↓
8. Frontend displays response
```

### Admin Rule Update Flow (Zero Downtime)

```
1. Admin updates rule via API
   ↓
2. Database transaction commits
   ↓
3. Next chat request automatically fetches updated rules
   (No server restart required)
   ↓
4. Updated rule behavior immediately active
```

## Security Considerations

### 1. Input Validation
- All API inputs validated with Pydantic schemas
- SQL injection prevention via SQLAlchemy ORM
- Regex pattern validation to prevent ReDoS attacks

### 2. Data Privacy
- PII detected is logged but not stored in detail
- Audit logs can be configured for retention policies
- Database encryption recommended for production

### 3. Authentication & Authorization
**Current:** Not implemented (as per requirements)
**Recommendation for Production:**
- JWT-based authentication
- Role-based access control (RBAC)
- API key authentication for admin endpoints

## Performance Optimization

### Latency Targets
- **SLA:** <100ms per response
- **Target:** <50ms average

### Optimization Strategies

1. **Database Optimization**
   - Indexes on frequently queried fields (is_active, region, priority)
   - Connection pooling
   - Query optimization

2. **ML Model Optimization**
   - Models loaded once at startup
   - GPU acceleration (if available)
   - Model quantization for faster inference

3. **Caching Strategy**
   - Redis for rule caching
   - Response caching for identical inputs
   - ML model output caching

4. **Async Processing**
   - FastAPI async endpoints
   - Non-blocking database queries
   - Parallel rule evaluation (future enhancement)

## Scalability

### Horizontal Scaling
```
Load Balancer
    ↓
[Backend 1] [Backend 2] [Backend 3]
    ↓           ↓           ↓
    └───────────┴───────────┘
              ↓
        PostgreSQL
```

### Considerations
- Stateless backend services
- Shared database layer
- Redis for distributed caching
- Message queue for async processing (future)

## Monitoring & Observability

### Key Metrics

1. **Performance Metrics**
   - Average moderation latency
   - P95, P99 latency
   - Throughput (requests/second)

2. **Business Metrics**
   - Total requests
   - Flagged rate
   - Blocked rate
   - False positive rate

3. **System Metrics**
   - CPU usage
   - Memory usage
   - Database connection pool
   - ML model inference time

### Logging
- Structured JSON logs
- Request/response logging
- Error tracking
- Audit trail

## Error Handling & Fallback

### Moderation Service Errors
- **ML model fails:** Continue with rule-based checks
- **Database unavailable:** Use cached rules + log error
- **High latency:** Return original response + log warning

### Fallback Messages
- Default: Generic apology message
- PII-specific: Privacy-focused message
- Toxicity-specific: Community guidelines message
- Financial-specific: Disclaimer message
- Medical-specific: Professional consultation message

## Compliance Features

### GDPR (EU)
- Enhanced PII detection
- Data retention policies
- Right to deletion support

### HIPAA (US)
- Medical term filtering
- PHI detection
- Audit logging

### Regional Rules
- Dynamic rule assignment based on user region
- Multiple regions per rule (global + regional)
- Priority system for rule conflicts

## Future Enhancements

1. **Advanced ML Models**
   - Fine-tuned BERT models
   - Multi-language support
   - Context-aware detection

2. **Real-time Rule Updates**
   - WebSocket notifications
   - Rule versioning
   - A/B testing framework

3. **Advanced Analytics**
   - Trend analysis
   - False positive tracking
   - Rule effectiveness metrics

4. **Integration Improvements**
   - Webhook support
   - GraphQL API
   - Streaming responses

5. **Performance**
   - Rule caching with Redis
   - Parallel rule evaluation
   - GPU acceleration for ML models

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 | User interface |
| Backend | FastAPI | REST API |
| Database | PostgreSQL | Persistent storage |
| ML Framework | Transformers, Detoxify | Content detection |
| ORM | SQLAlchemy | Database abstraction |
| Validation | Pydantic | Schema validation |
| HTTP Client | Axios | API communication |

## Development Workflow

1. **Local Development**
   - Backend: `uvicorn main:app --reload`
   - Frontend: `npm start`
   - Database: Local PostgreSQL

2. **Testing**
   - Unit tests with pytest
   - Integration tests with TestClient
   - Manual testing with test_api.py

3. **Deployment**
   - Docker containers
   - Docker Compose for local deployment
   - Kubernetes for production (recommended)

## Conclusion

This architecture provides a robust, scalable, and compliant moderation system that meets all the specified requirements:

✅ 100% response interception
✅ <100ms latency target
✅ Region-specific rules (GDPR, HIPAA)
✅ Dynamic rule updates without downtime
✅ Comprehensive audit logging
✅ ML-based content detection
✅ Fallback mechanisms

# Testing Guide

This guide provides comprehensive test cases to validate the moderation system.

## Test Categories

1. PII Detection
2. Toxicity Detection
3. Region-Specific Rules
4. Financial Terms
5. Performance Testing
6. Admin API

## 1. PII Detection Tests

### Test Case 1.1: Email Detection
**Input:** "You can reach me at john.doe@example.com for more information"
**Expected:** Response should be flagged/blocked for PII

### Test Case 1.2: Phone Number Detection
**Input:** "Call me at 555-123-4567 or (555) 987-6543"
**Expected:** Response should be flagged/blocked for PII

### Test Case 1.3: SSN Detection
**Input:** "My SSN is 123-45-6789"
**Expected:** Response should be flagged/blocked for PII

### Test Case 1.4: Credit Card Detection
**Input:** "Use card number 4532-1234-5678-9010"
**Expected:** Response should be flagged/blocked for PII

### Test Case 1.5: No PII
**Input:** "What's the weather like today?"
**Expected:** Response should pass without PII flags

## 2. Toxicity Detection Tests

### Test Case 2.1: Offensive Language
**Input:** Message with offensive language
**Expected:** Response should be flagged/blocked for toxicity

### Test Case 2.2: Normal Conversation
**Input:** "That's a great idea! I really appreciate your help."
**Expected:** Response should pass without toxicity flags

## 3. Region-Specific Rules Tests

### Test Case 3.1: US HIPAA - Medical Terms
**Region:** United States (us)
**Input:** "Tell me about my diagnosis and treatment plan"
**Expected:** Response containing medical terms should be moderated

### Test Case 3.2: EU GDPR - Enhanced PII
**Region:** European Union (eu)
**Input:** Message requesting personal data
**Expected:** Stricter PII detection applied

### Test Case 3.3: Global Region
**Region:** Global
**Input:** Any message
**Expected:** Only global rules applied

## 4. Financial Terms Tests

### Test Case 4.1: Restricted Financial Advice
**Input:** "This is a guaranteed return investment"
**Expected:** Response should be flagged/blocked

### Test Case 4.2: Crypto Scam Detection
**Input:** "Send bitcoin to double your crypto"
**Expected:** Response should be flagged/blocked

### Test Case 4.3: Normal Financial Discussion
**Input:** "What are the general types of investment accounts?"
**Expected:** Response should pass

## 5. Performance Testing

### Test Case 5.1: Latency Check
**Goal:** Verify moderation latency < 100ms
**Method:**
1. Send multiple chat messages
2. Check Admin Panel → Statistics → Avg Latency
**Expected:** Average latency should be < 100ms

### Test Case 5.2: Throughput Test
**Goal:** Test system under load
**Method:**
```bash
# Use the provided load test script
cd backend
python test_load.py
```
**Expected:** System maintains <100ms latency under load

## 6. Admin API Tests

### Test Case 6.1: List All Rules
**Endpoint:** GET /api/v1/admin/rules
**Expected:** Returns all moderation rules with correct structure

### Test Case 6.2: Create New Rule
**Endpoint:** POST /api/v1/admin/rules
**Payload:**
```json
{
  "name": "Test Rule",
  "description": "A test moderation rule",
  "rule_type": "keyword",
  "region": "global",
  "patterns": ["test", "sample"],
  "is_active": true,
  "priority": 50
}
```
**Expected:** Rule created successfully, returned with ID

### Test Case 6.3: Update Rule
**Endpoint:** PUT /api/v1/admin/rules/{id}
**Payload:**
```json
{
  "is_active": false
}
```
**Expected:** Rule updated successfully

### Test Case 6.4: Delete Rule
**Endpoint:** DELETE /api/v1/admin/rules/{id}
**Expected:** Rule deleted successfully (204 status)

### Test Case 6.5: Get Audit Logs
**Endpoint:** GET /api/v1/admin/audit-logs
**Expected:** Returns paginated audit logs

### Test Case 6.6: Get Statistics
**Endpoint:** GET /api/v1/admin/stats
**Expected:** Returns correct statistics:
- total_requests
- flagged_requests
- blocked_requests
- flag_rate
- block_rate
- avg_latency_ms

## 7. Integration Tests

### Test Case 7.1: End-to-End Flow
1. Send message from frontend
2. Backend generates response
3. Moderation service processes response
4. Moderated response returned to frontend
5. Audit log created
6. Statistics updated

**Verification:**
- Check message appears in chat
- Check audit log in Admin Panel
- Verify statistics updated

### Test Case 7.2: Rule Update Without Downtime
1. Note current system behavior
2. Update a rule via Admin API
3. Send new messages
4. Verify new rule behavior immediately applied
**Expected:** No downtime, rules applied immediately

## 8. Edge Cases

### Test Case 8.1: Empty Message
**Input:** Empty string
**Expected:** Handled gracefully, appropriate error message

### Test Case 8.2: Very Long Message
**Input:** Message with 10,000+ characters
**Expected:** Processed within latency requirements

### Test Case 8.3: Special Characters
**Input:** Message with emojis, unicode characters
**Expected:** Processed correctly

### Test Case 8.4: Multiple PII Types
**Input:** Message with email, phone, and SSN
**Expected:** All PII types detected and flagged

## 9. Success Metrics Validation

### Metric 1: 100% Interception Rate
**Test:** Send 100 messages, verify all are logged
**Success Criteria:** All 100 messages in audit logs

### Metric 2: <100ms Latency
**Test:** Check average latency in statistics
**Success Criteria:** avg_latency_ms < 100

### Metric 3: Dynamic Rule Updates
**Test:** Create/update/delete rules via API
**Success Criteria:** Changes reflected immediately without restart

### Metric 4: <0.1% False Positives
**Test:** Send 1000 clean messages
**Success Criteria:** <1 message incorrectly flagged

## Automated Testing

### Run All Tests
```bash
cd backend
pytest tests/
```

### Run Specific Test Category
```bash
pytest tests/test_moderation.py
pytest tests/test_api.py
pytest tests/test_performance.py
```

## Manual Testing Checklist

- [ ] Chat interface loads correctly
- [ ] Messages can be sent and received
- [ ] Region selector works
- [ ] Admin panel accessible
- [ ] Rules can be viewed
- [ ] Rules can be created/updated/deleted
- [ ] Audit logs display correctly
- [ ] Statistics display correctly
- [ ] PII detection works
- [ ] Toxicity detection works
- [ ] Region-specific rules work
- [ ] Moderation badges display
- [ ] Latency is acceptable
- [ ] System handles errors gracefully

## Performance Benchmarks

Expected performance metrics:

| Metric | Target | Acceptable | Needs Improvement |
|--------|--------|------------|-------------------|
| Avg Latency | <50ms | <100ms | >100ms |
| P95 Latency | <100ms | <150ms | >150ms |
| Throughput | >100 req/s | >50 req/s | <50 req/s |
| False Positive Rate | <0.05% | <0.1% | >0.1% |
| Uptime | 99.9% | 99.5% | <99.5% |

## Troubleshooting Test Failures

### PII Detection Fails
- Check regex patterns in ml_detector.py
- Verify text is being processed correctly
- Check rule is active

### Toxicity Detection Fails
- Ensure Detoxify model is loaded
- Check threshold values
- Verify model weights downloaded

### Latency Too High
- Check database query performance
- Profile ML model inference time
- Consider caching strategies
- Check network latency

### Rules Not Applied
- Verify rule is active (is_active=true)
- Check rule priority
- Verify region matches
- Check rule type configuration

## Reporting Issues

When reporting test failures, include:
1. Test case number
2. Input data
3. Expected result
4. Actual result
5. Error messages/logs
6. System configuration
7. Timestamps

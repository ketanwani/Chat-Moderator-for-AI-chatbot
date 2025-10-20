# Prometheus Metrics Implementation Guide

This guide explains the Prometheus metrics implementation for tracking the moderation system's success metrics.

## Table of Contents
- [Overview](#overview)
- [Success Metrics Tracked](#success-metrics-tracked)
- [Available Metrics](#available-metrics)
- [Setup and Installation](#setup-and-installation)
- [Accessing Metrics](#accessing-metrics)
- [Grafana Dashboard Setup](#grafana-dashboard-setup)
- [Alerting Rules](#alerting-rules)

---

## Overview

The moderation system uses Prometheus for metrics collection to track and ensure compliance with these success criteria:

1. **100% Interception**: All responses pass through moderation before delivery
2. **99% SLA**: Moderation latency < 100ms for 99% of requests
3. **Zero-Downtime Updates**: Admin API updates reflected without restarts
4. **< 0.1% False Positives**: High precision in content moderation

---

## Success Metrics Tracked

### 1. 100% Interception Rate

**Metric**: `moderation_interception_total{intercepted="true|false"}`

Tracks whether responses successfully passed through moderation.

**Target**: `intercepted="true"` should be 100% of all requests

**Query for Compliance**:
```promql
# Interception rate
sum(moderation_interception_total{intercepted="true"}) / sum(moderation_interception_total) * 100
```

### 2. 99% SLA on Latency < 100ms

**Metrics**:
- `moderation_latency_seconds` (histogram)
- `moderation_sla_violations_total{severity="warning|critical"}`

**Target**: p99 latency < 100ms (0.1 seconds)

**Query for Compliance**:
```promql
# P99 latency
histogram_quantile(0.99, sum(rate(moderation_latency_seconds_bucket[5m])) by (le))

# SLA compliance rate
(sum(moderation_requests_total{status="success"}) - sum(moderation_sla_violations_total{severity="critical"}))
/ sum(moderation_requests_total{status="success"}) * 100
```

### 3. Zero-Downtime Rule Updates

**Metrics**:
- `moderation_active_rules_count{region, rule_type}`
- `database_query_seconds{query_type="get_active_rules"}`

Rules are loaded from database on each request, ensuring updates are reflected immediately.

**Query for Verification**:
```promql
# Rule loading time (should be fast with caching)
rate(database_query_seconds_sum{query_type="get_active_rules"}[5m])
/ rate(database_query_seconds_count{query_type="get_active_rules"}[5m])
```

### 4. < 0.1% False Positive Rate

**Metrics**:
- `moderation_false_positives_total{rule_type, region}`
- `moderation_true_positives_total{rule_type, region}`
- `false_positive_rate{rule_type, time_window}` (gauge)

**Target**: FPR < 0.001 (0.1%)

**Query for Compliance**:
```promql
# False positive rate
sum(moderation_false_positives_total)
/ (sum(moderation_false_positives_total) + sum(moderation_true_positives_total))
```

---

## Available Metrics

### Moderation Performance

| Metric | Type | Description | Labels |
|--------|------|-------------|--------|
| `moderation_latency_seconds` | Histogram | Moderation processing time | - |
| `moderation_sla_violations_total` | Counter | SLA violations (>100ms) | `severity` |
| `moderation_requests_total` | Counter | Total moderation requests | `region`, `status` |
| `moderation_responses_total` | Counter | Responses by decision | `decision`, `region` |

### Rule Performance

| Metric | Type | Description | Labels |
|--------|------|-------------|--------|
| `moderation_rules_triggered_total` | Counter | Rules triggered | `rule_id`, `rule_name`, `rule_type` |
| `rule_execution_time` | Histogram | Individual rule execution time | `rule_type` |
| `moderation_active_rules_count` | Gauge | Active rules count | `region`, `rule_type` |

### Quality Metrics

| Metric | Type | Description | Labels |
|--------|------|-------------|--------|
| `moderation_false_positives_total` | Counter | False positives | `rule_type`, `region` |
| `moderation_true_positives_total` | Counter | True positives | `rule_type`, `region` |
| `false_positive_rate` | Gauge | Current FPR | `rule_type`, `time_window` |

### ML Model Performance

| Metric | Type | Description | Labels |
|--------|------|-------------|--------|
| `ml_inference_time` | Histogram | ML model inference time | `model_type` |
| `ml_model_scores` | Histogram | ML confidence scores | `model_type` |

### Database Performance

| Metric | Type | Description | Labels |
|--------|------|-------------|--------|
| `database_query_time` | Histogram | Database query time | `query_type` |

### Chatbot Performance

| Metric | Type | Description | Labels |
|--------|------|-------------|--------|
| `chatbot_response_seconds` | Histogram | LLM response time | `provider` |
| `chatbot_errors_total` | Counter | Chatbot errors | `provider`, `error_type` |

---

## Setup and Installation

### Using Docker Compose (Recommended)

**Everything runs in Docker - no manual installation needed!**

```bash
# Start all services (Backend, Prometheus, Grafana, PostgreSQL)
docker-compose up -d
```

This automatically starts:
- ✅ Backend API with metrics endpoint
- ✅ Prometheus (metrics collection)
- ✅ Grafana (pre-configured dashboards)
- ✅ PostgreSQL database

**Access services:**
- Backend API: http://localhost:8000/docs
- Metrics Endpoint: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (login: admin/admin)

**Pre-configured dashboard:**
The "Moderation Engine - Success Metrics" dashboard auto-loads in Grafana with all metrics configured.

**For detailed Docker setup, see:** [DOCKER_MONITORING_SETUP.md](../DOCKER_MONITORING_SETUP.md)

---

### Manual Setup (Alternative - Not Recommended)

If you need to run without Docker:

#### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

The `prometheus-client==0.19.0` package is already included.

#### 2. Start the Application

```bash
python main.py
# or
uvicorn main:app --reload
```

#### 3. Verify Metrics Endpoint

```bash
curl http://localhost:8000/metrics
```

**Note:** With manual setup, you'll need to separately install and configure Prometheus and Grafana. Docker setup is much simpler!

---

## Accessing Metrics

### Direct Access

The metrics are available at:
```
http://localhost:8000/metrics
```

### Using the Test Script

Run the included test script to verify metrics collection:

```bash
python test_metrics.py
```

This will:
1. Test the health endpoint
2. Verify metrics endpoint is working
3. Send test chat requests
4. Analyze collected metrics
5. Calculate SLA compliance

---

## Grafana Dashboard

### Pre-built Dashboard (Docker Setup)

If using Docker Compose, the dashboard is **automatically loaded** when you start Grafana:

1. Open http://localhost:3001
2. Login: admin / admin
3. Dashboard "Moderation Engine - Success Metrics" is already there!

No manual configuration needed! 🎉

### Dashboard Panels

The pre-configured dashboard includes:

1. **SLA Compliance Gauge** - Shows % of requests <100ms (target: ≥99%)
2. **Interception Rate Gauge** - Shows % of responses intercepted (target: 100%)
3. **False Positive Rate Gauge** - Shows FPR (target: <0.1%)
4. **Latency Chart** - P50, P95, P99 response times over time
5. **Moderation Decisions** - Allowed vs Flagged vs Blocked (stacked area chart)
6. **Rules Triggered** - Pie chart by rule type
7. **Top 10 Rules** - Most frequently triggered rules
8. **ML Model Performance** - Inference times by model type
9. **Chatbot Performance** - Response times by provider

### Key PromQL Queries

If you need to create custom panels, here are the main queries:

**SLA Compliance:**
```promql
(sum(moderation_requests_total{status="success"}) - sum(moderation_sla_violations_total{severity="critical"}))
/ sum(moderation_requests_total{status="success"}) * 100
```

**Interception Rate:**
```promql
sum(moderation_interception_total{intercepted="true"}) / sum(moderation_interception_total) * 100
```

**P99 Latency:**
```promql
histogram_quantile(0.99, sum(rate(moderation_latency_seconds_bucket[5m])) by (le))
```

**False Positive Rate:**
```promql
sum(moderation_false_positives_total)
/ (sum(moderation_false_positives_total) + sum(moderation_true_positives_total))
```

---

## Alerting Rules

### Critical Alerts

**Alert: SLA Violation**
```yaml
- alert: ModerationSLAViolation
  expr: |
    (sum(moderation_requests_total{status="success"}) - sum(moderation_sla_violations_total{severity="critical"}))
    / sum(moderation_requests_total{status="success"}) < 0.99
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Moderation SLA below 99%"
    description: "Only {{ $value | humanizePercentage }} of requests meet <100ms SLA"
```

**Alert: Interception Failure**
```yaml
- alert: ModerationInterceptionFailure
  expr: |
    sum(moderation_interception_total{intercepted="false"}) > 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Responses bypassing moderation detected"
    description: "{{ $value }} responses failed to be intercepted by moderation"
```

**Alert: High False Positive Rate**
```yaml
- alert: HighFalsePositiveRate
  expr: |
    sum(moderation_false_positives_total)
    / (sum(moderation_false_positives_total) + sum(moderation_true_positives_total)) > 0.001
  for: 15m
  labels:
    severity: warning
  annotations:
    summary: "False positive rate above 0.1%"
    description: "Current FPR: {{ $value | humanizePercentage }}"
```

### Warning Alerts

**Alert: Latency Warning**
```yaml
- alert: ModerationLatencyHigh
  expr: |
    histogram_quantile(0.95, sum(rate(moderation_latency_seconds_bucket[5m])) by (le)) > 0.08
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "Moderation latency approaching SLA threshold"
    description: "P95 latency is {{ $value }}s (threshold: 100ms)"
```

---

## Monitoring Best Practices

### 1. Regular SLA Reviews
- Review latency metrics daily
- Investigate p99 spikes
- Optimize slow rules

### 2. Interception Verification
- Monitor `moderation_interception_total` continuously
- Alert on any `intercepted="false"` occurrences
- Test fail-safe behavior regularly

### 3. False Positive Tracking
- Implement feedback collection system
- Regular review of flagged content
- Adjust rule thresholds based on data

### 4. Performance Optimization
- Cache frequently accessed rules
- Parallelize independent rule checks
- Optimize ML model inference
- Use connection pooling for database

---

## Next Steps

1. **Set up Prometheus**: Configure Prometheus to scrape the `/metrics` endpoint
2. **Create Grafana Dashboards**: Visualize the success metrics
3. **Configure Alerts**: Set up alerting for SLA violations and failures
4. **Implement Feedback API**: Build system for tracking false positives
5. **Load Testing**: Verify metrics under production load

---

## Troubleshooting

### Metrics not appearing
- Check that server is running: `curl http://localhost:8000/health`
- Verify metrics endpoint: `curl http://localhost:8000/metrics`
- Check logs for errors

### High latency
- Review `rule_execution_time` to identify slow rules
- Check `database_query_time` for slow queries
- Monitor `ml_inference_time` for ML model performance

### SLA violations
- Scale horizontally (add more instances)
- Optimize database queries
- Add caching layer for rules
- Consider async rule execution

---

## Support

For issues or questions:
1. Check application logs: configured in `backend/main.py`
2. Review audit logs in database
3. Analyze Prometheus metrics for patterns
4. Consult this guide and related documentation

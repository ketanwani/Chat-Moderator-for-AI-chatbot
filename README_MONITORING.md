# Monitoring & Metrics - Complete Guide

## 🎯 TL;DR - Get Started in 2 Minutes

```bash
# 1. Start everything (including Prometheus & Grafana)
docker-compose up -d

# 2. Open Grafana dashboard
# http://localhost:3001 (login: admin/admin)

# 3. Generate test data
pip install requests
python backend/test_metrics.py

# 4. View your success metrics in Grafana!
```

That's it! You now have a complete monitoring stack tracking all 4 success metrics. 🎉

---

## 📊 What Success Metrics Are Tracked?

| Metric | Target | Implementation | Status |
|--------|--------|----------------|--------|
| **100% Interception** | All responses through moderation | Fail-safe wrapper in chat endpoint | ✅ Complete |
| **99% SLA** | <100ms latency | Histogram + SLA violation counter | ✅ Complete |
| **Zero-Downtime Updates** | Immediate rule changes | Database-driven rules | ✅ Complete |
| **<0.1% False Positives** | High accuracy | TP/FP counters + feedback API | ✅ Framework Ready |

---

## 🏗️ Architecture

```
┌──────────┐
│  User    │
└────┬─────┘
     │
     ▼
┌──────────────────┐
│  Frontend (React)│
│  localhost:3000  │
└────┬─────────────┘
     │
     ▼
┌──────────────────────────────────┐
│  Backend (FastAPI)               │
│  localhost:8000                  │
│                                  │
│  ┌────────────┐  ┌────────────┐ │
│  │ Chat API   │→ │ Moderation │ │
│  └────────────┘  │ Service    │ │
│                  └──┬─────────┘ │
│                     │           │
│  /metrics endpoint  │           │
│  (Prometheus format)│           │
└─────────────────────┼───────────┘
                      │
                      ▼
              ┌───────────────┐
              │  Prometheus   │ ← Scrapes every 10s
              │  localhost:9090│
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │   Grafana     │ ← Visualizes
              │  localhost:3001│
              └───────────────┘
```

---

## 📁 Files Added/Modified

### New Files Created:

```
project/
├── prometheus.yml                    # Prometheus configuration
├── alert_rules.yml                   # Alert definitions
├── MONITORING_QUICKSTART.md          # Quick start guide
├── DOCKER_MONITORING_SETUP.md        # Detailed Docker setup
├── MONITORING_SUMMARY.md             # Implementation summary
├── backend/
│   ├── app/core/metrics.py           # Metrics definitions
│   ├── test_metrics.py               # Test script
│   └── METRICS_GUIDE.md              # Metrics documentation
└── grafana/
    ├── provisioning/
    │   ├── datasources/prometheus.yml
    │   └── dashboards/default.yml
    └── dashboards/
        └── moderation-metrics.json   # Pre-built dashboard
```

### Modified Files:

```
project/
├── docker-compose.yml                # Added Prometheus + Grafana
├── backend/
│   ├── requirements.txt              # Added prometheus-client
│   ├── main.py                       # Added /metrics endpoint
│   ├── app/
│   │   ├── services/
│   │   │   └── moderation_service.py # Integrated metrics
│   │   └── api/
│   │       └── chat.py               # Added fail-safe + metrics
```

---

## 🚀 Quick Start Guides

Choose your path:

### 1. Docker (Recommended)
👉 **[MONITORING_QUICKSTART.md](MONITORING_QUICKSTART.md)** - 2-minute setup

### 2. Detailed Docker Setup
👉 **[DOCKER_MONITORING_SETUP.md](DOCKER_MONITORING_SETUP.md)** - Complete Docker guide

### 3. Manual Setup
👉 **[backend/METRICS_GUIDE.md](backend/METRICS_GUIDE.md)** - Install Prometheus manually

---

## 🎛️ Access Your Monitoring Stack

Once running, access these URLs:

| Service | URL | Purpose | Credentials |
|---------|-----|---------|-------------|
| **Grafana Dashboard** | http://localhost:3001 | View all metrics visually | admin / admin |
| **Prometheus UI** | http://localhost:9090 | Query metrics, view alerts | - |
| **Metrics Endpoint** | http://localhost:8000/metrics | Raw Prometheus metrics | - |
| **API Docs** | http://localhost:8000/docs | Test API endpoints | - |
| **Frontend** | http://localhost:3000 | User interface | - |

---

## 📈 Grafana Dashboard Overview

The pre-built dashboard shows:

### Top Row - Success Metrics (Gauges)
1. **SLA Compliance** (target: ≥99%)
   - Green: ≥99%, Yellow: 95-99%, Red: <95%

2. **Interception Rate** (target: 100%)
   - Green: 100%, Yellow: ≥99%, Red: <99%

3. **False Positive Rate** (target: <0.1%)
   - Green: <0.05%, Yellow: 0.05-0.1%, Red: >0.1%

### Charts
4. **Latency Over Time** - P50, P95, P99 response times
5. **Moderation Decisions** - Allowed vs Flagged vs Blocked
6. **Rules Triggered** - Pie chart by rule type
7. **Top 10 Rules** - Most frequently triggered
8. **ML Model Performance** - Inference times
9. **Chatbot Performance** - Response times by provider

---

## 🔔 Alert Rules

Prometheus automatically monitors these conditions:

### Critical Alerts (Require Immediate Action)

| Alert | Condition | Meaning |
|-------|-----------|---------|
| `ModerationSLAViolation` | SLA compliance <99% for 5min | Too many slow requests |
| `ModerationP99LatencyExceeded` | P99 latency >100ms for 5min | Performance degradation |
| `ModerationInterceptionFailure` | Any response bypasses moderation | Security breach |
| `BackendServiceDown` | Service unreachable for 1min | System outage |

### Warning Alerts (Monitor Closely)

| Alert | Condition | Meaning |
|-------|-----------|---------|
| `ModerationLatencyHigh` | P95 latency >80ms for 10min | Approaching SLA limit |
| `HighFalsePositiveRate` | FPR >0.1% for 15min | Quality degradation |
| `DatabaseQuerySlow` | P95 DB time >50ms for 10min | Database bottleneck |
| `MLInferenceSlow` | P95 ML time >50ms for 10min | Model bottleneck |

View alerts: http://localhost:9090/alerts

---

## 🧪 Testing & Verification

### 1. Start Services
```bash
docker-compose up -d
docker-compose ps  # Verify all services are "Up"
```

### 2. Check Metrics Endpoint
```bash
curl http://localhost:8000/metrics | head -20
```

Expected output:
```
# HELP moderation_latency_seconds Time spent in moderation layer (seconds)
# TYPE moderation_latency_seconds histogram
...
```

### 3. Verify Prometheus is Scraping
Open: http://localhost:9090/targets

Should show: `moderation_backend (1/1 up)` ✅

### 4. Run Test Suite
```bash
pip install requests
python backend/test_metrics.py
```

This sends test requests and verifies metrics collection.

### 5. View Dashboard
1. Open http://localhost:3001
2. Login: admin / admin
3. Dashboard auto-loads with live data

---

## 📊 Key Metrics Explained

### Latency Histogram
```promql
moderation_latency_seconds
```
- **Type**: Histogram
- **Buckets**: 10ms, 25ms, 50ms, 75ms, 100ms, 150ms, 200ms, 500ms, 1s
- **Use**: Calculate percentiles (P50, P95, P99)

### SLA Violations Counter
```promql
moderation_sla_violations_total{severity="critical"}
```
- **Type**: Counter
- **Labels**: severity (warning/critical)
- **Use**: Track requests >100ms

### Interception Tracking
```promql
moderation_interception_total{intercepted="true|false"}
```
- **Type**: Counter
- **Labels**: intercepted (true/false)
- **Use**: Verify 100% coverage

### False Positive Rate
```promql
moderation_false_positives_total / (moderation_false_positives_total + moderation_true_positives_total)
```
- **Type**: Derived from counters
- **Use**: Track quality over time

---

## 🔍 Common Queries

### Check SLA Compliance
```promql
(sum(moderation_requests_total{status="success"}) - sum(moderation_sla_violations_total{severity="critical"}))
/ sum(moderation_requests_total{status="success"}) * 100
```

### Get P99 Latency
```promql
histogram_quantile(0.99, sum(rate(moderation_latency_seconds_bucket[5m])) by (le))
```

### View Top Slowest Rules
```promql
topk(5,
  rate(rule_execution_time_sum[5m])
  / rate(rule_execution_time_count[5m])
)
```

### Calculate Request Rate
```promql
rate(moderation_requests_total[5m])
```

---

## 🛠️ Troubleshooting

### Grafana Dashboard is Empty

**Solution 1**: Generate test data
```bash
python backend/test_metrics.py
```

**Solution 2**: Check time range
- Click time picker (top right)
- Select "Last 5 minutes"

**Solution 3**: Verify Prometheus connection
- Grafana → Configuration → Data Sources
- Test connection to Prometheus

### Prometheus Shows "Target Down"

**Check backend is running:**
```bash
docker-compose ps backend
curl http://localhost:8000/metrics
```

**View Prometheus logs:**
```bash
docker-compose logs prometheus
```

**Restart services:**
```bash
docker-compose restart backend prometheus
```

### Metrics Not Updating

**Check scrape interval:**
- Default is 10 seconds
- Wait at least 15 seconds after generating traffic

**Force Prometheus reload:**
```bash
curl -X POST http://localhost:9090/-/reload
```

---

## 🎯 Production Checklist

Before deploying to production:

- [ ] Change Grafana admin password
- [ ] Enable HTTPS for all services
- [ ] Set up Alertmanager for notifications (email/Slack)
- [ ] Configure data retention (default 15 days)
- [ ] Set up regular backups of Prometheus data
- [ ] Add authentication to Prometheus
- [ ] Configure firewall rules
- [ ] Set resource limits in docker-compose
- [ ] Test alert rules fire correctly
- [ ] Document runbook procedures

---

## 📚 Documentation Index

1. **[MONITORING_QUICKSTART.md](MONITORING_QUICKSTART.md)** - Start here! 2-minute setup
2. **[DOCKER_MONITORING_SETUP.md](DOCKER_MONITORING_SETUP.md)** - Complete Docker guide
3. **[MONITORING_SUMMARY.md](MONITORING_SUMMARY.md)** - Implementation details
4. **[backend/METRICS_GUIDE.md](backend/METRICS_GUIDE.md)** - Metrics reference
5. **[prometheus.yml](prometheus.yml)** - Prometheus configuration
6. **[alert_rules.yml](alert_rules.yml)** - Alert rule definitions

---

## 🎉 Success!

You now have:
- ✅ Prometheus collecting metrics every 10 seconds
- ✅ Grafana dashboard visualizing all success metrics
- ✅ Automated alerts for SLA violations
- ✅ Complete observability into your moderation engine
- ✅ All running in Docker with one command

**Just run `docker-compose up -d` and start monitoring!** 🚀

---

## 💡 Next Steps

1. ✅ **Setup Complete** - Monitoring is running
2. 📊 **View Metrics** - Open Grafana dashboard
3. 🧪 **Test Alerts** - Trigger an alert condition
4. 📈 **Monitor Production** - Watch real traffic patterns
5. 🎯 **Optimize** - Use metrics to improve performance
6. 🔔 **Add Notifications** - Set up Alertmanager
7. 📝 **Create Runbooks** - Document incident response

---

## 🆘 Need Help?

- **Metrics not showing?** → Check [Troubleshooting](#-troubleshooting)
- **Want to customize?** → See [DOCKER_MONITORING_SETUP.md](DOCKER_MONITORING_SETUP.md)
- **Understanding metrics?** → Read [METRICS_GUIDE.md](backend/METRICS_GUIDE.md)
- **Quick start?** → Try [MONITORING_QUICKSTART.md](MONITORING_QUICKSTART.md)

**Pro tip**: Run `docker-compose logs -f` to see all logs in real-time while troubleshooting.

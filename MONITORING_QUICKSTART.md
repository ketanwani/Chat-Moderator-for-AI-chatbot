# Monitoring Quick Start

Get the complete monitoring stack running in 2 minutes!

## What You'll Get

✅ **Prometheus** - Collecting metrics every 10 seconds
✅ **Grafana** - Beautiful dashboards showing all success metrics
✅ **Alerts** - Automated alerts for SLA violations
✅ **All in Docker** - No manual installation needed!

## Start Everything

```bash
# Start all services (including Prometheus & Grafana)
docker-compose up -d

# Wait 30 seconds for everything to initialize
# Then open Grafana
```

**Open in browser:**
- **Grafana Dashboard**: http://localhost:3001
  - Login: `admin` / `admin`
  - Dashboard: "Moderation Engine - Success Metrics"

- **Prometheus**: http://localhost:9090
- **Backend API**: http://localhost:8000/docs
- **Raw Metrics**: http://localhost:8000/metrics

## What You'll See

### In Grafana Dashboard:

1. **🎯 SLA Compliance** (Target: ≥99%)
   - Shows % of requests processed in <100ms

2. **🛡️ Interception Rate** (Target: 100%)
   - Confirms ALL responses go through moderation

3. **✓ False Positive Rate** (Target: <0.1%)
   - Tracks moderation accuracy

4. **📊 Latency Charts**
   - P50, P95, P99 response times
   - Real-time performance visualization

5. **📈 Decision Breakdown**
   - Allowed vs Flagged vs Blocked responses

6. **🔍 Rule Performance**
   - Which rules are triggering most often
   - Execution time per rule type

## Generate Test Data

```bash
# Install requests if needed
pip install requests

# Run test script
python backend/test_metrics.py
```

This will send test requests and you'll immediately see metrics appear in Grafana!

## Success Metrics at a Glance

| Metric | Location | Target | Status |
|--------|----------|--------|--------|
| **100% Interception** | Grafana → Top Right Gauge | 100% | ✅ Implemented |
| **99% SLA (<100ms)** | Grafana → Top Left Gauge | ≥99% | ✅ Implemented |
| **Zero-Downtime Updates** | Database-driven rules | Real-time | ✅ Working |
| **<0.1% False Positives** | Grafana → Top Center Gauge | <0.1% | ✅ Framework Ready |

## Troubleshooting

**Dashboard is empty?**
```bash
# Check services are running
docker-compose ps

# Generate test data
python backend/test_metrics.py

# Wait 15 seconds, then refresh Grafana
```

**Can't connect to Grafana?**
```bash
# Check Grafana logs
docker-compose logs grafana

# Restart Grafana
docker-compose restart grafana
```

**Prometheus not collecting metrics?**
```bash
# Check if backend metrics endpoint works
curl http://localhost:8000/metrics

# Check Prometheus targets (should show "UP")
# Open: http://localhost:9090/targets
```

## Next Steps

1. ✅ **Dashboard Running** - You're viewing metrics in Grafana
2. 📊 **Send Real Traffic** - Use the frontend at http://localhost:3000
3. 🚨 **Test Alerts** - Prometheus will alert if SLA is violated
4. 📈 **Monitor Trends** - Watch performance over hours/days

## Full Documentation

- **Complete Setup Guide**: [DOCKER_MONITORING_SETUP.md](DOCKER_MONITORING_SETUP.md)
- **Metrics Details**: [backend/METRICS_GUIDE.md](backend/METRICS_GUIDE.md)
- **Alert Rules**: [alert_rules.yml](alert_rules.yml)

## Stop Everything

```bash
docker-compose down
```

---

**That's it!** You now have a production-grade monitoring stack running. 🎉

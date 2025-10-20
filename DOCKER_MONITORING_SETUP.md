# Docker Monitoring Setup Guide

This guide shows you how to run Prometheus and Grafana alongside your moderation engine using Docker Compose.

## Quick Start

### 1. Start All Services

```bash
docker-compose up -d
```

This will start:
- **PostgreSQL** (port 5432) - Database
- **Backend API** (port 8000) - Moderation engine
- **Frontend** (port 3000) - Web UI
- **Prometheus** (port 9090) - Metrics collection
- **Grafana** (port 3001) - Metrics visualization

### 2. Access the Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Backend API | http://localhost:8000 | - |
| API Docs | http://localhost:8000/docs | - |
| Metrics Endpoint | http://localhost:8000/metrics | - |
| Frontend | http://localhost:3000 | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3001 | admin / admin |

### 3. View Metrics in Grafana

1. Open Grafana: http://localhost:3001
2. Login with: `admin` / `admin` (you'll be prompted to change the password)
3. The **"Moderation Engine - Success Metrics"** dashboard should be automatically loaded
4. If not, go to Dashboards → Browse → Select "Moderation Engine - Success Metrics"

### 4. Generate Test Data

Run the test script to generate some metrics:

```bash
# Make sure services are running
docker-compose ps

# Install test dependencies
pip install requests

# Run the test script
python backend/test_metrics.py
```

### 5. View Real-time Metrics

In Grafana, you'll see:
- **SLA Compliance Gauge** - Should show 99%+ (green)
- **Interception Rate** - Should show 100% (green)
- **False Positive Rate** - Should be <0.1%
- **Latency Charts** - P50, P95, P99 response times
- **Decision Breakdown** - Allowed vs Blocked vs Flagged
- **Rule Performance** - Which rules are triggering

---

## Detailed Setup

### Service Architecture

```
┌─────────────┐      ┌──────────────┐
│   Frontend  │─────▶│   Backend    │
│   (React)   │      │   (FastAPI)  │
└─────────────┘      └──────┬───────┘
                            │
                            ├─────▶ PostgreSQL (data)
                            │
                            ├─────▶ /metrics endpoint
                            │
                     ┌──────▼───────┐
                     │  Prometheus  │ (scrapes every 10s)
                     └──────┬───────┘
                            │
                     ┌──────▼───────┐
                     │   Grafana    │ (visualizes)
                     └──────────────┘
```

### Prometheus Configuration

The Prometheus configuration is in `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'moderation_backend'
    scrape_interval: 10s  # Scrape every 10 seconds
    metrics_path: '/metrics'
    static_configs:
      - targets: ['backend:8000']
```

**Key settings:**
- Scrapes backend every 10 seconds for real-time monitoring
- Stores data in a Docker volume for persistence
- Alert rules defined in `alert_rules.yml`

### Alert Rules

Prometheus will automatically evaluate these alerts:

| Alert | Severity | Trigger Condition |
|-------|----------|-------------------|
| ModerationSLAViolation | Critical | SLA compliance < 99% for 5 minutes |
| ModerationP99LatencyExceeded | Critical | P99 latency > 100ms for 5 minutes |
| ModerationInterceptionFailure | Critical | Any response bypasses moderation |
| HighFalsePositiveRate | Warning | FPR > 0.1% for 15 minutes |
| ModerationLatencyHigh | Warning | P95 latency > 80ms for 10 minutes |

View active alerts at: http://localhost:9090/alerts

### Grafana Dashboard

The dashboard shows all 4 success metrics:

1. **SLA Compliance Gauge**
   - Query: `(sum(moderation_requests_total{status="success"}) - sum(moderation_sla_violations_total{severity="critical"})) / sum(moderation_requests_total{status="success"}) * 100`
   - Target: ≥99%

2. **Interception Rate Gauge**
   - Query: `sum(moderation_interception_total{intercepted="true"}) / sum(moderation_interception_total) * 100`
   - Target: 100%

3. **False Positive Rate Gauge**
   - Query: `sum(moderation_false_positives_total) / (sum(moderation_false_positives_total) + sum(moderation_true_positives_total))`
   - Target: <0.1%

4. **Latency Chart**
   - Shows P50, P95, P99 over time
   - Threshold line at 100ms

---

## Common Commands

### Start services
```bash
docker-compose up -d
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f prometheus
docker-compose logs -f grafana
```

### Stop services
```bash
docker-compose down
```

### Stop and remove all data (CAREFUL!)
```bash
docker-compose down -v
```

### Restart a specific service
```bash
docker-compose restart backend
docker-compose restart prometheus
```

### Check service health
```bash
docker-compose ps
```

### View metrics directly
```bash
# Raw Prometheus metrics
curl http://localhost:8000/metrics

# Prometheus query
curl 'http://localhost:9090/api/v1/query?query=moderation_latency_seconds'
```

---

## Troubleshooting

### Prometheus not showing data

**Check if Prometheus can reach backend:**
```bash
# Enter Prometheus container
docker exec -it moderation_prometheus sh

# Try to reach backend
wget -O- http://backend:8000/metrics
```

**Check Prometheus targets:**
- Go to http://localhost:9090/targets
- The `moderation_backend` target should be "UP"
- If "DOWN", check backend logs

### Grafana dashboard is empty

1. **Check Prometheus data source:**
   - Grafana → Configuration → Data Sources
   - Should see "Prometheus" configured
   - Test connection

2. **Check time range:**
   - Top right corner of dashboard
   - Change to "Last 5 minutes" or "Last 1 hour"

3. **Generate test data:**
   ```bash
   python backend/test_metrics.py
   ```

### Backend metrics not updating

**Check if prometheus-client is installed:**
```bash
docker exec -it moderation_backend pip list | grep prometheus
```

**Verify metrics endpoint:**
```bash
curl http://localhost:8000/metrics | head -20
```

Should see output like:
```
# HELP moderation_latency_seconds Time spent in moderation layer (seconds)
# TYPE moderation_latency_seconds histogram
...
```

### Port conflicts

If ports are already in use:

**Option 1: Stop conflicting services**
```bash
# Find what's using the port
netstat -ano | findstr :9090
netstat -ano | findstr :3001

# Kill the process (Windows)
taskkill /PID <pid> /F
```

**Option 2: Change ports in docker-compose.yml**
```yaml
prometheus:
  ports:
    - "9091:9090"  # Change 9090 to 9091

grafana:
  ports:
    - "3002:3000"  # Change 3001 to 3002
```

---

## Customization

### Change Grafana Password

1. Login to Grafana
2. Click on avatar (bottom left) → Profile → Change Password

Or set via environment variable in `docker-compose.yml`:
```yaml
grafana:
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=your-secure-password
```

### Add More Dashboards

1. Create dashboard in Grafana UI
2. Export as JSON
3. Save to `grafana/dashboards/`
4. Restart Grafana: `docker-compose restart grafana`

### Modify Alert Rules

Edit `alert_rules.yml` and reload Prometheus:
```bash
# Edit the file
nano alert_rules.yml

# Reload Prometheus configuration
curl -X POST http://localhost:9090/-/reload
```

### Change Scrape Interval

Edit `prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'moderation_backend'
    scrape_interval: 5s  # Change to 5 seconds for more granular data
```

Restart Prometheus:
```bash
docker-compose restart prometheus
```

---

## Production Considerations

### 1. Data Retention

By default, Prometheus keeps 15 days of data. To change:

```yaml
prometheus:
  command:
    - '--storage.tsdb.retention.time=30d'  # Keep 30 days
```

### 2. Resource Limits

Add resource limits to prevent OOM:

```yaml
prometheus:
  deploy:
    resources:
      limits:
        memory: 2G
        cpus: '1.0'

grafana:
  deploy:
    resources:
      limits:
        memory: 512M
        cpus: '0.5'
```

### 3. Persistent Storage

Data is already stored in Docker volumes:
- `prometheus_data` - Metrics data
- `grafana_data` - Dashboards and settings

**Backup volumes:**
```bash
# Backup Prometheus data
docker run --rm -v moderation_prometheus_data:/data -v $(pwd):/backup ubuntu tar czf /backup/prometheus-backup.tar.gz -C /data .

# Backup Grafana data
docker run --rm -v moderation_grafana_data:/data -v $(pwd):/backup ubuntu tar czf /backup/grafana-backup.tar.gz -C /data .
```

### 4. Security

**Production checklist:**
- [ ] Change Grafana admin password
- [ ] Enable HTTPS for Grafana
- [ ] Add authentication to Prometheus
- [ ] Restrict network access (firewall rules)
- [ ] Use secrets management for passwords

### 5. External Prometheus

If you want to use an external Prometheus instance:

1. Remove Prometheus from `docker-compose.yml`
2. Configure external Prometheus to scrape: `http://your-host:8000/metrics`
3. Point Grafana data source to external Prometheus

---

## Next Steps

1. ✅ **Services Running** - All containers are up
2. ✅ **Metrics Collecting** - Prometheus scraping backend
3. ✅ **Dashboard Visible** - Grafana showing data
4. 🔄 **Generate Load** - Run test suite or use the application
5. 📊 **Monitor Trends** - Watch metrics over time
6. 🚨 **Test Alerts** - Trigger alert conditions
7. 🎯 **Optimize** - Use metrics to improve performance

---

## Support

**Check service status:**
```bash
docker-compose ps
```

**View all logs:**
```bash
docker-compose logs -f
```

**Restart everything:**
```bash
docker-compose restart
```

**Full reset (DELETES ALL DATA):**
```bash
docker-compose down -v
docker-compose up -d
```

For more information:
- [Backend Metrics Guide](backend/METRICS_GUIDE.md)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

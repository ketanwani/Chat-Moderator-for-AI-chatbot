"""
Prometheus metrics for the moderation system

This module defines all Prometheus metrics for tracking:
- Moderation latency and SLA compliance
- Interception rates
- False positive rates
- Rule performance
- System health
"""

from prometheus_client import Counter, Histogram, Gauge, Info
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# MODERATION METRICS
# =============================================================================

# Latency histogram with buckets optimized for 100ms SLA
moderation_latency_histogram = Histogram(
    'moderation_latency_seconds',
    'Time spent in moderation layer (seconds)',
    buckets=[0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.5, 1.0]  # 10ms to 1s
)

# SLA violations counter
moderation_sla_violations = Counter(
    'moderation_sla_violations_total',
    'Number of moderation requests exceeding 100ms SLA',
    ['severity']  # 'warning' (80-100ms), 'critical' (>100ms)
)

# Total moderation requests
moderation_requests_total = Counter(
    'moderation_requests_total',
    'Total number of moderation requests processed',
    ['region', 'status']  # status: success, error, timeout
)

# Interception rate (should be 100%)
moderation_interception_total = Counter(
    'moderation_interception_total',
    'Total responses intercepted by moderation',
    ['intercepted']  # 'true' or 'false'
)

# =============================================================================
# RULE PERFORMANCE METRICS
# =============================================================================

# Responses blocked vs allowed
moderation_responses_total = Counter(
    'moderation_responses_total',
    'Total responses by moderation decision',
    ['decision', 'region']  # decision: blocked, allowed, flagged
)

# Rules triggered
moderation_rules_triggered = Counter(
    'moderation_rules_triggered_total',
    'Number of times each rule was triggered',
    ['rule_id', 'rule_name', 'rule_type']
)

# Rule execution time
rule_execution_time = Histogram(
    'moderation_rule_execution_seconds',
    'Time to execute individual moderation rules',
    ['rule_type'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1]
)

# =============================================================================
# QUALITY METRICS (FALSE POSITIVES)
# =============================================================================

# False positive tracking
moderation_false_positives = Counter(
    'moderation_false_positives_total',
    'Number of confirmed false positives',
    ['rule_type', 'region']
)

# True positive tracking
moderation_true_positives = Counter(
    'moderation_true_positives_total',
    'Number of confirmed true positives',
    ['rule_type', 'region']
)

# False positive rate gauge (updated periodically)
false_positive_rate = Gauge(
    'moderation_false_positive_rate',
    'Current false positive rate (0-1)',
    ['rule_type', 'time_window']  # time_window: 1h, 24h, 7d
)

# =============================================================================
# CHATBOT METRICS
# =============================================================================

# Chatbot response generation time
chatbot_response_time = Histogram(
    'chatbot_response_seconds',
    'Time to generate chatbot response',
    ['provider'],  # openai, anthropic, ollama, mock
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# Chatbot errors
chatbot_errors_total = Counter(
    'chatbot_errors_total',
    'Number of chatbot errors',
    ['provider', 'error_type']
)

# =============================================================================
# SYSTEM HEALTH METRICS
# =============================================================================

# Active rules gauge
active_rules_count = Gauge(
    'moderation_active_rules_count',
    'Number of active moderation rules',
    ['region', 'rule_type']
)

# Database query time
database_query_time = Histogram(
    'database_query_seconds',
    'Database query execution time',
    ['query_type'],  # get_rules, create_audit_log, etc.
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.5]
)

# Cache hit rate
cache_hits_total = Counter(
    'cache_hits_total',
    'Number of cache hits',
    ['cache_type']  # rules_cache, ml_model_cache
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Number of cache misses',
    ['cache_type']
)

# =============================================================================
# ML MODEL METRICS
# =============================================================================

# ML model inference time
ml_inference_time = Histogram(
    'ml_inference_seconds',
    'ML model inference time',
    ['model_type'],  # toxicity, pii, etc.
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)

# ML model scores distribution
ml_model_scores = Histogram(
    'ml_model_scores',
    'Distribution of ML model confidence scores',
    ['model_type'],
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

# =============================================================================
# APPLICATION INFO
# =============================================================================

# Application info
app_info = Info(
    'moderation_app',
    'Moderation application information'
)

# Initialize app info
app_info.info({
    'version': '1.0.0',
    'component': 'moderation_engine'
})


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def track_moderation_latency(latency_seconds: float, region: str):
    """
    Track moderation latency and SLA compliance

    Args:
        latency_seconds: Latency in seconds
        region: User region
    """
    # Record latency
    moderation_latency_histogram.observe(latency_seconds)

    # Check SLA violations
    latency_ms = latency_seconds * 1000

    if latency_ms > 100:
        moderation_sla_violations.labels(severity='critical').inc()
        logger.warning(f"SLA violation: {latency_ms:.2f}ms (critical) in region {region}")
    elif latency_ms > 80:
        moderation_sla_violations.labels(severity='warning').inc()
        logger.info(f"SLA warning: {latency_ms:.2f}ms (approaching threshold) in region {region}")


def track_moderation_decision(is_blocked: bool, is_flagged: bool, region: str):
    """
    Track moderation decision

    Args:
        is_blocked: Whether response was blocked
        is_flagged: Whether response was flagged
        region: User region
    """
    if is_blocked:
        decision = 'blocked'
    elif is_flagged:
        decision = 'flagged'
    else:
        decision = 'allowed'

    moderation_responses_total.labels(decision=decision, region=region).inc()


def track_false_positive(rule_type: str, region: str):
    """Track a false positive"""
    moderation_false_positives.labels(rule_type=rule_type, region=region).inc()
    logger.info(f"False positive recorded: {rule_type} in {region}")


def track_true_positive(rule_type: str, region: str):
    """Track a true positive"""
    moderation_true_positives.labels(rule_type=rule_type, region=region).inc()


def calculate_and_update_fpr(rule_type: str, time_window: str = '24h'):
    """
    Calculate and update false positive rate gauge

    Args:
        rule_type: Type of rule
        time_window: Time window for calculation (1h, 24h, 7d)
    """
    # This would typically query metrics from Prometheus or a database
    # For now, we'll update the gauge when called with calculated values
    # In production, this should be called periodically by a background task
    pass


logger.info("Prometheus metrics initialized")

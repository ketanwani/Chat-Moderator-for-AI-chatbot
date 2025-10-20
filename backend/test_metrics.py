"""
Test script for Prometheus metrics integration

This script tests:
1. Metrics endpoint availability
2. Metrics collection during chat requests
3. SLA tracking and violations
4. Interception tracking
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"


def test_health_check():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)

    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200, "Health check failed"
    print("✓ Health check passed")


def test_metrics_endpoint():
    """Test that metrics endpoint is available"""
    print("\n" + "="*60)
    print("Testing Metrics Endpoint")
    print("="*60)

    response = requests.get(f"{BASE_URL}/metrics")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        metrics_text = response.text
        print(f"Metrics response length: {len(metrics_text)} characters")
        print("\nSample metrics (first 500 chars):")
        print(metrics_text[:500])
        print("✓ Metrics endpoint is working")
        return metrics_text
    else:
        print("✗ Metrics endpoint failed")
        return None


def test_chat_and_metrics():
    """Test chat endpoint and verify metrics are collected"""
    print("\n" + "="*60)
    print("Testing Chat with Metrics Collection")
    print("="*60)

    # Test 1: Normal safe message
    print("\n1. Testing safe message...")
    chat_payload = {
        "message": "Hello, how are you?",
        "region": "US",
        "session_id": "test-session-1"
    }

    response = requests.post(f"{BASE_URL}{API_PREFIX}/chat", json=chat_payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Test 2: Message that triggers PII detection
    print("\n2. Testing PII detection...")
    chat_payload = {
        "message": "What is pii?",
        "region": "US",
        "session_id": "test-session-2"
    }

    response = requests.post(f"{BASE_URL}{API_PREFIX}/chat", json=chat_payload)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Is Moderated: {result.get('is_moderated')}")
    if result.get('moderation_info'):
        print(f"Moderation Info: {json.dumps(result['moderation_info'], indent=2)}")

    # Test 3: Message that triggers toxicity detection
    print("\n3. Testing toxicity detection...")
    chat_payload = {
        "message": "Say something toxic",
        "region": "US",
        "session_id": "test-session-3"
    }

    response = requests.post(f"{BASE_URL}{API_PREFIX}/chat", json=chat_payload)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Is Moderated: {result.get('is_moderated')}")
    if result.get('moderation_info'):
        print(f"Moderation Info: {json.dumps(result['moderation_info'], indent=2)}")

    print("\n✓ Chat requests completed")


def analyze_metrics():
    """Fetch and analyze metrics"""
    print("\n" + "="*60)
    print("Analyzing Collected Metrics")
    print("="*60)

    response = requests.get(f"{BASE_URL}/metrics")
    if response.status_code != 200:
        print("✗ Could not fetch metrics")
        return

    metrics_text = response.text
    lines = metrics_text.split('\n')

    # Filter and display relevant metrics
    print("\n--- Moderation Latency Metrics ---")
    for line in lines:
        if 'moderation_latency' in line and not line.startswith('#'):
            print(line)

    print("\n--- SLA Violation Metrics ---")
    for line in lines:
        if 'moderation_sla_violations' in line and not line.startswith('#'):
            print(line)

    print("\n--- Request Count Metrics ---")
    for line in lines:
        if 'moderation_requests_total' in line and not line.startswith('#'):
            print(line)

    print("\n--- Interception Metrics ---")
    for line in lines:
        if 'moderation_interception_total' in line and not line.startswith('#'):
            print(line)

    print("\n--- Response Decision Metrics ---")
    for line in lines:
        if 'moderation_responses_total' in line and not line.startswith('#'):
            print(line)

    print("\n--- Rule Trigger Metrics ---")
    for line in lines:
        if 'moderation_rules_triggered' in line and not line.startswith('#'):
            print(line)

    print("\n--- Chatbot Response Time ---")
    for line in lines:
        if 'chatbot_response_seconds' in line and not line.startswith('#'):
            print(line)

    print("\n✓ Metrics analysis complete")


def calculate_sla_compliance():
    """Calculate SLA compliance from metrics"""
    print("\n" + "="*60)
    print("SLA Compliance Analysis")
    print("="*60)

    response = requests.get(f"{BASE_URL}/metrics")
    if response.status_code != 200:
        print("✗ Could not fetch metrics")
        return

    metrics_text = response.text
    lines = metrics_text.split('\n')

    # Parse metrics
    total_requests = 0
    sla_violations = 0

    for line in lines:
        if 'moderation_requests_total' in line and 'status="success"' in line:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    total_requests += float(parts[-1])
                except ValueError:
                    pass

        if 'moderation_sla_violations_total' in line and not line.startswith('#'):
            parts = line.split()
            if len(parts) >= 2:
                try:
                    sla_violations += float(parts[-1])
                except ValueError:
                    pass

    if total_requests > 0:
        compliance_rate = ((total_requests - sla_violations) / total_requests) * 100
        print(f"Total Requests: {total_requests}")
        print(f"SLA Violations: {sla_violations}")
        print(f"SLA Compliance: {compliance_rate:.2f}%")
        print(f"Target: 99% (< 100ms)")

        if compliance_rate >= 99:
            print("✓ SLA target met!")
        else:
            print("⚠ SLA target not met")
    else:
        print("No requests processed yet")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("PROMETHEUS METRICS TEST SUITE")
    print("="*60)
    print("\nNOTE: Make sure the backend server is running on http://localhost:8000")
    print("Start it with: python main.py or uvicorn main:app --reload")

    input("\nPress Enter to start tests...")

    try:
        # Run tests
        test_health_check()
        test_metrics_endpoint()
        test_chat_and_metrics()
        time.sleep(1)  # Give metrics time to update
        analyze_metrics()
        calculate_sla_compliance()

        print("\n" + "="*60)
        print("TEST SUITE COMPLETED")
        print("="*60)
        print("\nYou can view metrics at: http://localhost:8000/metrics")
        print("For continuous monitoring, set up Prometheus to scrape this endpoint")

    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to server at", BASE_URL)
        print("Please ensure the backend is running with: python main.py")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")


if __name__ == "__main__":
    main()

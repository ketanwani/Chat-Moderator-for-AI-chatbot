"""
Simple API test script to validate the moderation system
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def print_test(name, passed):
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status} - {name}")

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        passed = response.status_code == 200 and response.json().get("status") == "healthy"
        print_test("Health Check", passed)
        return passed
    except Exception as e:
        print_test(f"Health Check (Error: {e})", False)
        return False

def test_chat_normal_message():
    """Test chat with normal message"""
    try:
        response = requests.post(f"{BASE_URL}/chat", json={
            "message": "Hello, how are you?",
            "region": "global"
        })
        passed = response.status_code == 200
        data = response.json()
        print_test("Chat - Normal Message", passed)
        if passed:
            print(f"  Response: {data['response'][:50]}...")
            print(f"  Moderated: {data['is_moderated']}")
        return passed
    except Exception as e:
        print_test(f"Chat - Normal Message (Error: {e})", False)
        return False

def test_chat_pii_detection():
    """Test PII detection"""
    try:
        response = requests.post(f"{BASE_URL}/chat", json={
            "message": "My email is test@example.com",
            "region": "global"
        })
        passed = response.status_code == 200
        data = response.json()
        print_test("Chat - PII Detection", passed)
        if passed:
            print(f"  Moderated: {data['is_moderated']}")
            if data.get('moderation_info'):
                print(f"  Blocked: {data['moderation_info'].get('blocked')}")
                print(f"  Latency: {data['moderation_info'].get('latency_ms'):.2f}ms")
        return passed
    except Exception as e:
        print_test(f"Chat - PII Detection (Error: {e})", False)
        return False

def test_get_rules():
    """Test getting moderation rules"""
    try:
        response = requests.get(f"{BASE_URL}/admin/rules")
        passed = response.status_code == 200
        rules = response.json()
        print_test("Admin - Get Rules", passed)
        if passed:
            print(f"  Total rules: {len(rules)}")
            active_rules = sum(1 for r in rules if r['is_active'])
            print(f"  Active rules: {active_rules}")
        return passed
    except Exception as e:
        print_test(f"Admin - Get Rules (Error: {e})", False)
        return False

def test_create_rule():
    """Test creating a new rule"""
    try:
        new_rule = {
            "name": "Test Rule",
            "description": "A test moderation rule",
            "rule_type": "keyword",
            "region": "global",
            "patterns": ["testword", "sampleword"],
            "is_active": True,
            "priority": 50
        }
        response = requests.post(f"{BASE_URL}/admin/rules", json=new_rule)
        passed = response.status_code == 201
        print_test("Admin - Create Rule", passed)
        if passed:
            data = response.json()
            print(f"  Created rule ID: {data['id']}")
            return data['id']  # Return ID for cleanup
        return None
    except Exception as e:
        print_test(f"Admin - Create Rule (Error: {e})", False)
        return None

def test_update_rule(rule_id):
    """Test updating a rule"""
    if not rule_id:
        print_test("Admin - Update Rule (Skipped)", False)
        return False

    try:
        response = requests.put(f"{BASE_URL}/admin/rules/{rule_id}", json={
            "is_active": False
        })
        passed = response.status_code == 200
        print_test("Admin - Update Rule", passed)
        return passed
    except Exception as e:
        print_test(f"Admin - Update Rule (Error: {e})", False)
        return False

def test_delete_rule(rule_id):
    """Test deleting a rule"""
    if not rule_id:
        print_test("Admin - Delete Rule (Skipped)", False)
        return False

    try:
        response = requests.delete(f"{BASE_URL}/admin/rules/{rule_id}")
        passed = response.status_code == 204
        print_test("Admin - Delete Rule", passed)
        return passed
    except Exception as e:
        print_test(f"Admin - Delete Rule (Error: {e})", False)
        return False

def test_get_audit_logs():
    """Test getting audit logs"""
    try:
        response = requests.get(f"{BASE_URL}/admin/audit-logs?limit=10")
        passed = response.status_code == 200
        logs = response.json()
        print_test("Admin - Get Audit Logs", passed)
        if passed:
            print(f"  Total logs returned: {len(logs)}")
        return passed
    except Exception as e:
        print_test(f"Admin - Get Audit Logs (Error: {e})", False)
        return False

def test_get_statistics():
    """Test getting statistics"""
    try:
        response = requests.get(f"{BASE_URL}/admin/stats")
        passed = response.status_code == 200
        stats = response.json()
        print_test("Admin - Get Statistics", passed)
        if passed:
            print(f"  Total requests: {stats.get('total_requests', 0)}")
            print(f"  Flagged requests: {stats.get('flagged_requests', 0)}")
            print(f"  Blocked requests: {stats.get('blocked_requests', 0)}")
            print(f"  Avg latency: {stats.get('avg_latency_ms', 0):.2f}ms")

            # Check SLA
            avg_latency = stats.get('avg_latency_ms', 0)
            if avg_latency > 0:
                sla_met = avg_latency < 100
                print(f"  SLA (<100ms): {'✓ MET' if sla_met else '✗ EXCEEDED'}")
        return passed
    except Exception as e:
        print_test(f"Admin - Get Statistics (Error: {e})", False)
        return False

def test_latency():
    """Test moderation latency"""
    try:
        latencies = []
        num_tests = 10

        print(f"\nRunning {num_tests} latency tests...")
        for i in range(num_tests):
            start = time.time()
            response = requests.post(f"{BASE_URL}/chat", json={
                "message": f"Test message {i}",
                "region": "global"
            })
            end = time.time()

            if response.status_code == 200:
                total_latency = (end - start) * 1000
                data = response.json()
                moderation_latency = data.get('moderation_info', {}).get('latency_ms', 0) if data.get('is_moderated') else 0
                latencies.append(moderation_latency if moderation_latency > 0 else total_latency)

        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            max_latency = max(latencies)
            min_latency = min(latencies)

            print(f"\n  Latency Results:")
            print(f"  Average: {avg_latency:.2f}ms")
            print(f"  Min: {min_latency:.2f}ms")
            print(f"  Max: {max_latency:.2f}ms")

            passed = avg_latency < 100
            print_test("Performance - Latency <100ms", passed)
            return passed
        return False
    except Exception as e:
        print_test(f"Performance - Latency (Error: {e})", False)
        return False

def main():
    print("=" * 60)
    print("Real-Time Moderation and Compliance Engine - API Tests")
    print("=" * 60)
    print()

    # Basic tests
    print("Basic API Tests:")
    print("-" * 60)
    test_health_check()
    test_chat_normal_message()
    test_chat_pii_detection()
    print()

    # Admin API tests
    print("Admin API Tests:")
    print("-" * 60)
    test_get_rules()
    rule_id = test_create_rule()
    test_update_rule(rule_id)
    test_delete_rule(rule_id)
    test_get_audit_logs()
    test_get_statistics()
    print()

    # Performance tests
    print("Performance Tests:")
    print("-" * 60)
    test_latency()
    print()

    print("=" * 60)
    print("Test suite completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()

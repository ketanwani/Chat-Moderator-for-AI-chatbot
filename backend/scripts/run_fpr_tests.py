#!/usr/bin/env python3
"""
False Positive Rate (FPR) Testing Suite

This script tests the moderation system against a labeled dataset to calculate:
- False Positive Rate (FPR): Clean samples incorrectly flagged
- False Negative Rate (FNR): Harmful samples that weren't flagged
- True Positive Rate (TPR): Harmful samples correctly flagged
- True Negative Rate (TNR): Clean samples correctly allowed

Usage:
    python scripts/run_fpr_tests.py
    python scripts/run_fpr_tests.py --update-metrics  # Also update Prometheus
    python scripts/run_fpr_tests.py --report-only     # Generate report from last run
"""

import json
import sys
import os
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.moderation_service import moderation_service
from app.db.base import SessionLocal
from app.models.moderation_rule import Region


class FPRTester:
    """False Positive Rate testing suite"""

    def __init__(self, test_data_dir: str = "test_data"):
        self.test_data_dir = Path(__file__).parent.parent / test_data_dir
        self.results_dir = Path(__file__).parent.parent / "test_results"
        self.results_dir.mkdir(exist_ok=True)

        self.clean_samples = []
        self.harmful_samples = []

        # Results
        self.true_positives = []   # Harmful samples correctly flagged
        self.false_positives = []  # Clean samples incorrectly flagged
        self.true_negatives = []   # Clean samples correctly allowed
        self.false_negatives = []  # Harmful samples that slipped through

    def load_test_data(self):
        """Load clean and harmful sample datasets"""
        print("📁 Loading test data...")

        # Load clean samples
        clean_file = self.test_data_dir / "clean_samples.json"
        if clean_file.exists():
            with open(clean_file, 'r') as f:
                data = json.load(f)
                self.clean_samples = data['samples']
                print(f"  ✅ Loaded {len(self.clean_samples)} clean samples")
        else:
            print(f"  ⚠️  No clean_samples.json found at {clean_file}")

        # Load harmful samples
        harmful_file = self.test_data_dir / "harmful_samples.json"
        if harmful_file.exists():
            with open(harmful_file, 'r') as f:
                data = json.load(f)
                self.harmful_samples = data['samples']
                print(f"  ✅ Loaded {len(self.harmful_samples)} harmful samples")
        else:
            print(f"  ⚠️  No harmful_samples.json found at {harmful_file}")

        total = len(self.clean_samples) + len(self.harmful_samples)
        print(f"📊 Total test samples: {total}\n")

    def test_sample(self, sample: Dict, db, is_harmful: bool) -> Tuple[bool, Dict]:
        """
        Test a single sample through moderation

        Returns:
            (was_flagged, moderation_result)
        """
        try:
            result = moderation_service.moderate_response(
                user_message="Test message",
                bot_response=sample['message'],
                region=Region.GLOBAL,
                db=db,
                session_id=f"fpr_test_{sample['id']}"
            )

            was_flagged = result.is_flagged

            return was_flagged, {
                'is_flagged': result.is_flagged,
                'is_blocked': result.is_blocked,
                'flagged_rules': result.flagged_rules,
                'latency_ms': result.latency_ms
            }

        except Exception as e:
            print(f"    ❌ Error testing sample {sample['id']}: {e}")
            return False, {'error': str(e)}

    def run_tests(self):
        """Run all tests and categorize results"""
        print("🧪 Running moderation tests...\n")

        db = SessionLocal()

        try:
            # Test clean samples (should NOT be flagged)
            print(f"Testing {len(self.clean_samples)} clean samples (expecting ALLOW)...")
            for i, sample in enumerate(self.clean_samples, 1):
                if i % 10 == 0:
                    print(f"  Progress: {i}/{len(self.clean_samples)}")

                was_flagged, result = self.test_sample(sample, db, is_harmful=False)

                if was_flagged:
                    # FALSE POSITIVE: Clean sample was flagged (BAD!)
                    self.false_positives.append({
                        **sample,
                        'moderation_result': result
                    })
                else:
                    # TRUE NEGATIVE: Clean sample was allowed (GOOD!)
                    self.true_negatives.append({
                        **sample,
                        'moderation_result': result
                    })

            print(f"  ✅ Completed clean samples\n")

            # Test harmful samples (SHOULD be flagged)
            print(f"Testing {len(self.harmful_samples)} harmful samples (expecting FLAG/BLOCK)...")
            for i, sample in enumerate(self.harmful_samples, 1):
                if i % 10 == 0:
                    print(f"  Progress: {i}/{len(self.harmful_samples)}")

                was_flagged, result = self.test_sample(sample, db, is_harmful=True)

                if was_flagged:
                    # TRUE POSITIVE: Harmful sample was flagged (GOOD!)
                    self.true_positives.append({
                        **sample,
                        'moderation_result': result
                    })
                else:
                    # FALSE NEGATIVE: Harmful sample slipped through (BAD!)
                    self.false_negatives.append({
                        **sample,
                        'moderation_result': result
                    })

            print(f"  ✅ Completed harmful samples\n")

        finally:
            db.close()

    def calculate_metrics(self) -> Dict:
        """Calculate FPR, FNR, TPR, TNR, and other metrics"""
        tp = len(self.true_positives)
        fp = len(self.false_positives)
        tn = len(self.true_negatives)
        fn = len(self.false_negatives)

        total = tp + fp + tn + fn

        # Calculate rates
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0  # False Positive Rate
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0  # False Negative Rate
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0  # True Positive Rate (Recall)
        tnr = tn / (tn + fp) if (tn + fp) > 0 else 0  # True Negative Rate (Specificity)

        # Additional metrics
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        accuracy = (tp + tn) / total if total > 0 else 0
        f1_score = 2 * (precision * tpr) / (precision + tpr) if (precision + tpr) > 0 else 0

        return {
            'timestamp': datetime.now().isoformat(),
            'total_samples': total,
            'confusion_matrix': {
                'true_positives': tp,
                'false_positives': fp,
                'true_negatives': tn,
                'false_negatives': fn
            },
            'rates': {
                'false_positive_rate': fpr,
                'false_negative_rate': fnr,
                'true_positive_rate': tpr,
                'true_negative_rate': tnr
            },
            'metrics': {
                'precision': precision,
                'recall': tpr,
                'accuracy': accuracy,
                'f1_score': f1_score
            },
            'target_compliance': {
                'fpr_target': 0.001,  # <0.1%
                'fpr_compliant': fpr < 0.001,
                'fnr_acceptable': fnr < 0.05  # We want to catch at least 95% of harmful content
            }
        }

    def generate_report(self, metrics: Dict):
        """Print detailed test report"""
        print("=" * 70)
        print("📊 FALSE POSITIVE RATE (FPR) TEST REPORT")
        print("=" * 70)
        print()

        print(f"⏰ Test completed at: {metrics['timestamp']}")
        print(f"📝 Total samples tested: {metrics['total_samples']}")
        print()

        print("🎯 CONFUSION MATRIX:")
        cm = metrics['confusion_matrix']
        print(f"  True Positives (TP):  {cm['true_positives']:4d} - Harmful samples correctly flagged ✅")
        print(f"  False Positives (FP): {cm['false_positives']:4d} - Clean samples incorrectly flagged ❌")
        print(f"  True Negatives (TN):  {cm['true_negatives']:4d} - Clean samples correctly allowed ✅")
        print(f"  False Negatives (FN): {cm['false_negatives']:4d} - Harmful samples missed ❌")
        print()

        print("📈 PERFORMANCE METRICS:")
        rates = metrics['rates']
        print(f"  False Positive Rate (FPR): {rates['false_positive_rate']:.4f} ({rates['false_positive_rate']*100:.2f}%)")
        print(f"  False Negative Rate (FNR): {rates['false_negative_rate']:.4f} ({rates['false_negative_rate']*100:.2f}%)")
        print(f"  True Positive Rate (TPR):  {rates['true_positive_rate']:.4f} ({rates['true_positive_rate']*100:.2f}%)")
        print(f"  True Negative Rate (TNR):  {rates['true_negative_rate']:.4f} ({rates['true_negative_rate']*100:.2f}%)")
        print()

        m = metrics['metrics']
        print(f"  Precision: {m['precision']:.4f} ({m['precision']*100:.2f}%)")
        print(f"  Recall:    {m['recall']:.4f} ({m['recall']*100:.2f}%)")
        print(f"  Accuracy:  {m['accuracy']:.4f} ({m['accuracy']*100:.2f}%)")
        print(f"  F1 Score:  {m['f1_score']:.4f}")
        print()

        print("🎯 TARGET COMPLIANCE:")
        tc = metrics['target_compliance']
        fpr_status = "✅ PASS" if tc['fpr_compliant'] else "❌ FAIL"
        fnr_status = "✅ ACCEPTABLE" if tc['fnr_acceptable'] else "⚠️  NEEDS IMPROVEMENT"

        print(f"  FPR Target: <0.1% (0.001)")
        print(f"  FPR Actual: {rates['false_positive_rate']*100:.4f}% - {fpr_status}")
        print()
        print(f"  FNR Target: <5% (0.05)")
        print(f"  FNR Actual: {rates['false_negative_rate']*100:.2f}% - {fnr_status}")
        print()

        # Show false positives if any
        if self.false_positives:
            print("⚠️  FALSE POSITIVES (Clean samples incorrectly flagged):")
            for fp in self.false_positives[:5]:  # Show first 5
                print(f"  - [{fp['id']}] {fp['category']}: {fp['message'][:60]}...")
            if len(self.false_positives) > 5:
                print(f"  ... and {len(self.false_positives) - 5} more")
            print()

        # Show false negatives if any
        if self.false_negatives:
            print("🚨 FALSE NEGATIVES (Harmful samples that slipped through):")
            for fn in self.false_negatives[:5]:  # Show first 5
                print(f"  - [{fn['id']}] {fn['category']}: {fn['message'][:60]}...")
            if len(self.false_negatives) > 5:
                print(f"  ... and {len(self.false_negatives) - 5} more")
            print()

        print("=" * 70)

    def save_results(self, metrics: Dict):
        """Save detailed results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.results_dir / f"fpr_results_{timestamp}.json"

        results = {
            **metrics,
            'detailed_results': {
                'false_positives': self.false_positives,
                'false_negatives': self.false_negatives,
                'true_positives_count': len(self.true_positives),
                'true_negatives_count': len(self.true_negatives)
            }
        }

        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"💾 Results saved to: {filename}")
        print()

    def update_prometheus_metrics(self, metrics: Dict):
        """Update Prometheus metrics with FPR test results via HTTP API"""
        print("📊 Updating Prometheus metrics...")

        try:
            import requests

            fp_count = metrics['confusion_matrix']['false_positives']
            tp_count = metrics['confusion_matrix']['true_positives']

            # Call internal metrics update endpoint
            # We'll increment the counters to reflect test results
            backend_url = "http://localhost:8000/api/v1"

            # Update false positives counter
            for _ in range(fp_count):
                try:
                    requests.post(f"{backend_url}/admin/metrics/fpr/false-positive",
                                 json={"rule_type": "fpr_test", "region": "global"},
                                 timeout=2)
                except:
                    pass

            # Update true positives counter
            for _ in range(tp_count):
                try:
                    requests.post(f"{backend_url}/admin/metrics/fpr/true-positive",
                                 json={"rule_type": "fpr_test", "region": "global"},
                                 timeout=2)
                except:
                    pass

            print(f"  ✅ Updated metrics via API: FP={fp_count}, TP={tp_count}")
            print(f"     FPR: {metrics['rates']['false_positive_rate']*100:.2f}%")
            print(f"  📊 Refresh Grafana to see updated FPR gauge")

        except Exception as e:
            print(f"  ⚠️  Could not update Prometheus metrics via API: {e}")
            print(f"     This is OK - you can still view results in the JSON file")
            print(f"     FPR: {metrics['rates']['false_positive_rate']*100:.2f}%")

        print()


def main():
    parser = argparse.ArgumentParser(description='Run False Positive Rate tests')
    parser.add_argument('--update-metrics', action='store_true',
                       help='Update Prometheus metrics after tests')
    parser.add_argument('--report-only', action='store_true',
                       help='Generate report from last test run only')

    args = parser.parse_args()

    tester = FPRTester()

    if not args.report_only:
        # Run full test suite
        tester.load_test_data()

        if not tester.clean_samples and not tester.harmful_samples:
            print("❌ No test data found. Please create test data files first.")
            sys.exit(1)

        tester.run_tests()
        metrics = tester.calculate_metrics()
        tester.generate_report(metrics)
        tester.save_results(metrics)

        if args.update_metrics:
            tester.update_prometheus_metrics(metrics)
    else:
        # Load and display most recent results
        results_files = sorted(tester.results_dir.glob("fpr_results_*.json"))
        if not results_files:
            print("❌ No previous test results found")
            sys.exit(1)

        latest_file = results_files[-1]
        print(f"📂 Loading results from: {latest_file}\n")

        with open(latest_file, 'r') as f:
            metrics = json.load(f)

        tester.generate_report(metrics)


if __name__ == "__main__":
    main()

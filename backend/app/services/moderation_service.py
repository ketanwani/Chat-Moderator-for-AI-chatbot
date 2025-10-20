import time
import uuid
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.moderation_rule import ModerationRule, RuleType, Region
from app.models.audit_log import AuditLog
from app.services.ml_detector import ml_detector
from app.schemas.moderation import ModerationResult
from app.core.metrics import (
    track_moderation_latency,
    track_moderation_decision,
    moderation_requests_total,
    moderation_rules_triggered,
    rule_execution_time,
    database_query_time,
    ml_inference_time
)
import logging

logger = logging.getLogger(__name__)


class ModerationService:
    """Service for moderating chatbot responses"""

    def __init__(self):
        """Initialize moderation service"""
        self.fallback_messages = {
            "default": "I apologize, but I cannot provide that response. Please rephrase your question.",
            "pii": "I detected potential personal information in the response. For your privacy, I cannot share that.",
            "toxicity": "I apologize, but that response doesn't meet our community guidelines.",
            "financial": "I cannot provide specific financial advice or information on that topic.",
            "medical": "I cannot provide specific medical information. Please consult a healthcare professional."
        }

    def moderate_response(
        self,
        user_message: str,
        bot_response: str,
        region: Region,
        db: Session,
        session_id: Optional[str] = None
    ) -> ModerationResult:
        """
        Moderate a chatbot response

        Args:
            user_message: User's message
            bot_response: Bot's proposed response
            region: User's region
            db: Database session
            session_id: Session ID for tracking

        Returns:
            ModerationResult with moderation decision
        """
        start_time = time.time()
        request_id = str(uuid.uuid4())

        try:
            # Get active rules for the region
            rules = self._get_active_rules(db, region)

            flagged_rules = []
            all_scores = {}
            is_blocked = False

            # Apply each rule
            for rule in rules:
                result = self._apply_rule(rule, bot_response)

                if result["flagged"]:
                    flagged_rules.append({
                        "rule_id": rule.id,
                        "rule_name": rule.name,
                        "rule_type": rule.rule_type.value,
                        "details": result["details"]
                    })

                    # Track rule trigger
                    moderation_rules_triggered.labels(
                        rule_id=str(rule.id),
                        rule_name=rule.name,
                        rule_type=rule.rule_type.value
                    ).inc()

                    # Determine if response should be blocked
                    if result["block"]:
                        is_blocked = True

                # Collect scores
                if "scores" in result:
                    all_scores[rule.name] = result["scores"]

            # Calculate latency
            latency_seconds = time.time() - start_time
            latency_ms = latency_seconds * 1000

            # Track metrics
            track_moderation_latency(latency_seconds, region.value)
            track_moderation_decision(is_blocked, len(flagged_rules) > 0, region.value)
            moderation_requests_total.labels(region=region.value, status='success').inc()

            # Determine final response
            if is_blocked:
                final_response = self._get_fallback_message(flagged_rules)
            else:
                final_response = bot_response
            
            # Create audit log
            self._create_audit_log(
                db=db,
                request_id=request_id,
                user_message=user_message,
                bot_response=bot_response,
                is_flagged=len(flagged_rules) > 0,
                is_blocked=is_blocked,
                flagged_rules=flagged_rules,
                scores=all_scores,
                latency_ms=latency_ms,
                region=region.value,
                final_response=final_response,
                session_id=session_id
            )

            return ModerationResult(
                is_flagged=len(flagged_rules) > 0,
                is_blocked=is_blocked,
                flagged_rules=flagged_rules,
                scores=all_scores,
                latency_ms=latency_ms,
                final_response=final_response
            )

        except Exception as e:
            # Track error
            latency_seconds = time.time() - start_time
            moderation_requests_total.labels(region=region.value, status='error').inc()
            logger.error(f"Error in moderation: {e}")
            raise

    def _get_active_rules(self, db: Session, region: Region) -> List[ModerationRule]:
        """Get active rules for a region, sorted by priority"""
        start_time = time.time()

        rules = db.query(ModerationRule).filter(
            ModerationRule.is_active == True,
            (ModerationRule.region == region) | (ModerationRule.region == Region.GLOBAL)
        ).order_by(ModerationRule.priority.desc()).all()

        # Track database query time
        database_query_time.labels(query_type='get_active_rules').observe(time.time() - start_time)

        return rules

    def _apply_rule(self, rule: ModerationRule, text: str) -> Dict[str, Any]:
        """Apply a single moderation rule"""
        start_time = time.time()

        try:
            if rule.rule_type == RuleType.TOXICITY:
                result = self._check_toxicity(rule, text)
            elif rule.rule_type == RuleType.PII:
                result = self._check_pii(rule, text)
            elif rule.rule_type == RuleType.KEYWORD:
                result = self._check_keywords(rule, text)
            elif rule.rule_type == RuleType.REGEX:
                result = self._check_regex(rule, text)
            elif rule.rule_type == RuleType.FINANCIAL:
                result = self._check_financial(rule, text)
            elif rule.rule_type == RuleType.MEDICAL:
                result = self._check_medical(rule, text)
            else:
                result = {"flagged": False, "block": False, "details": {}}

            # Track rule execution time
            rule_execution_time.labels(rule_type=rule.rule_type.value).observe(time.time() - start_time)

            return result

        except Exception as e:
            logger.error(f"Error applying rule {rule.id}: {e}")
            rule_execution_time.labels(rule_type=rule.rule_type.value).observe(time.time() - start_time)
            return {"flagged": False, "block": False, "details": {"error": str(e)}}

    def _check_toxicity(self, rule: ModerationRule, text: str) -> Dict[str, Any]:
        """Check for toxicity"""
        start_time = time.time()
        result = ml_detector.detect_toxicity(text, rule.threshold or 0.7)
        ml_inference_time.labels(model_type='toxicity').observe(time.time() - start_time)

        flagged = result["is_toxic"]
        return {
            "flagged": flagged,
            "block": flagged,  # Block if toxic
            "scores": result["scores"],
            "details": result
        }

    def _check_pii(self, rule: ModerationRule, text: str) -> Dict[str, Any]:
        """Check for PII"""
        start_time = time.time()
        result = ml_detector.detect_pii(text)
        ml_inference_time.labels(model_type='pii').observe(time.time() - start_time)

        flagged = result["has_pii"]
        return {
            "flagged": flagged,
            "block": flagged,  # Block if PII detected
            "details": result
        }

    def _check_keywords(self, rule: ModerationRule, text: str) -> Dict[str, Any]:
        """Check for keywords"""
        keywords = rule.patterns or []
        result = ml_detector.detect_keywords(text, keywords, is_regex=False)

        flagged = result["found"]
        return {
            "flagged": flagged,
            "block": flagged,
            "details": result
        }

    def _check_regex(self, rule: ModerationRule, text: str) -> Dict[str, Any]:
        """Check for regex patterns"""
        patterns = rule.patterns or []
        result = ml_detector.detect_keywords(text, patterns, is_regex=True)

        flagged = result["found"]
        return {
            "flagged": flagged,
            "block": flagged,
            "details": result
        }

    def _check_financial(self, rule: ModerationRule, text: str) -> Dict[str, Any]:
        """Check for restricted financial terms using hardcoded list"""
        result = ml_detector.detect_financial_terms(text)

        flagged = result["has_restricted_terms"]
        return {
            "flagged": flagged,
            "block": flagged,
            "details": result
        }

    def _check_medical(self, rule: ModerationRule, text: str) -> Dict[str, Any]:
        """Check for medical terms using hardcoded list (HIPAA compliance)"""
        result = ml_detector.detect_medical_terms(text)

        flagged = result["has_medical_terms"]
        return {
            "flagged": flagged,
            "block": flagged,
            "details": result
        }

    def _get_fallback_message(self, flagged_rules: List[Dict[str, Any]]) -> str:
        """Get appropriate fallback message based on flagged rules"""
        if not flagged_rules:
            return self.fallback_messages["default"]

        # Prioritize specific messages
        rule_types = [rule["rule_type"] for rule in flagged_rules]

        if "pii" in rule_types:
            return self.fallback_messages["pii"]
        elif "toxicity" in rule_types:
            return self.fallback_messages["toxicity"]
        elif "financial" in rule_types:
            return self.fallback_messages["financial"]
        elif "medical" in rule_types:
            return self.fallback_messages["medical"]
        else:
            return self.fallback_messages["default"]

    def _create_audit_log(
        self,
        db: Session,
        request_id: str,
        user_message: str,
        bot_response: str,
        is_flagged: bool,
        is_blocked: bool,
        flagged_rules: List[Dict[str, Any]],
        scores: Dict[str, Any],
        latency_ms: float,
        region: str,
        final_response: str,
        session_id: Optional[str] = None
    ):
        """Create audit log entry"""
        try:
            audit_log = AuditLog(
                request_id=request_id,
                user_message=user_message,
                bot_response=bot_response,
                is_flagged=is_flagged,
                is_blocked=is_blocked,
                flagged_rules=flagged_rules,
                moderation_scores=scores,
                moderation_latency_ms=latency_ms,
                region=region,
                final_response=final_response,
                session_id=session_id
            )
            db.add(audit_log)
            db.commit()
        except Exception as e:
            logger.error(f"Error creating audit log: {e}")
            db.rollback()


# Singleton instance
moderation_service = ModerationService()

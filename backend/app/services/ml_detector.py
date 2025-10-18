import re
from typing import Dict, Any, List
from detoxify import Detoxify
import logging

logger = logging.getLogger(__name__)


class MLDetector:
    """ML-based content detection service"""

    def __init__(self):
        """Initialize ML models"""
        try:
            # Initialize Detoxify model for toxicity detection
            self.toxicity_model = Detoxify('original')
            logger.info("Toxicity model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading toxicity model: {e}")
            self.toxicity_model = None

    def detect_toxicity(self, text: str, threshold: float = 0.7) -> Dict[str, Any]:
        """
        Detect toxicity in text

        Args:
            text: Text to analyze
            threshold: Confidence threshold

        Returns:
            Dictionary with detection results
        """
        try:
            if not self.toxicity_model:
                return {
                    "is_toxic": False,
                    "scores": {},
                    "error": "Model not loaded"
                }

            results = self.toxicity_model.predict(text)

            # Check if any category exceeds threshold
            is_toxic = any(score > threshold for score in results.values())

            return {
                "is_toxic": is_toxic,
                "scores": {k: float(v) for k, v in results.items()},
                "threshold": threshold
            }
        except Exception as e:
            logger.error(f"Error in toxicity detection: {e}")
            return {
                "is_toxic": False,
                "scores": {},
                "error": str(e)
            }

    def detect_pii(self, text: str) -> Dict[str, Any]:
        """
        Detect PII in text using regex patterns

        Args:
            text: Text to analyze

        Returns:
            Dictionary with detection results
        """
        pii_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            "ip_address": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        }

        detected = {}
        found_any = False

        for pii_type, pattern in pii_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                detected[pii_type] = len(matches)
                found_any = True

        return {
            "has_pii": found_any,
            "detected_types": detected,
            "matches": sum(detected.values()) if detected else 0
        }

    def detect_financial_terms(self, text: str, restricted_terms: List[str]) -> Dict[str, Any]:
        """
        Detect restricted financial terms

        Args:
            text: Text to analyze
            restricted_terms: List of restricted terms

        Returns:
            Dictionary with detection results
        """
        text_lower = text.lower()
        found_terms = []

        for term in restricted_terms:
            if term.lower() in text_lower:
                found_terms.append(term)

        return {
            "has_restricted_terms": len(found_terms) > 0,
            "found_terms": found_terms,
            "count": len(found_terms)
        }

    def detect_keywords(self, text: str, keywords: List[str], is_regex: bool = False) -> Dict[str, Any]:
        """
        Detect keywords or regex patterns in text

        Args:
            text: Text to analyze
            keywords: List of keywords or regex patterns
            is_regex: Whether patterns are regex

        Returns:
            Dictionary with detection results
        """
        text_lower = text.lower()
        found = []

        if is_regex:
            for pattern in keywords:
                try:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    if matches:
                        found.append({"pattern": pattern, "matches": matches})
                except re.error as e:
                    logger.error(f"Invalid regex pattern {pattern}: {e}")
        else:
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    found.append(keyword)

        return {
            "found": len(found) > 0,
            "matches": found,
            "count": len(found)
        }


# Singleton instance
ml_detector = MLDetector()

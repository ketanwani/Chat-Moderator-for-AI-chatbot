from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Float, Enum
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class RuleType(str, enum.Enum):
    """Types of moderation rules"""
    PII = "pii"
    TOXICITY = "toxicity"
    HATE_SPEECH = "hate_speech"
    KEYWORD = "keyword"
    REGEX = "regex"
    FINANCIAL = "financial"
    MEDICAL = "medical"


class Region(str, enum.Enum):
    """Supported regions"""
    GLOBAL = "global"
    US = "us"
    EU = "eu"
    UK = "uk"
    APAC = "apac"


class ModerationRule(Base):
    """Model for storing moderation rules"""
    __tablename__ = "moderation_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    rule_type = Column(Enum(RuleType), nullable=False, index=True)
    region = Column(Enum(Region), nullable=False, index=True, default=Region.GLOBAL)

    # Rule configuration
    patterns = Column(JSON, nullable=True)  # List of keywords or regex patterns
    threshold = Column(Float, nullable=True, default=0.7)  # Confidence threshold for ML models
    config = Column(JSON, nullable=True)  # Additional configuration

    # Status
    is_active = Column(Boolean, default=True, index=True)
    priority = Column(Integer, default=0)  # Higher priority rules are checked first

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

    def __repr__(self):
        return f"<ModerationRule {self.name} ({self.rule_type.value})>"

from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Float, Text
from sqlalchemy.sql import func
from app.db.base import Base


class AuditLog(Base):
    """Model for storing audit logs of moderation decisions"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Request information
    request_id = Column(String, nullable=False, index=True, unique=True)
    user_message = Column(Text, nullable=True)
    bot_response = Column(Text, nullable=False)

    # Moderation result
    is_flagged = Column(Boolean, nullable=False, index=True)
    is_blocked = Column(Boolean, nullable=False, index=True)
    flagged_rules = Column(JSON, nullable=True)  # List of rules that flagged this response

    # Moderation details
    moderation_scores = Column(JSON, nullable=True)  # Detailed scores from ML models
    moderation_latency_ms = Column(Float, nullable=True)
    region = Column(String, nullable=True, index=True)

    # Final response
    final_response = Column(Text, nullable=True)  # Response sent to user (original or fallback)

    # Metadata
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    client_ip = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    session_id = Column(String, nullable=True, index=True)

    def __repr__(self):
        return f"<AuditLog {self.request_id} - Flagged: {self.is_flagged}>"

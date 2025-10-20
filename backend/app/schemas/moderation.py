from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.moderation_rule import RuleType, Region


class ModerationRuleBase(BaseModel):
    """Base schema for moderation rules"""
    name: str = Field(..., description="Name of the rule")
    description: Optional[str] = Field(None, description="Description of the rule")
    rule_type: RuleType = Field(..., description="Type of moderation rule")
    region: Region = Field(Region.GLOBAL, description="Region where this rule applies")
    patterns: Optional[List[str]] = Field(None, description="List of keywords or regex patterns")
    threshold: Optional[float] = Field(0.7, description="Confidence threshold (0-1)", ge=0, le=1)
    config: Optional[Dict[str, Any]] = Field(None, description="Additional configuration")
    is_active: bool = Field(True, description="Whether the rule is active")
    priority: int = Field(0, description="Priority (higher = checked first)")


class ModerationRuleCreate(ModerationRuleBase):
    """Schema for creating a moderation rule"""
    created_by: Optional[str] = None


class ModerationRuleUpdate(BaseModel):
    """Schema for updating a moderation rule"""
    name: Optional[str] = None
    description: Optional[str] = None
    rule_type: Optional[RuleType] = None
    region: Optional[Region] = None
    patterns: Optional[List[str]] = None
    threshold: Optional[float] = Field(None, ge=0, le=1)
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None
    updated_by: Optional[str] = None


class ModerationRuleResponse(ModerationRuleBase):
    """Schema for moderation rule response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: Optional[str]
    updated_by: Optional[str]

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """Schema for chat request"""
    message: str = Field(..., description="User message")
    region: Optional[Region] = Field(Region.GLOBAL, description="User's region")
    session_id: Optional[str] = Field(None, description="Session ID for tracking")
    llm_provider: Optional[str] = Field("mock", description="LLM provider: openai, anthropic, ollama, or mock")


class ChatResponse(BaseModel):
    """Schema for chat response"""
    response: str = Field(..., description="Chatbot response")
    request_id: str = Field(..., description="Unique request ID")
    is_moderated: bool = Field(..., description="Whether the response was moderated")
    moderation_info: Optional[Dict[str, Any]] = Field(None, description="Moderation details")


class AuditLogResponse(BaseModel):
    """Schema for audit log response"""
    id: int
    request_id: str
    user_message: Optional[str]
    bot_response: str
    is_flagged: bool
    is_blocked: bool
    flagged_rules: Optional[List[Dict[str, Any]]]
    moderation_scores: Optional[Dict[str, Any]]
    moderation_latency_ms: Optional[float]
    region: Optional[str]
    final_response: Optional[str]
    timestamp: datetime
    session_id: Optional[str]

    class Config:
        from_attributes = True


class ModerationResult(BaseModel):
    """Internal schema for moderation results"""
    is_flagged: bool
    is_blocked: bool
    flagged_rules: List[Dict[str, Any]]
    scores: Dict[str, Any]
    latency_ms: float
    final_response: str

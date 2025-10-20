from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.base import get_db
from app.models.moderation_rule import ModerationRule, RuleType, Region
from app.models.audit_log import AuditLog
from app.schemas.moderation import (
    ModerationRuleCreate,
    ModerationRuleUpdate,
    ModerationRuleResponse,
    AuditLogResponse
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/rules", response_model=List[ModerationRuleResponse])
async def get_rules(
    rule_type: Optional[RuleType] = None,
    region: Optional[Region] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all moderation rules with optional filtering"""
    try:
        query = db.query(ModerationRule)

        if rule_type:
            query = query.filter(ModerationRule.rule_type == rule_type)
        if region:
            query = query.filter(ModerationRule.region == region)
        if is_active is not None:
            query = query.filter(ModerationRule.is_active == is_active)

        rules = query.order_by(ModerationRule.priority.desc()).all()
        return rules

    except Exception as e:
        logger.error(f"Error fetching rules: {e}")
        raise HTTPException(status_code=500, detail="Error fetching rules")


@router.get("/rules/{rule_id}", response_model=ModerationRuleResponse)
async def get_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific moderation rule by ID"""
    rule = db.query(ModerationRule).filter(ModerationRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.post("/rules", response_model=ModerationRuleResponse, status_code=201)
async def create_rule(
    rule: ModerationRuleCreate,
    db: Session = Depends(get_db)
):
    """Create a new moderation rule"""
    try:
        db_rule = ModerationRule(**rule.model_dump())
        db.add(db_rule)
        db.commit()
        db.refresh(db_rule)
        return db_rule

    except Exception as e:
        logger.error(f"Error creating rule: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating rule")


@router.put("/rules/{rule_id}", response_model=ModerationRuleResponse)
async def update_rule(
    rule_id: int,
    rule_update: ModerationRuleUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing moderation rule"""
    try:
        db_rule = db.query(ModerationRule).filter(ModerationRule.id == rule_id).first()
        if not db_rule:
            raise HTTPException(status_code=404, detail="Rule not found")

        # Update fields
        update_data = rule_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_rule, field, value)

        db.commit()
        db.refresh(db_rule)
        return db_rule

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating rule: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating rule")


@router.delete("/rules/{rule_id}", status_code=204)
async def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """Delete a moderation rule"""
    try:
        db_rule = db.query(ModerationRule).filter(ModerationRule.id == rule_id).first()
        if not db_rule:
            raise HTTPException(status_code=404, detail="Rule not found")

        db.delete(db_rule)
        db.commit()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting rule: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting rule")


@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    is_flagged: Optional[bool] = None,
    is_blocked: Optional[bool] = None,
    region: Optional[str] = None,
    session_id: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get audit logs with optional filtering"""
    try:
        query = db.query(AuditLog)

        if is_flagged is not None:
            query = query.filter(AuditLog.is_flagged == is_flagged)
        if is_blocked is not None:
            query = query.filter(AuditLog.is_blocked == is_blocked)
        if region:
            query = query.filter(AuditLog.region == region)
        if session_id:
            query = query.filter(AuditLog.session_id == session_id)

        logs = query.order_by(AuditLog.timestamp.desc()).offset(offset).limit(limit).all()
        return logs

    except Exception as e:
        logger.error(f"Error fetching audit logs: {e}")
        raise HTTPException(status_code=500, detail="Error fetching audit logs")


@router.get("/audit-logs/{request_id}", response_model=AuditLogResponse)
async def get_audit_log(
    request_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific audit log by request ID"""
    log = db.query(AuditLog).filter(AuditLog.request_id == request_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return log


@router.get("/stats")
async def get_stats(
    db: Session = Depends(get_db)
):
    """Get moderation statistics

    Note: Audit logs only contain flagged responses (as per requirements).
    For total request counts, use Prometheus metrics at /metrics endpoint.
    """
    try:
        # Since audit logs only contain flagged responses now
        flagged_requests = db.query(AuditLog).count()  # All audit logs are flagged
        blocked_requests = db.query(AuditLog).filter(AuditLog.is_blocked == True).count()

        # Average latency (for flagged requests only)
        avg_latency = db.query(AuditLog).with_entities(
            db.func.avg(AuditLog.moderation_latency_ms)
        ).scalar()

        return {
            "total_flagged_requests": flagged_requests,  # Renamed for clarity
            "flagged_requests": flagged_requests,  # Kept for backward compatibility
            "blocked_requests": blocked_requests,
            "block_rate_of_flagged": (blocked_requests / flagged_requests * 100) if flagged_requests > 0 else 0,
            "avg_latency_ms": round(avg_latency, 2) if avg_latency else 0,
            "note": "Audit logs only contain flagged responses. Use /metrics for total request counts."
        }

    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Error fetching statistics")

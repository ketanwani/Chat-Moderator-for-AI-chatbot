from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.moderation import ChatRequest, ChatResponse
from app.services.chatbot_service import chatbot_service
from app.services.moderation_service import moderation_service
from app.core.metrics import (
    moderation_interception_total,
    chatbot_response_time,
    chatbot_errors_total
)
import logging
import time

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Process chat message with moderation

    This endpoint:
    1. Generates a response from the chatbot
    2. Applies moderation rules (100% interception)
    3. Returns the moderated response
    """
    try:
        # Track chatbot response generation time
        chatbot_start = time.time()

        # Generate chatbot response
        bot_response = chatbot_service.generate_response(request.message)

        # Track chatbot performance
        chatbot_provider = chatbot_service.llm_provider
        chatbot_response_time.labels(provider=chatbot_provider).observe(time.time() - chatbot_start)

        # CRITICAL: Apply moderation (must succeed or fail-safe)
        # This ensures 100% interception of responses
        try:
            moderation_result = moderation_service.moderate_response(
                user_message=request.message,
                bot_response=bot_response,
                region=request.region,
                db=db,
                session_id=request.session_id
            )

            # Track successful interception
            moderation_interception_total.labels(intercepted='true').inc()

        except Exception as moderation_error:
            # FAIL-SAFE: If moderation fails, block the response
            logger.critical(f"Moderation failure - blocking response: {moderation_error}")
            moderation_interception_total.labels(intercepted='false').inc()

            return ChatResponse(
                response="I'm temporarily unable to process your request. Please try again in a moment.",
                request_id="error",
                is_moderated=True,
                moderation_info={
                    "error": "moderation_failure",
                    "flagged": True,
                    "blocked": True
                }
            )

        # Build response
        response = ChatResponse(
            response=moderation_result.final_response,
            request_id=str(moderation_result.scores.get("request_id", "unknown")),
            is_moderated=moderation_result.is_flagged,
            moderation_info={
                "flagged": moderation_result.is_flagged,
                "blocked": moderation_result.is_blocked,
                "latency_ms": moderation_result.latency_ms,
                "rules_triggered": len(moderation_result.flagged_rules)
            } if moderation_result.is_flagged else None
        )

        return response

    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        chatbot_errors_total.labels(
            provider=chatbot_service.llm_provider,
            error_type=type(e).__name__
        ).inc()
        raise HTTPException(status_code=500, detail="Error processing request")

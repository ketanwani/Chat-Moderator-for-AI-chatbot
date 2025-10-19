from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.moderation import ChatRequest, ChatResponse
from app.services.chatbot_service import chatbot_service
from app.services.moderation_service import moderation_service
import logging

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
    2. Applies moderation rules
    3. Returns the moderated response
    """
    try:
        # Generate chatbot response        
        bot_response = chatbot_service.generate_response(request.message)

        # Apply moderation
        moderation_result = moderation_service.moderate_response(
            user_message=request.message,
            bot_response=bot_response,
            region=request.region,
            db=db,
            session_id=request.session_id
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
        raise HTTPException(status_code=500, detail="Error processing request")

# app/routers/chat.py

from fastapi import APIRouter, Depends
from .. import schemas, security
from ..chat import get_chatbot_response

router = APIRouter()

@router.post("/query", response_model=schemas.ChatResponse)
def handle_chat_query(
    request: schemas.ChatQuery,
    current_user: dict = Depends(security.get_current_regular_user)
):
    """
    Handles a user's chat query.
    - Requires a valid JWT from any logged-in user.
    - Extracts company_id from the token to ensure data isolation.
    """
    company_id = current_user["company_id"]
    answer = get_chatbot_response(query=request.query, company_id=company_id)
    return schemas.ChatResponse(answer=answer)
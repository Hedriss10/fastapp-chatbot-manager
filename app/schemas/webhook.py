# app/schemas/webhook.py

from typing import Any, Dict

from pydantic import BaseModel


class WebhookPayload(BaseModel):
    data: Dict[str, Any]

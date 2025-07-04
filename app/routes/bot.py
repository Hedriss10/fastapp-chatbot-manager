# app/routes/bot.py

import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from app.core.bot import BotCore
from app.logs.log import setup_logger
from app.schemas.webhook import WebhookPayload
from app.service.redis import SessionManager

log = setup_logger()
load_dotenv()

RATE_COUNT_LIMIT_MESSAGE = int(os.getenv("RATE_COUNT_LIMIT_MESSAGE", "3"))
CLOSES_MESSAGE_REDIS = int(os.getenv("CLOSES_MESSAGE_REDIS", "60"))

bot = APIRouter(
    prefix="/bot",
    tags=["bot"],
)


@bot.post("/webhook", tags=["bot"])
async def webhook(payload: WebhookPayload):
    try:
        session = SessionManager()
        payload_data = payload.data

        if payload_data.get("key", {}).get("fromMe", False):
            log.info("Ignoring message from bot (fromMe: True)")
            return {"status": "ignored", "message": "Message from bot"}

        phone_number = (
            payload_data.get("key", {}).get("remoteJid", "").split("@")[0]
        )
        message_id = payload_data.get("key", {}).get("id", "")
        message_timestamp = payload_data.get("messageTimestamp", 0)
        push_name = payload_data.get("pushName", "Usuário")
        message_data = payload_data.get("message", {})

        if not phone_number or not message_id or not message_timestamp:
            log.error(
                f"Missing phone, id or timestamp: \
                {phone_number}, {message_id}, {message_timestamp}"
            )
            raise HTTPException(
                status_code=400, detail="Missing required fields"
            )

        # Deduplicação
        dedup_key = f"msg:{phone_number}:{message_id}:{message_timestamp}"
        if session.client.get(dedup_key):
            log.info(f"Duplicate message ignored: {message_id}")
            return {"status": "ignored", "message": "Duplicate message"}

        session.client.set(dedup_key, "processed", ex=600)

        # Rate Limiting
        rate_key = f"rate:{phone_number}"
        rate_count = session.client.incr(rate_key)
        if rate_count == 1:
            session.client.expire(rate_key, CLOSES_MESSAGE_REDIS)
        if rate_count > RATE_COUNT_LIMIT_MESSAGE:
            log.warning(f"Rate limit exceeded for {phone_number}")
            raise HTTPException(status_code=429, detail="Too many requests")

        # Texto da mensagem
        message_text = (
            (
                message_data.get("conversation")
                or message_data.get("extendedTextMessage", {}).get("text")
                or ""
            )
            .strip()
            .lower()
        )

        if not message_text:
            log.error(f"No message text from {phone_number}")
            raise HTTPException(status_code=400, detail="No message text")

        BotCore(message_text, phone_number, push_name).send_message()
        return {"status": "success"}

    except HTTPException as e:
        raise e  # Mantém o status_code correto

    except Exception as e:
        log.error(f"Error in webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

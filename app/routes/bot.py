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

bot = APIRouter(prefix="/bot", tags=["bot"])


@bot.post(
    "/webhook",
    response_model=dict,
    summary="Send menssage to bot",
    description="Web hook bot",
)
async def webhook(payload: WebhookPayload):
    try:
        session = SessionManager()
        data = payload.data
        print("coletando o data", data)

        if not data:
            log.error("No payload data received")
            raise HTTPException(status_code=400, detail="Missing 'data' field")

        if data.key and data.key.fromMe:
            log.info("Ignoring message from bot (fromMe: True)")
            return {"status": "ignored", "message": "Message from bot"}

        phone_number = (
            (data.key.remoteJid or "").split("@")[0] if data.key else ""
        )
        message_id = data.key.id if data.key else ""
        message_timestamp = data.messageTimestamp or 0
        push_name = data.pushName or "Usuário"
        message_data = data.message

        if not phone_number or not message_id or not message_timestamp:
            log.error(
                f"Missing key fields: phone={phone_number}, \
                id={message_id}, timestamp={message_timestamp}"
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

        # Rate limiting
        rate_key = f"rate:{phone_number}"
        rate_count = session.client.incr(rate_key)
        if rate_count == 1:
            session.client.expire(rate_key, CLOSES_MESSAGE_REDIS)
        if rate_count > RATE_COUNT_LIMIT_MESSAGE:
            log.warning(f"Rate limit exceeded for {phone_number}")
            raise HTTPException(status_code=429, detail="Too many requests")

        # Extrai texto
        message_text = (
            (
                (message_data.conversation if message_data else None)
                or (
                    message_data.extendedTextMessage.text
                    if message_data and message_data.extendedTextMessage
                    else None
                )
                or ""
            )
            .strip()
            .lower()
        )

        if not message_text:
            log.error(f"No message text found for: {phone_number}")
            raise HTTPException(status_code=400, detail="No message text")

        # Processa a mensagem
        BotCore(message_text, phone_number, push_name).send_message()

        return {"status": "success"}

    except HTTPException as e:
        print("COLETANDO O ERRO DE RETORNO", e)
        raise e
    except Exception as e:
        print("Coletando o errr", e)
        log.error(f"Error in webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

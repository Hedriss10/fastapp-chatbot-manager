# app/service/redis.py

import json
import os
from typing import Any, Optional

import redis

HOST_REDIS = os.getenv("HOST_REDIS", "localhost")
PORT_REDIS = int(os.getenv("PORT_REDIS", "6379"))
DB_REDIS = int(os.getenv("DB_REDIS", "0"))
SOCKE_CONNECT_TIMEOUT = int(os.getenv("SOCKET_CONNECT_TIMEOUT", "5"))


class SessionManager:
    def __init__(self):
        self.client = redis.Redis(
            host=HOST_REDIS,
            port=PORT_REDIS,
            db=DB_REDIS,
            decode_responses=True,
            socket_connect_timeout=SOCKE_CONNECT_TIMEOUT,
        )

    def is_employee(self, phone: str) -> bool:
        """Verifica se o número pertence a um barbeiro"""
        try:
            return self.client.sismember("employees:phones", phone)
        except Exception as e:
            print(f"Redis is_employee error: {e}")
            return False

    def get_pending_confirmation(self, employee_phone: str) -> Optional[dict]:
        """Obtém agendamento pendente de confirmação"""
        try:
            data = self.client.get(f"pending_confirmation:{employee_phone}")
            return json.loads(data) if data else None
        except Exception as e:
            print(f"Redis get_pending_confirmation error: {e}")
            return None

    def get_state(self, phone: str) -> str | None:
        try:
            return self.client.get(f"session:{phone}")
        except Exception as e:
            print(f"Redis get_state error: {e}")
            return None

    def set_state(
        self, phone: str, state: str, expire_seconds: int = 600
    ) -> None:
        try:
            self.client.set(f"session:{phone}", state, ex=expire_seconds)
        except Exception as e:
            print(f"Redis set_state error: {e}")

    def clear(self, phone: str) -> None:
        try:
            self.client.delete(f"session:{phone}")
        except Exception as e:
            print(f"Redis clear error: {e}")

    def reset_to_default(self, phone: str, RESPONSE_DICTIONARY: dict) -> str:
        self.clear(phone)
        return RESPONSE_DICTIONARY.get("default", "Algo deu errado...")

    # Para qualquer chave genérica (employee list, products, etc)
    def set_key(self, key: str, value: Any, expire_seconds: int = 600) -> None:
        try:
            self.client.set(key, json.dumps(value), ex=expire_seconds)
        except Exception as e:
            print(f"Redis set_key error: {e}")

    def get_key(self, key: str) -> Any:
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            print(f"Redis get_key error: {e}")
        return None

    def delete(self, key: str) -> None:
        try:
            self.client.delete(key)
        except Exception as e:
            print(f"Redis delete error: {e}")

    def clear_all(self) -> None:
        """Clear all session, message deduplication, and rate limiting keys."""
        for pattern in ["session:*", "msg:*", "rate:*"]:
            cursor = 0
            while True:
                cursor, keys = self.client.scan(
                    cursor=cursor, match=pattern, count=100
                )
                if keys:
                    self.client.delete(*keys)
                if cursor == 0:
                    break

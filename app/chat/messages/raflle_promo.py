# app/messages/raffle_promo.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.campaign.messages import SummaryMessage

log = setup_logger()


RAFFLE_PROMO = 'raflle_promo'


class RafflePromoCore:
    def __init__(
        self, message: str, sender_number: str, push_name: str, db: Session
    ):
        self.message = message
        self.sender_number = sender_number
        self.push_name = push_name
        self.db = db
        self.message_summary = SummaryMessage

    def get_raffle_promo_info(self) -> str:
        try:
            message_stmt = select(self.message_summary.message).where(
                self.message_summary.ticket == RAFFLE_PROMO
            )
            result_message = self.db.execute(message_stmt).fetchone()
            if not result_message:
                return '⚠️ Promoção de Raffle não está disponível no momento.'

            message_format = result_message[0]['text'].format(
                nome_cliente=self.push_name
            )
            return message_format

        except Exception as e:
            log.error(f'Error getting raffle promo info: {e}')
            return '⚠️ Erro ao obter informações da promoção. Tente novamente mais tarde.'

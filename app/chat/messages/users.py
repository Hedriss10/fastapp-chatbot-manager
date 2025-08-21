# app/messages/users.py

from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.core.log import setup_logger
from app.models.users import User

log = setup_logger()


class UsersCore:
    def __init__(
        self,
        message: str,
        sender_number: str,
        push_name: str,
        db: Session,
        *args,
        **kwargs,
    ):
        self.message = message
        self.sender_number = sender_number
        self.push_name = push_name
        self.db = db

    def add_users(self, lastname: str) -> str:
        try:
            stmt = insert(User).values(
                username=self.push_name,
                lastname=lastname,
                phone=self.sender_number,
            )
            self.db.execute(stmt)
            self.db.commit()
            log.info(f'User {self.sender_number} added successfully.')
            return '✅ Usuário adicionado com sucesso!'
        except Exception as e:
            log.error(f'Error adding user: {e}')
            return '⚠️ Erro ao adicionar usuário. Tente novamente.'

    def check_user_exists(self) -> bool:
        try:
            user = (
                self.db.query(User)
                .filter(User.phone == self.sender_number)
                .first()
            )
            if user:
                log.info(f'User {self.sender_number} already exists.')
                return True
            else:
                log.info(f'User {self.sender_number} does not exist.')
                return False
        except Exception as e:
            log.error(f'Error checking user existence: {e}')
            return False

# app/messages/Products.py


from sqlalchemy import select
from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.employee import Employee
from app.models.messages import SummaryMessage
from app.models.product.product import Products, ProductsEmployees

log = setup_logger()


LIST_PRODUCTS = 'list_products'


class ProductsCore:
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
        self.send_number = sender_number
        self.push_name = push_name
        self.db = db
        self.message = SummaryMessage

    def list_products(self, employee_id: int) -> tuple[str, list[dict]]:
        try:
            stmt = (
                select(
                    Products.id,
                    Products.description,
                    Products.value_operation,
                )
                .select_from(Products)
                .join(
                    ProductsEmployees,
                    ProductsEmployees.product_id == Products.id,
                )
                .join(Employee, Employee.id == ProductsEmployees.employee_id)
                .where(Employee.id == employee_id)
            )

            result = self.db.execute(stmt).fetchall()

            if not result:
                return '⚠️ Nenhum serviço disponível para esse profissional.'

            # Formatar opções de produtos
            produts_list = []
            options_product = ''
            for idx, (prod_id, description, value) in enumerate(
                result, start=1
            ):
                value_formatted = f'R${value:.2f}'.replace('.', ',')
                produts_list.append({
                    'id': prod_id,
                    'description': description,
                })
                options_product += (
                    f'{idx}️⃣ {description} – {value_formatted}  \n'
                )

            # Buscar template do banco
            message_stmt = select(self.message.message).where(
                self.message.ticket == LIST_PRODUCTS
            )

            result_message = self.db.execute(message_stmt).fetchone()

            if not result_message:
                return '⚠️ Nenhuma mensagem configurada para serviços.'

            message_format = result_message[0]['text'].format(
                nome_cliente=self.push_name,
                opcoes_produtos=options_product.strip(),
            )

            return message_format, produts_list

        except Exception as e:
            log.error(f'Logger: error list product {e}')
            return '⚠️ Erro ao listar serviços. Tente novamente mais tarde.'

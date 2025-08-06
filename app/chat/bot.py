import os
from typing import Dict, Optional, Tuple

import httpx
from dotenv import load_dotenv

from app.chat.message import MessagesCore
from app.logs.log import setup_logger
from app.service.redis import SessionManager

load_dotenv()


class BotCore:
    def __init__(
        self, message: str, sender_number: str, push_name: str, *args, **kwargs
    ):
        self.message_text = message.strip()
        self.sender_number = sender_number
        self.push_name = push_name
        self.base_url = os.getenv('URL_INSTANCE_EVOLUTION')
        self.apikey = os.getenv('EVOLUTION_APIKEY')
        self.session = SessionManager()
        self.log = setup_logger()

        self.message_handler = MessagesCore(
            message=self.message_text,
            sender_number=self.sender_number,
            push_name=self.push_name,
        )

    def _reset_session(self, phone: str = None) -> str:
        """Reseta completamente a sessão do usuário"""
        phone = phone or self.sender_number
        try:
            keys = self.session.client.keys(f'*{phone}*')
            if keys:
                self.session.client.delete(*keys)
            return '⚠️ Sua sessão foi reiniciada. \
            Envie qualquer mensagem para começar novamente. 👋'
        except Exception as e:
            self.log.error(f'Error resetting session: {e}')
            return '⚠️ Ocorreu um erro ao reiniciar sua sessão.'

    def _validate_scheduling_data(self) -> Tuple[bool, Optional[Dict]]:
        """Valida e retorna todos os dados do agendamento"""
        keys = [
            'selected_employee_id',
            'selected_product_id',
            'selected_day',
            'selected_slot',
        ]
        data = {}

        for key in keys:
            value = self.session.get_key(f'{self.sender_number}_{key}')
            if value is None:
                return False, None
            data[key] = value

        return True, data

    def _send_message_to_number(self, number: str, message: str) -> bool:
        """Envia mensagem para qualquer número"""
        try:
            payload = {'number': number, 'text': message, 'delay': 2000}
            print(f'Payload: {payload}')
            headers = {
                'apikey': self.apikey,
                'Content-Type': 'application/json',
            }
            response = httpx.post(
                self.base_url, json=payload, headers=headers, timeout=10
            )
            return response.status_code == 201
        except Exception as e:
            self.log.error(f'Error sending message to {number}: {str(e)}')
            return False

    def _notify_employee(
        self, employee_id: str, scheduling_data: Dict
    ) -> bool:
        """Notifica o barbeiro e registra confirmação pendente"""
        try:
            # Obtém telefone e mensagem para o barbeiro
            phone_employee, msg_employee = (
                self.message_handler.approved_service(
                    employee_id=employee_id,
                    product_id=scheduling_data['selected_product_id'],
                    date_selected=scheduling_data['selected_day'],
                    hour_selected=scheduling_data['selected_slot'][0],
                )
            )

            if not phone_employee:
                self.log.error(
                    f'Employee phone not found for ID: {employee_id}'
                )
                return False

            # Registrar o número como barbeiro
            self.session.client.sadd('employees:phones', phone_employee)

            # Registrar a confirmação pendente
            pending_data = {
                'client_phone': self.sender_number,
                'employee_id': employee_id,
                'date': scheduling_data['selected_day'],
                'time': scheduling_data['selected_slot'][0],
                'product_id': scheduling_data['selected_product_id'],
            }
            self.session.set_key(
                f'pending_confirmation:{phone_employee}',
                pending_data,
                3600,  # Expira em 1 hora
            )

            # Enviar a mensagem
            return self._send_message_to_number(phone_employee, msg_employee)
        except Exception as e:
            self.log.error(f'Error in notify_employee: {str(e)}')
            return False

    def _handle_employee_response(self, msg: str) -> Optional[str]:
        """Trata mensagens recebidas de barbeiros"""
        if not self.session.is_employee(self.sender_number):
            return None

        # Verifica se é uma resposta a uma confirmação pendente
        pending = self.session.get_pending_confirmation(self.sender_number)

        if not pending:
            return 'ℹ️ Você é um barbeiro, mas não há agendamentos pendentes para confirmar.'

        # Processa comandos do barbeiro
        clean_msg = msg.lower().strip()
        if clean_msg in ['confirmar', 'sim', 's', 'ok', '1']:
            return self._confirm_scheduling(pending)
        elif clean_msg in ['recusar', 'não', 'nao', 'n', '2']:
            return self._reject_scheduling(pending)
        else:
            return (
                '⚠️ Comando não reconhecido. Por favor responda com:\n\n'
                '1 - Para CONFIRMAR este agendamento\n'
                '2 - Para RECUSAR este agendamento\n\n'
                f'Detalhes do agendamento:\n'
                f'Cliente: {pending.get("client_phone", "N/A")}\n'
                f'Data: {pending.get("date", "N/A")} às {pending.get("time", "N/A")}'
            )

    def _confirm_scheduling(self, scheduling_data: dict) -> str:
        """Confirma o agendamento pelo barbeiro"""
        try:
            client_response = self.message_handler.send_check_service_employee(
                employee_id=scheduling_data.get('employee_id'),
                date_selected=scheduling_data.get('date'),
                hour_selected=scheduling_data.get('time'),
            )
            self._send_message_to_number(
                scheduling_data['client_phone'], client_response
            )
            self.message_handler.send_update_schedule(
                send_number=scheduling_data['client_phone']
            )
            self.session.delete(f'pending_confirmation:{self.sender_number}')
            self._reset_session(scheduling_data['client_phone'])

            return '✅ Agendamento confirmado com sucesso! O cliente foi notificado.'

        except Exception as e:
            self.log.error(f'Error confirming scheduling: {str(e)}')
            return '⚠️ Erro ao confirmar agendamento. Tente novamente.'

    def _reject_scheduling(self, scheduling_data: dict) -> str:
        """Recusa o agendamento pelo barbeiro"""
        try:
            # 1. Atualiza o status no banco de dados

            # 2. Notifica o cliente com opções alternativas
            client_response = (
                '⚠️ O barbeiro não pode atender no horário agendado.\n\n'
                'Por favor, inicie um novo agendamento enviando uma mensagem.'
            )
            self._send_message_to_number(
                scheduling_data['client_phone'], client_response
            )

            # 3. Limpa o estado pendente
            self.session.delete(f'pending_confirmation:{self.sender_number}')

            # 4. Reseta completamente a sessão do cliente
            self._reset_session(scheduling_data['client_phone'])

            return '⚠️ Agendamento recusado. O cliente foi notificado e pode tentar um novo horário.'
        except Exception as e:
            self.log.error(f'Logger: reject scheduling: {e}')
            return None

    def get_response(self) -> str:
        """Lida com o fluxo principal de mensagens"""
        try:
            msg = self.message_text.lower().strip()

            # Primeiro verifica se é uma resposta de barbeiro
            employee_response = self._handle_employee_response(msg)
            if employee_response is not None:
                return employee_response
            # Comandos especiais
            if msg in ['reset', 'reiniciar']:
                return self._reset_session()

            state = self.session.get_key(f'{self.sender_number}_state')

            # Command to return to the main menu
            if msg == 'menu':
                self._reset_session()
                return self.message_handler.send_welcome()

            # Fluxo inicial
            if state is None:
                self.session.set_key(
                    f'{self.sender_number}_state', 'INICIO', 1800
                )
                return self.message_handler.send_welcome()

            # Máquina de estados principal
            if state == 'INICIO':
                if msg == '1':
                    if self.message_handler.send_check_existing_user():
                        message, employees = (
                            self.message_handler.send_list_employee()
                        )
                        if not employees:
                            return '⚠️ Nenhum profissional disponível.'

                        self.session.set_key(
                            f'{self.sender_number}_employees_list',
                            employees,
                            1800,
                        )
                        self.session.set_key(
                            f'{self.sender_number}_state',
                            'ESCOLHER_FUNCIONARIO',
                            1800,
                        )
                        return message

                    else:
                        message = '👥 Por favor, envie seu nome completo *(nome e sobrenome)*'
                        self.session.set_key(
                            f'{self.sender_number}_state',
                            'WAITING_FOR_NAME',
                            1800,
                        )
                        return "👥 Por favor, envie seu nome completo *(nome e sobrenome)*.\n\nDigite 'menu' para voltar ao início."

                if msg == '2':
                    message = self.message_handler.send_opening_hours()

                    if not message:
                        return '⚠️ Horários de funcionamento não disponíveis.'
                    return message

                if msg == '3':
                    employees, message = (
                        self.message_handler.send_barber_info()
                    )

                    if not message:
                        return '⚠️ Falar com atendente não está disponível.'

                    self.session.set_key(
                        f'{self.sender_number}_state', 'ASK_WHICH_BARBER', 1800
                    )
                    self.session.set_key(
                        f'{self.sender_number}_ask_which_barber_employee_id',
                        message,
                        1800,
                    )
                    return employees

                if msg == '4':
                    message = self.message_handler.send_raffle_promo_info()
                    if not message:
                        return '⚠️ Promoção de Raffle não está disponível no momento.'
                    return message

                return 'Por favor, digite alguma opção valida.'

            elif state == 'WAITING_FOR_NAME':
                lastname = self.message_text
                self.message_handler.send_add_user(
                    lastname=lastname,
                )
                self.session.set_key(
                    f'{self.sender_number}_state', 'INICIO', 1800
                )
                return self.message_handler.send_welcome()

            elif state == 'ESCOLHER_FUNCIONARIO':
                employees = self.session.get_key(
                    f'{self.sender_number}_employees_list'
                )
                if employees and msg.isdigit():
                    idx = int(msg) - 1
                    if 0 <= idx < len(employees):
                        employee = employees[idx]
                        self.session.set_key(
                            f'{self.sender_number}_selected_employee_id',
                            employee['id'],
                            1800,
                        )

                        message, products = (
                            self.message_handler.send_list_products_id(
                                employee['id']
                            )
                        )
                        if not products:
                            return '⚠️ Nenhum serviço disponível.'

                        self.session.set_key(
                            f'{self.sender_number}_products_list',
                            products,
                            1800,
                        )
                        self.session.set_key(
                            f'{self.sender_number}_state',
                            'ESCOLHER_PRODUTO',
                            1800,
                        )
                        return message
                return self._reset_session()

            elif state == 'ESCOLHER_PRODUTO':
                products = self.session.get_key(
                    f'{self.sender_number}_products_list'
                )
                if products and msg.isdigit():
                    idx = int(msg) - 1
                    if 0 <= idx < len(products):
                        product = products[idx]
                        self.session.set_key(
                            f'{self.sender_number}_selected_product_id',
                            product['id'],
                            1800,
                        )

                        message, days = (
                            self.message_handler.send_available_days()
                        )
                        if not days:
                            return '⚠️ Nenhuma data disponível.'

                        self.session.set_key(
                            f'{self.sender_number}_available_days', days, 1800
                        )
                        self.session.set_key(
                            f'{self.sender_number}_state', 'ESCOLHER_DIA', 1800
                        )
                        return message
                return self._reset_session()

            elif state == 'ESCOLHER_DIA':
                days = self.session.get_key(
                    f'{self.sender_number}_available_days'
                )
                if days and msg.isdigit():
                    idx = int(msg) - 1
                    if 0 <= idx < len(days):
                        day = days[idx]
                        self.session.set_key(
                            f'{self.sender_number}_selected_day', day, 1800
                        )

                        employee_id = self.session.get_key(
                            f'{self.sender_number}_selected_employee_id'
                        )
                        product_id = self.session.get_key(
                            f'{self.sender_number}_selected_product_id'
                        )

                        message, slots = (
                            self.message_handler.send_available_slots(
                                employee_id, day, product_id
                            )
                        )
                        if not slots:
                            return message

                        serialized_slots = [
                            (s[0].strftime('%H:%M'), s[1].strftime('%H:%M'))
                            for s in slots
                        ]
                        self.session.set_key(
                            f'{self.sender_number}_available_slots',
                            serialized_slots,
                            1800,
                        )
                        self.session.set_key(
                            f'{self.sender_number}_state',
                            'ESCOLHER_HORARIO',
                            1800,
                        )
                        return message
                return self._reset_session()

            elif state == 'ESCOLHER_HORARIO':
                slots = self.session.get_key(
                    f'{self.sender_number}_available_slots'
                )
                if slots and msg.isdigit():
                    idx = int(msg) - 1
                    if 0 <= idx < len(slots):
                        slot = slots[idx]
                        self.session.set_key(
                            f'{self.sender_number}_selected_slot', slot, 1800
                        )
                        self.session.set_key(
                            f'{self.sender_number}_state',
                            'CONFIRMAR_AGENDAMENTO',
                            1800,
                        )
                        return f'⏰ Horário: {slot[0]}. Confirmar agendamento? (sim/não)'
                return self._reset_session()

            elif state == 'CONFIRMAR_AGENDAMENTO':
                if msg in ['sim', 's']:
                    valid, data = self._validate_scheduling_data()
                    if not valid:
                        return '⚠️ Dados incompletos. Reinicie o agendamento.'

                    # Notifica o barbeiro primeiro
                    if not self._notify_employee(
                        data['selected_employee_id'], data
                    ):
                        return (
                            '⚠️ Erro ao notificar o barbeiro. Tente novamente.'
                        )

                    # Mostra confirmação ao cliente
                    self.session.set_key(
                        f'{self.sender_number}_state',
                        'AGENDAMENTO_CONCLUIDO',
                        1800,
                    )
                    print(valid, data)
                    self.message_handler.send_add_schedule(
                        send_number=self.sender_number,
                        employee_id=data['selected_employee_id'],
                        date=data['selected_day'],
                        time=data['selected_slot'][0],
                        product_id=data['selected_product_id'],
                    )
                    return self.message_handler.send_resume_scheduling(
                        employee_id=data['selected_employee_id'],
                        date_selected=data['selected_day'],
                        hour_selected=data['selected_slot'][0],
                        product_id=data['selected_product_id'],
                    )
                else:
                    self.session.set_key(
                        f'{self.sender_number}_state', 'ESCOLHER_HORARIO', 1800
                    )
                    return '🔁 Escolha outro horário:'

            elif state == 'AGENDAMENTO_CONCLUIDO':
                return '✅ Agendamento confirmado! Obrigado.'

            elif state == 'AGENDAMENTO_CONCLUIDO':
                return '✅ Agendamento confirmado! Obrigado.'

            elif state == 'ASK_WHICH_BARBER':
                employees = self.session.get_key(
                    f'{self.sender_number}_ask_which_barber_employee_id'
                )
                if employees and msg.isdigit():
                    idx = int(msg) - 1
                    if 0 <= idx < len(employees):
                        employee = employees[idx]
                        employee_id = employee['id']
                        self.session.set_key(
                            f'{self.sender_number}_selected_employee_id',
                            employee_id,
                            1800,
                        )
                        # Direto para o estado de conexão
                        self.session.set_key(
                            f'{self.sender_number}_state',
                            'FORWARD_TO_BARBER',
                            1800,
                        )
                        # Construir a mensagem de conexão
                        try:
                            connecting_message = (
                                self.message_handler.send_connecting_to_barber(
                                    employee_id=employee_id
                                )
                            )
                            return connecting_message
                        except Exception as e:
                            self.log.error(
                                f'Error get connecting to barber info: {e}'
                            )
                            self._reset_session()
                            return '⚠️ Erro ao conectar com o barbeiro. Tente novamente.'
                    else:
                        self._reset_session()
                        return '⚠️ Opção inválida. Escolha um número da lista de barbeiros.'
                else:
                    return '⚠️ Por favor, digite o número do barbeiro desejado.'

            elif state == 'FORWARD_TO_BARBER':
                employee_id = self.session.get_key(
                    f'{self.sender_number}_selected_employee_id'
                )
                if employee_id:
                    try:
                        response, employee_phone = (
                            self.message_handler.send_forward_to_barber(
                                employee_id=employee_id,
                                type_schedule='padrao',  # Definindo o type_schedule como "padrao"
                            )
                        )
                        if response:
                            # Envia a mensagem para o barbeiro
                            if self._send_message_to_number(
                                employee_phone, response
                            ):
                                return '✅ Mensagem enviada ao barbeiro.'
                            else:
                                return '⚠️ Erro ao enviar mensagem ao barbeiro.'
                        else:
                            return '⚠️ Erro ao obter informações do barbeiro.'
                    except Exception as e:
                        self.log.error(f'Error forwarding to barber: {e}')
                        return '⚠️ Erro ao encaminhar para o barbeiro.'
                return '⚠️ Barbeiro não selecionado. Inicie novamente.'

            return self._reset_session()

        except Exception as e:
            self.log.error(f'Error in get_response: {str(e)}')
            return self._reset_session()

    def send_message(self) -> Optional[httpx.Response]:
        try:
            response_text = self.get_response()

            payload = {
                'number': self.sender_number,
                'text': response_text,
                'delay': 2000,
            }
            headers = {
                'apikey': self.apikey,
                'Content-Type': 'application/json',
            }

            return httpx.post(
                self.base_url, json=payload, headers=headers, timeout=10
            )

        except Exception as e:
            self.log.error(f'Error sending message: {str(e)}')
            return None

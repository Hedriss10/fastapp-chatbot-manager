from sqlalchemy.ext.asyncio import AsyncSession

"""
Todo: Implementar o fluxo de automação do agendamento de serviços

Deve conter todo o funcionamento do atendente do whatsapp

Agendar
Listar barbeiros disponiveis
Listar serviços disponíveis
Listar horários disponíveis
Agendar serviço com confirmação do barbeiro
Deletar serviço

"""


class AutomationCore:
    def __init__(self, session: AsyncSession):
        self.session = session

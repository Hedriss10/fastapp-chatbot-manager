# app/utils/reponse.py

RESPONSE_DICTIONARY = {
    "default": (
        "Olá, seja bem-vindo à nossa barbearia! 💈\n\n"
        "Como posso te ajudar hoje?\n"
        "1️⃣ Quero fazer um agendamento\n"
        "2️⃣ Horários de atendimento\n"
        "3️⃣ Cancelar agendamento\n"
        "4️⃣ Meus agendamentos\n\n"
        "Digite o número da opção desejada"
        "ou envie 'menu' para voltar ao início."
    ),
    "period_selection": (
        "Escolha o período desejado:\n\n"
        "1️⃣ 🌅 Manhã (08:00 - 12:00)\n"
        "2️⃣ ☀️ Tarde (13:00 - 18:00)\n"
        "3️⃣ 🌙 Noite (18:00 - 20:00)\n\n"
        'Digite o número do período\n\n"'
        "ou 'menu' para voltar ao início."
    ),
    "cancelar": (
        "✅ Seus agendamentos ativos:\n\n{agendamentos}\n\n"
        "Por favor, envie o número do agendamento que deseja cancelar.\n\n"
        "Digite 'menu' para voltar ao início."
    ),
    "meus_agendamentos": (
        "Seus agendamentos ativos:\
        \n\n{agendamentos}\n\n"
        "Digite 'menu' para voltar ao início."
    ),
}

TIME_SLOTS_CONFIG = {
    "manha": {
        "label": "🌅 Manhã",
        "period": "08:00 - 12:00",
        "slots": [
            "08:00",
            "08:20",
            "08:40",
            "09:00",
            "09:20",
            "09:40",
            "10:00",
            "10:20",
            "10:40",
            "11:00",
            "11:20",
            "11:40",
        ],
    },
    "tarde": {
        "label": "☀️ Tarde",
        "period": "13:00 - 18:00",
        "slots": [
            "13:00",
            "13:20",
            "13:40",
            "14:00",
            "14:20",
            "14:40",
            "15:00",
            "15:20",
            "15:40",
            "16:00",
            "16:20",
            "16:40",
            "17:00",
            "17:20",
            "17:40",
        ],
    },
    "noite": {
        "label": "🌙 Noite",
        "period": "18:00 - 20:00",
        "slots": ["18:00", "18:20", "18:40", "19:00", "19:20", "19:40"],
    },
}

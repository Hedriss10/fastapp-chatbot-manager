<h1 align="center">Fastapp build chatbot manager</h1>



### Arquitetura do projeto
```textplain
app/
├─ main.py                # instancia app, include_routers, eventos startup/shutdown
├─ core/
│  ├─ config.py           # leitura de env / pydantic settings
│  ├─ logger.py
│  └─ exceptions.py       # exceções customizadas e handlers
├─ db/
│  ├─ base.py             # Base declarative
│  ├─ session.py          # engine + sessão (async ou sync)
│  └─ migrations/         # alembic (fora do pacote app)
├─ api/
│  ├─ v1/
│  │  ├─ routers/
│  │  │  └─ users.py
│  │  └─ deps.py
├─ models/
│  └─ user.py             # SQLAlchemy models
├─ schemas/
│  └─ user.py             # Pydantic request/response DTOs
├─ repositories/
│  └─ user_repo.py
├─ services/
│  └─ user_service.py
├─ tests/
│  └─ unit/, integration/
└─ utils/
   └─ pagination.py

└──────────────┘
```
<h1 align="center">Fastapp build chatbot manager</h1>



### Arquitetura do projeto
```textplain
┌──────────────┐
│   Router     │  → Recebe requisições HTTP (FastAPI)
├──────────────┤
│   Core       │  → Regras de negócio e lógica de uso (ex: UserCore, EmployeeCore)
├──────────────┤
│   Schema     │  → Validação e serialização de dados (Pydantic)
├──────────────┤
│   Model      │  → Mapeamento ORM (SQLAlchemy)
├──────────────┤
│   DB         │  → Conexão e sessão com banco
└──────────────┘
```
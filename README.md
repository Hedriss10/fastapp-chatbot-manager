# Fastapp Chatbot Manager

Bem-vindo ao **Fastapp Chatbot Manager**, uma API RESTful desenvolvida com FastAPI para gerenciar chatbots de maneira eficiente e escalável. Este projeto adota uma arquitetura monolítica modular, com separação clara de responsabilidades entre modelos, serviços, repositórios e rotas, garantindo manutenibilidade e facilidade de extensão.

## Visão Geral

O Fastapp Chatbot Manager permite criar, gerenciar e interagir com chatbots por meio de uma API robusta. Ele utiliza FastAPI para alta performance, SQLAlchemy com suporte a operações assíncronas para acesso ao banco de dados, Alembic para gerenciar migrações e Pydantic para validação de dados. A aplicação é conteinerizável com Docker e inclui testes unitários e de integração.

## Arquitetura do Projeto

A estrutura do projeto segue o padrão de arquitetura limpa, com os seguintes diretórios e arquivos principais:

```plaintext
app/
├── main.py                # Inicializa a aplicação FastAPI, inclui routers e configura eventos de startup/shutdown
├── core/
│   ├── config.py          # Configurações do ambiente usando Pydantic Settings
│   ├── logger.py          # Configuração centralizada de logging
│   └── exceptions.py      # Exceções personalizadas e handlers de erro
├── db/
│   ├── base.py            # Base declarativa para modelos SQLAlchemy
│   ├── session.py         # Configuração de engine e sessões (suporte a async/sync)
│   └── migrations/        # Scripts de migração gerenciados pelo Alembic
├── api/
│   └── v1/
│       ├── routers/
│       │   └── users.py   # Rotas da API para gerenciamento de usuários
│       └── deps.py        # Dependências injetáveis para as rotas
├── models/
│   └── user.py            # Modelos SQLAlchemy para entidades do banco
├── schemas/
│   └── user.py            # Esquemas Pydantic para validação de requests/responses
├── repositories/
│   └── user_repo.py       # Camada de acesso a dados para operações no banco
├── services/
│   └── user_service.py    # Lógica de negócio para operações com usuários
├── tests/
│   ├── unit/              # Testes unitários
│   └── integration/       # Testes de integração
└── utils/
    └── pagination.py      # Utilitários para paginação de resultados

Outros arquivos:
├── alembic.ini            # Configuração do Alembic para migrações
├── CHANGES.md             # Changelog do projeto
├── docker-compose.yml     # Configuração para orquestração com Docker
├── Dockerfile             # Definição do contêiner da aplicação
├── LICENSE                # Licença do projeto
├── pyproject.toml         # Configuração de dependências com Poetry
├── requirements.txt        # Lista de dependências para instalação com pip
├── htmlcov/               # Relatórios de cobertura de testes
├── logs/                  # Diretório para logs da aplicação
└── dev.sh                 # Script auxiliar para desenvolvimento
```

## Pré-requisitos

Para rodar o projeto localmente, você precisará de:

- **Python**: 3.10 ou superior
- **Banco de Dados**: PostgreSQL (recomendado) ou outro compatível com SQLAlchemy
- **Docker**: Opcional, para rodar a aplicação em contêineres
- **Poetry**: Recomendado para gerenciar dependências
- **Git**: Para clonar o repositório

## Configuração do Ambiente

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/fastapp-chatbot-manager.git
   cd fastapp-chatbot-manager
   ```

2. **Crie um ambiente virtual** (opcional se usar Poetry):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:
   Com Poetry (recomendado):
   ```bash
   poetry install
   ```
   Ou com pip:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**:
   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
   ```plaintext
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
   LOG_LEVEL=INFO
   SECRET_KEY=sua-chave-secreta-aqui
   ```
   As variáveis são lidas pelo módulo `app/core/config.py` usando Pydantic Settings.

5. **Aplique as migrações do banco de dados**:
   ```bash
   alembic upgrade head
   ```

## Executando o Projeto

### Localmente com FastAPI
Inicie o servidor de desenvolvimento com Uvicorn:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Acesse a documentação interativa da API em: `http://localhost:8000/docs`.

### Com Docker
Construa e inicie os contêineres:
```bash
docker-compose up --build
```

## Executando Testes

Os testes estão localizados em `app/tests/` e incluem testes unitários e de integração. Para executá-los:

```bash
pytest
```

Para gerar relatórios de cobertura:
```bash
pytest --cov=app --cov-report=html
```
Os relatórios serão salvos no diretório `htmlcov/`.

## Funcionalidades Principais

- **Gerenciamento de Usuários**: Endpoints para criar, listar, atualizar e excluir usuários.
- **Alta Performance**: Suporte a operações assíncronas com FastAPI e SQLAlchemy.
- **Validação Robusta**: Esquemas Pydantic para validação de dados de entrada e saída.
- **Logging Centralizado**: Configuração de logs para monitoramento e depuração.
- **Paginação**: Suporte a paginação para endpoints que retornam grandes conjuntos de dados.
- **Migrações de Banco**: Gerenciamento de esquema com Alembic.

## Contribuindo

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature: `git checkout -b minha-feature`.
3. Commit suas alterações: `git commit -m 'Adiciona minha feature'`.
4. Envie para o repositório remoto: `git push origin minha-feature`.
5. Abra um Pull Request.

Certifique-se de:
- Seguir as convenções de código do projeto.
- Adicionar testes para novas funcionalidades.
- Atualizar o `CHANGES.md` com suas alterações.

## Solução de Problemas

- **Erro de conexão com o banco**: Verifique se o `DATABASE_URL` está correto no arquivo `.env`.
- **Dependências não encontradas**: Certifique-se de que todas as dependências foram instaladas com `poetry install` ou `pip install -r requirements.txt`.
- **Problemas com migrações**: Execute `alembic revision --autogenerate` para criar novas migrações, se necessário.

## Licença

Este projeto está licenciado sob os termos descritos no arquivo `LICENSE`.

## Contato

Para perguntas, sugestões ou suporte, entre em contato com [hedrisgts@gmail.com] ou abra uma issue no repositório.
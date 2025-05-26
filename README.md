# Lu Estilo API

API RESTful desenvolvida para a Lu Estilo, empresa de confecção, com o objetivo de facilitar a comunicação entre o time comercial, clientes e a empresa, além de permitir automação de mensagens via WhatsApp em eventos comerciais.

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como Executar](#como-executar)
  - [Pré-requisitos](#pré-requisitos)
  - [Configuração do Ambiente](#configuração-do-ambiente)
  - [Rodando com Docker](#rodando-com-docker)
  - [Rodando Localmente (sem Docker)](#rodando-localmente-sem-docker)
- [Acesso Admin Padrão](#acesso-admin-padrão)
- [Documentação da API](#documentação-da-api)
- [Testes](#testes)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Observações](#observações)
- [Autor](#autor)

---

## Sobre o Projeto

Esta API foi desenvolvida como parte de um desafio técnico para a Lu Estilo.  
Ela permite o gerenciamento de clientes, produtos, pedidos e integrações automáticas com WhatsApp para notificações comerciais.

---

## Funcionalidades

- **Autenticação JWT** (login, registro, refresh token)
- **Gerenciamento de Clientes** (CRUD, filtros, validação de CPF/email)
- **Gerenciamento de Produtos** (CRUD, filtros por categoria, preço, disponibilidade)
- **Pedidos** (CRUD, múltiplos produtos por pedido, validação de estoque, filtros avançados)
- **Níveis de acesso** (usuário comum e admin)
- **Envio automático de mensagens WhatsApp** para clientes em eventos comerciais (ex: novo pedido)
- **Documentação automática** via Swagger/OpenAPI
- **Testes unitários e de integração** com Pytest
- **Deploy fácil com Docker**

---

## Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pytest](https://docs.pytest.org/)
- [Docker](https://www.docker.com/)
- [UltraMsg API](https://ultramsg.com/) (WhatsApp)
- [Sentry](https://sentry.io/) (monitoramento de erros)

---

## Como Executar

### Pré-requisitos

- Docker e Docker Compose **ou** Python 3.11+, PostgreSQL local e [pipenv](https://pipenv.pypa.io/en/latest/) ou [venv](https://docs.python.org/3/library/venv.html)

### Configuração do Ambiente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/lu-estilo-api.git
   cd lu-estilo-api
   ```

2. **Crie o arquivo `.env` na raiz do projeto:**
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/luestilo
   SECRET_KEY=sua_chave_secreta
   ADMIN_EMAIL=admin@luestilo.com
   ADMIN_PASSWORD=admin123
   WHATSAPP_INSTANCE_ID=seu_instance_id_ultramsg
   WHATSAPP_TOKEN=seu_token_ultramsg
   SENTRY_DSN=sua_dsn_sentry
   ```

### Rodando com Docker

1. **Suba os containers:**
   ```bash
   docker-compose up --build
   ```
2. Acesse a documentação interativa em:  
   [http://localhost:8000/docs](http://localhost:8000/docs)

## 🐳 Deploy com Docker

1. Certifique-se de ter o Docker e Docker Compose instalados.
2. Crie o arquivo `.env` conforme o exemplo.
3. Execute o comando abaixo na raiz do projeto:
   ```bash
   docker-compose up --build
   ```
4. Acesse a documentação da API em [http://localhost:8000/docs](http://localhost:8000/docs)

Para parar os containers:
```bash
docker-compose down
```

### Rodando Localmente (sem Docker)

1. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure o banco de dados e rode as migrações:**
   ```bash
   alembic upgrade head
   ```
4. **Execute a aplicação:**
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 👤 Acesso Admin Padrão

Na primeira vez que a aplicação for executada, um usuário admin será criado automaticamente com os seguintes dados padrão:

- **Email:** admin@luestilo.com
- **Senha:** admin123

Você pode alterar esses valores usando as variáveis de ambiente:
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`

> 🔓 Para facilitar os testes durante o processo seletivo, o sistema está com um usuário admin padrão habilitado.

---

## Documentação da API

Acesse a documentação interativa (Swagger/OpenAPI) em:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## Testes

Execute os testes unitários e de integração com:
```bash
pytest
```

---

## Estrutura do Projeto

```
.
├── alembic/                # Migrações do banco de dados
│   ├── versions/           # Arquivos de versões das migrações
│   ├── env.py
│   ├── README
│   ├── script.py.mako
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── routes/
│   │           ├── __init__.py
│   │           ├── auth.py
│   │           ├── clients.py
│   │           ├── orders.py
│   │           └── products.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   └── security.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── clients.py
│   │   ├── orders.py
│   │   ├── products.py
│   │   └── user.py
│   ├── db/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   ├── orders.py
│   │   │   ├── products.py
│   │   │   └── user.py
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── orders.py
│   │   ├── products.py
│   │   └── user.py
│   ├── services/
│   │   └── whatsapp.py
│   ├── main.py
│   └── startup.py
├── tests/                  # Testes automatizados
├── .env.example            # Exemplo de variáveis de ambiente
├── .gitattributes
├── .gitignore
├── alembic.ini             # Configuração do Alembic
├── pytest.ini              # Configuração do Pytest
├── README.md
├── requirements.txt
```

---

## Variáveis de Ambiente

| Variável                | Descrição                                 | Exemplo                                  |
|------------------------ |-------------------------------------------|------------------------------------------|
| DATABASE_URL            | URL de conexão com o banco PostgreSQL     | postgresql+asyncpg://postgres:postgres@db:5432/luestilo |
| SECRET_KEY              | Chave secreta para JWT                    | sua_chave_secreta                        |
| ADMIN_EMAIL             | Email do admin inicial                    | admin@luestilo.com                       |
| ADMIN_PASSWORD          | Senha do admin inicial                    | admin123                                 |
| WHATSAPP_INSTANCE_ID    | Instance ID do UltraMsg                   | instance123456                           |
| WHATSAPP_TOKEN          | Token do UltraMsg                         | seu_token_ultramsg                       |
| SENTRY_DSN              | DSN do Sentry (opcional)                  | https://...sentry.io/...                  |

---

## Observações

- **Usuários autenticados** (admin ou não) podem criar pedidos.
- **Pedidos** sempre pertencem a um cliente (`client_id`).
- **Admins** podem criar pedidos para qualquer cliente; usuários comuns só para si mesmos.
- O envio de mensagens WhatsApp utiliza a API UltraMsg (fácil integração e plano gratuito para testes).
- O projeto segue boas práticas de arquitetura, validação, tratamento de erros e documentação.
- **Login:** Use seu e-mail no campo `username` ao autenticar.

---

## Autor

Desenvolvido por [Raquel](https://github.com/raquel-brito).

---

> Dúvidas ou sugestões? Abra uma issue ou entre em contato!
# 🛠️ Teste Técnico Back-End - Lu Estilo API

> 💡 **Acesse a API agora:**
>
> - **Produção (Fly.io):** [https://lu-estilo-api-misty-frost-2101.fly.dev/docs](https://lu-estilo-api-misty-frost-2101.fly.dev/)
> - **Docker local:** [http://localhost:8000/docs](http://localhost:8000/)
> - **Ambiente local (sem Docker):** [http://localhost:8000/docs](http://localhost:8000/)
>
> Você pode testar todos os endpoints e a documentação Swagger em qualquer ambiente acima!

Bem-vindo ao repositório do desafio técnico para a Lu Estilo!  
Aqui você encontra uma API RESTful robusta, moderna e pronta para produção, desenvolvida em **Python** com **FastAPI**, **PostgreSQL** e **Docker**.

---

## 👤 Acesso Admin

> **Atenção:** O sistema já inicia com um usuário **admin** padrão para facilitar testes e avaliação.
>
> - **Email:** admin@luestilo.com  
> - **Senha:** admin123  
>
> Você pode alterar esses dados via variáveis de ambiente (`ADMIN_EMAIL`, `ADMIN_PASSWORD`).  
> Apenas admins podem criar outros admins e têm acesso total a todos os recursos.

---

## 📌 Descrição do Desafio

A Lu Estilo, empresa de confecção, busca novas oportunidades de negócio e precisa de uma API para facilitar a comunicação entre o time comercial, clientes e a empresa.  
O objetivo é criar uma API RESTful para gerenciar clientes, produtos e pedidos, além de integrar notificações automáticas via WhatsApp.

---

## 🎯 Funcionalidades

- **Autenticação JWT** (login, registro, refresh token)
- **Níveis de acesso:** admin e usuário comum
- **CRUD completo:** clientes, produtos, pedidos
- **Validação de dados:** email e CPF únicos, estoque, filtros avançados
- **Envio automático de mensagens WhatsApp** (UltraMsg API) em eventos comerciais
- **Documentação automática** (Swagger/OpenAPI)
- **Testes unitários e de integração** (Pytest)
- **Deploy fácil com Docker**

---

## 🔒 Autenticação e Autorização

- JWT para autenticação
- Rotas protegidas para clientes, produtos e pedidos
- **Admin:** pode criar, editar e excluir qualquer recurso, além de criar outros admins
- **Usuário Comum (Autenticado):** pode realizar pedidos, consultar seus próprios pedidos e produtos disponíveis 

---

## 🛣️ Endpoints Principais

### 🔹 Autenticação
- `POST /auth/login` – Login (use seu e-mail como username)
- `POST /auth/register` – Registro de novo usuário
- `POST /auth/refresh-token` – Renovação de token JWT

### 🔹 Clientes
- `GET /clients` – Listar clientes (paginação, filtro por nome/email)
- `POST /clients` – Criar cliente (validação de email e CPF únicos)
- `GET /clients/{id}` – Obter cliente específico
- `PUT /clients/{id}` – Atualizar cliente
- `DELETE /clients/{id}` – Excluir cliente

### 🔹 Produtos
- `GET /products` – Listar produtos (paginação, filtros por categoria, preço, disponibilidade)
- `POST /products` – Criar produto (descrição, valor, código de barras, seção, estoque, validade, imagens)
- `GET /products/{id}` – Obter produto específico
- `PUT /products/{id}` – Atualizar produto
- `DELETE /products/{id}` – Excluir produto

### 🔹 Pedidos
- `GET /orders` – Listar pedidos (filtros: período, seção, id, status, cliente)
- `POST /orders` – Criar pedido (múltiplos produtos, validação de estoque)
- `GET /orders/{id}` – Obter pedido específico
- `PUT /orders/{id}` – Atualizar pedido (incluindo status)
- `DELETE /orders/{id}` – Excluir pedido

---

## 💬 Integração WhatsApp (Desafio Extra)

- Envio automático de mensagens para clientes via UltraMsg API em eventos comerciais, como:
  - Novos pedidos realizados

> As mensagens são disparadas automaticamente pela API, sem necessidade de ação manual do usuário.

---

## 🖥️ Rodando Localmente (sem Docker)

---

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/lu_estilo_api.git
   cd lu_estilo_api
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   # Linux/Mac
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados e rode as migrações:**
   ```bash
   alembic upgrade head
   ```

5. **Execute a aplicação:**
   ```bash
   uvicorn app.main:app --reload
   ```

Acesse a documentação da API em [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🗄️ Banco de Dados

- **PostgreSQL** como banco relacional
- Migrações com **Alembic**
- Índices para performance em campos de busca

---

## 📝 Documentação da API

- Documentação automática via Swagger em  
  [http://localhost:8000/docs](http://localhost:8000/docs)
- Exemplos de requisições e respostas para todos os endpoints
- Descrições detalhadas das regras de negócio

---
## 🖥️ Página de Teste Interativa

Inclui uma página `index.html` para testar rapidamente o fluxo de login, cadastro e visualização do perfil do usuário autenticado.

**Como usar:**
1. Rode a API localmente.
2. Abra o arquivo `index.html` no navegador.
3. Cadastre-se, faça login e clique em "Ver Meu Perfil" para ver seus dados.

> A página faz requisições para `http://localhost:8000`. Certifique-se de que o backend está ativo e o CORS habilitado.

---

## 🧪 Testes

- Testes unitários e de integração com **Pytest**
- Cobertura dos principais fluxos de negócio

A aplicação está preparada para integração com o **Sentry**, permitindo o monitoramento centralizado de erros e exceções em produção.

- Basta configurar a variável de ambiente `SENTRY_DSN` no arquivo `.env` com o seu DSN do Sentry.
- Com isso, qualquer erro crítico será automaticamente reportado para o painel do Sentry, facilitando a identificação e correção de problemas.

Mais informações: [https://sentry.io/for/python/](https://sentry.io/for/python/)

---

## 🚀 Deploy com Docker

1. **Pré-requisitos:** Docker e Docker-Compose instalados
2. **Clone o repositório e configure o `.env`**
3. **Suba os containers:**
   ```bash
   docker-compose up --build
   ```
4. **Acesse a API:**  
   [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🌍 Deploy no Fly.io
A API também está disponível em produção via [Fly.io](https://fly.io/).

- **Acesse a API em produção:**  
  [https://lu-estilo-api-misty-frost-2101.fly.dev/docs]
  (https://lu-estilo-api-misty-frost-2101.fly.dev/)

Você pode testar todos os endpoints e a documentação Swagger diretamente nesse ambiente, sem necessidade de rodar localmente.

> **Observação:** O ambiente de produção pode ter dados de demonstração e ser reiniciado periodicamente.

---

## 📂 Estrutura do Projeto

```
.
├── alembic/                # Migrações do banco de dados
├── app/
│   ├── api/v1/routes/      # Endpoints da API
│   ├── core/               # Configurações, segurança, dependências
│   ├── crud/               # Operações de banco (CRUD)
│   ├── db/                 # Models e sessão do banco
│   ├── schemas/            # Schemas Pydantic
│   ├── services/           # Integrações externas (WhatsApp)
│   ├── main.py             # Entrypoint FastAPI
│   └── startup.py          # Inicialização customizada
├── tests/                  # Testes automatizados
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Variáveis de Ambiente

Para rodar o projeto, é necessário criar um arquivo `.env` na raiz do projeto com base no arquivo `.env.example`.  
O arquivo `.env.example` contém todos os parâmetros necessários, como configurações do banco de dados, credenciais de admin, DSN do Sentry, entre outros.

**Passos:**
1. Copie o arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```
   Ou crie manualmente um novo arquivo `.env` e preencha os campos conforme o `.env.example`.

2. Preencha as variáveis obrigatórias, como:
   - `DATABASE_URL`
   - `ADMIN_EMAIL`
   - `ADMIN_PASSWORD`
   - `SENTRY_DSN` (opcional, para monitoramento de erros)
   - Outras variáveis conforme necessidade do projeto

> **Importante:** Nunca compartilhe seu `.env` real publicamente, pois ele pode conter informações sensíveis.

---

## 📊 Critérios de Avaliação

- **Funcionalidade:** A API atende aos requisitos?
- **Código:** Organização, legibilidade e boas práticas.
- **Documentação:** Clareza e completude.
- **Testes:** Cobertura e qualidade.
- **Deploy:** Docker configurado corretamente.

---

## 🔗 Links úteis

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)
- [UltraMsg API](https://ultramsg.com/)
- [GitHub](https://github.com/)

---

## Autor

Desenvolvido por [Raquel](https://github.com/raquel-brito).

---

> Dúvidas ou sugestões? Abra uma issue ou entre em contato!

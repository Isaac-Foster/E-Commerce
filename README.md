

# E-commerce Boilerplate

Este é um boilerplate para um sistema de **E-commerce** escalável e modular, desenvolvido com **FastAPI**. O projeto utiliza uma arquitetura limpa e modular (Clean Architecture/Hexagonal) para facilitar a manutenção e a evolução do código. Ele é projetado para ser facilmente extensível, com suporte a múltiplos provedores de **armazenamento de mídia** (como Oracle OCI e Amazon S3), **gerenciamento de sessões com Redis**, e integrações com diversos **sistemas de pagamento**.

## Funcionalidades

- Gerenciamento de **produtos** (CRUD)
- Gerenciamento de **categorias de produtos**
- **Carrinho de compras** persistente, com integração de sessão
- **Autenticação e gerenciamento de sessões** com **cookies** e **Redis**
- Armazenamento de imagens de produtos em **Oracle OCI** ou **Amazon S3**
- Integração com múltiplos **sistemas de pagamento** (Gerencianet, PagSeguro, MercadoPago, Asaas, Open Pix, Stripe, Binance, etc.)
- Sistema de **cache** para otimizar performance de consultas e páginas

## Arquitetura

Este projeto foi estruturado com uma organização clara e modular, visando facilitar a manutenção, escalabilidade e performance. Atualmente, a arquitetura segue um modelo inspirado em princípios de **Clean Architecture**, com foco na separação de responsabilidades entre as camadas de **domínio**, **aplicação**, **infraestrutura** e **interface**.

Futuramente, o projeto será reorganizado para seguir uma **Arquitetura Hexagonal**, permitindo uma maior flexibilidade e independência em relação às implementações externas (como bancos de dados, provedores de mídia, gateways de pagamento, etc.).

## Estrutura do Projeto

```
├── config                     # Configuração de ambientes (database, storage, etc)
│   ├── gateway                # Configurações de gateway e microservices (se houver)
│   └── media                  # Configurações de provedores de mídia (OCI, S3, etc)
│       ├── amazon
│       └── oracle
├── ecommerce
│   ├── config.py              # Configuração central do aplicativo
│   ├── database               # Configurações de bancos de dados (Redis, SQL)
│   │   ├── redis.py           # Configuração de Redis (sessão de usuários, cache, etc)
│   │   └── sql.py             # Configuração do banco de dados SQL (ex: PostgreSQL)
│   ├── __main__.py            # Ponto de entrada da aplicação (FastAPI)
│   ├── media                  # Serviços e lógica de upload de mídia (imagens, vídeos)
│   │   ├── __init__.py        # Inicialização dos serviços de mídia
│   │   └── README.md          # Instruções sobre os provedores de mídia (S3, OCI)
│   ├── middleware             # Middlewares da aplicação (autenticação, sessão, etc)
│   │   └── refresh_session.py # Middleware para renovar sessão
│   ├── models                 # Definições de modelos de dados (User, Product, etc)
│   │   ├── admin.py           # Modelos de dados para Admins
│   │   ├── __init__.py        # Arquivo de inicialização
│   │   ├── products.py        # Modelos de dados para Produtos
│   │   └── user.py            # Modelos de dados para Usuários
│   ├── routers                # Definição das rotas da API (Admin, Users, Public)
│   │   ├── admins             # Rotas relacionadas ao painel admin
│   │   │   └── admin.py       # Rotas para admins
│   │   ├── __init__.py        # Arquivo de inicialização das rotas
│   │   ├── public             # Rotas públicas (ex: visualização de produtos)
│   │   └── users              # Rotas relacionadas aos usuários (autenticação, perfil, etc)
│   │       └── user.py        # Rotas para usuários
│   ├── schema                 # Definições dos schemas para validação de dados
│   │   ├── admin              # Schemas para Admins
│   │   ├── products           # Schemas para Produtos
│   │   └── users              # Schemas para Usuários
│   │       └── user.py        # Schemas para usuários
│   ├── static                 # Arquivos estáticos (imagens, CSS)
│   ├── templates              # Templates de HTML (se necessário)
│   ├── utils                  # Funções auxiliares, helpers
│   │   └── __init__.py        # Arquivo de inicialização
│   └── views                  # Visualizações (páginas) para a aplicação
│       ├── __init__.py        # Arquivo de inicialização das views
│       ├── restrict           # Views restritas (Admin, Usuários)
│       │   ├── admins         # Views restritas para Admins
│       │   └── users          # Views restritas para Usuários
│       └── users              # Views públicas para Usuários
├── pyproject.toml             # Dependências do projeto (FastAPI, Redis, OCI, etc)
└── uv.lock                    # Lock do ambiente para garantir reprodutibilidade
```

## Dependências

### Requisitos do Sistema

- Python 3.11 ou superior
- Docker (para rodar o projeto em containers)

### Dependências Python

No arquivo `pyproject.toml` você encontrará todas as dependências necessárias, incluindo:

- `FastAPI` - Framework web
- `Uvicorn` - Servidor ASGI para FastAPI
- `Redis` - Armazenamento em cache e gerenciamento de sessão
- `SQLAlchemy` - ORM para interação com o banco de dados (ex: PostgreSQL)
- `oci` - Biblioteca para interagir com o Oracle OCI
- `boto3` - Cliente AWS SDK para Amazon S3
- `httpx[http2]` - Para integração com APIs externas (como gateways de pagamento)

### Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/ecommerce-boilerplate.git
    cd ecommerce-boilerplate
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

3. Se você for usar Docker, configure o `docker-compose.yaml` para rodar o banco de dados, Redis e outros serviços necessários.

4. Para rodar o servidor localmente:

    ```bash
    uvicorn ecommerce.__main__:app --reload
    ```

    O servidor estará rodando em `http://localhost:8000`.

## Como Contribuir

Se você deseja contribuir para este projeto, siga as etapas abaixo:

1. **Fork** este repositório.
2. Crie uma nova **branch** para suas modificações:
    ```bash
    git checkout -b minha-feature
    ```
3. Faça as mudanças necessárias e **commit**.
4. **Push** para sua branch:
    ```bash
    git push origin minha-feature
    ```
5. Abra um **Pull Request** explicando suas mudanças.


## Roadmap

### Funcionalidades futuras a serem implementadas:

- [ ] Integração com mais gateways de pagamento (ex: Asaas, Open Pix, etc.)
- [ ] Suporte a múltiplas moedas e conversões de preços
- [ ] Funcionalidades avançadas de **recomendações** de produtos (como na Amazon)
- [ ] **API de Notificações** para enviar e-mails ou mensagens de texto para os usuários
- [ ] **Suporte a múltiplos idiomas** (internacionalização)
- [ ] **Sistema de Avaliações e Comentários** para produtos

## Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

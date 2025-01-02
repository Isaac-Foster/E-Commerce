
---

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

Este projeto segue uma arquitetura limpa baseada em **Clean Architecture** e **Arquitetura Hexagonal**. Ele é composto pelas seguintes camadas:

- **Core**: Contém a lógica de negócios (serviços, entidades e repositórios).
- **Infraestrutura**: Implementação de detalhes técnicos (acesso ao banco de dados, cache, armazenamento de mídia, etc.).
- **Interfaces**: Exposição das APIs RESTful e interações com o mundo externo (controllers, rotas).
- **Utilitários**: Funções auxiliares, middlewares e helpers.

## Estrutura do Projeto

```
├── compose.yaml
├── config
│   ├── gateway
│   └── media
│       ├── amazon
│       └── oracle
├── ecommerce
│   ├── adapters
│   ├── config.py
│   ├── core
│   │   ├── domain
│   │   ├── ports
│   │   └── use_cases
│   ├── infrastructure
│   │   ├── database
│   │   └── models
│   ├── interfaces
│   │   ├── middleware
│   │   │   └── refresh_session.py
│   │   ├── routers
│   │   │   ├── admins
│   │   │   ├── __init__.py
│   │   │   ├── public
│   │   │   └── users
│   │   └── services
│   ├── __main__.py
│   ├── schema
│   │   ├── admin
│   │   └── users
│   ├── static
│   ├── templates
│   ├── utils
│   │   └── __init__.py
│   └── views
│       ├── __init__.py
│       ├── restrict
│       │   ├── admins
│       │   └── users
│       └── users
├── pyproject.toml
├── README.md
└── uv.lock
```

### Camadas Principais:

- **Core**: Contém a lógica de negócios e as regras principais da aplicação (como gerenciamento de produtos, carrinho de compras, etc.).
- **Infraestrutura**: Onde as implementações específicas de banco de dados, sessões e armazenamento de mídia (OCI, S3) são feitas.
- **Interfaces**: Onde são definidas as rotas da API (com FastAPI), validações de dados (schemas) e middlewares (como autenticação e segurança).
- **Serviços de Pagamento**: Integração com múltiplos gateways de pagamento, como Gerencianet, PagSeguro, Stripe, MercadoPago, etc.

## Dependências

### Requisitos do Sistema

- Python 3.9 ou superior
- Docker (para rodar o projeto em containers)

### Dependências Python

No arquivo `pyproject.toml` você encontrará todas as dependências necessárias, incluindo:

- `FastAPI` - Framework web
- `Uvicorn` - Servidor ASGI para FastAPI
- `Redis` - Armazenamento em cache e gerenciamento de sessão
- `SQLAlchemy` - ORM para interação com o banco de dados (ex: PostgreSQL)
- `oci` - Biblioteca para interagir com o Oracle OCI
- `boto3` - Cliente AWS SDK para Amazon S3
- `requests` - Para integração com APIs externas (como gateways de pagamento)

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

## Testes

Para garantir a qualidade do código, o projeto inclui testes automatizados. Para rodar os testes, utilize o framework de testes integrado (por exemplo, `pytest`).

Execute os testes com o seguinte comando:

```bash
pytest ecommerce/tests
```

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

Esse **README.md** oferece uma boa base para seu projeto de **e-commerce**, explicando a estrutura de pastas, como rodar o projeto, dependências e como contribuir. Ele também fornece um guia para a modularização do código e como você pode expandir o sistema no futuro.

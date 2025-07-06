# Crypto Dashboard API

## Descrição

API desenvolvida com Flask para:

* Cadastro de usuários e autenticação via sessão (cookies);
* Gerenciamento de cotações de criptomoedas (preço em BRL) usando a API da Binance.

## Instalação

### Pré-requisitos

* Python 3.7 ou superior
* pip
* Git (opcional)

### Passos

1. Clone o repositório:

   ```bash
   git clone https://github.com/seuusuario/mvp-backend.git
   cd mvp-backend
   ```
2. Crie e ative o ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate       # Windows
   ```
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
4. Inicie a API:

   ```bash
   python app.py
   ```

   A aplicação estará disponível em `http://localhost:5000`.

## Endpoints Principais

| Método | Rota                 | Descrição                                       |
| ------ | -------------------- | ----------------------------------------------- |
| POST   | `/cadastrar_usuario` | Registra um novo usuário (nome, email e senha). |
| POST   | `/login`             | Autentica usuário e inicia sessão.              |
| POST   | `/logout`            | Encerra sessão do usuário.                      |
| GET    | `/cryptos`           | Retorna lista de criptomoedas cadastradas.      |
| POST   | `/cryptos`           | Cadastra nova criptomoeda e obtém preço em BRL. |
| POST   | `/cryptos/atualizar` | Atualiza preços de todas as criptomoedas.       |
| DELETE | `/cryptos/{symbol}`  | Remove criptomoeda pelo símbolo (ex: BTC).      |

## Documentação Interativa (Swagger)

Após iniciar o servidor, acesse:

```text
http://localhost:5000/docs
```

para visualizar e testar todas as rotas via interface OpenAPI.

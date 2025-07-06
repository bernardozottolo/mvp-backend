# app.py

import os
import requests
from datetime import datetime

from flask import Flask, request, jsonify, session, send_from_directory
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from models import init_db, get_db

# === Configurações iniciais ===
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
init_db()

API_BINANCE = 'https://api.binance.com/api/v3/ticker/price?symbol={}BRL'


def fetch_price(symbol: str) -> float:
    """Busca o preço da criptomoeda no par SYMBOL-BRL."""
    res = requests.get(API_BINANCE.format(symbol))
    res.raise_for_status()
    return float(res.json()['price'])


# === Rotas de Usuário ===

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()
    hash_pw = bcrypt.generate_password_hash(data['senha']).decode()
    db = get_db()
    cur = db.execute(
        'INSERT INTO usuarios (nome, email, senha_hash) VALUES (?,?,?)',
        (data['nome'], data['email'], hash_pw)
    )
    db.commit()
    return jsonify({'id': cur.lastrowid}), 201


@app.route('/buscar_usuario/<int:id>', methods=['GET'])
def buscar_usuario(id):
    db = get_db()
    user = db.execute(
        'SELECT id, nome, email, criado_em FROM usuarios WHERE id = ?',
        (id,)
    ).fetchone()
    if not user:
        return ('', 404)
    return jsonify(dict(user))


@app.route('/buscar_usuarios', methods=['GET'])
def buscar_usuarios():
    db = get_db()
    rows = db.execute(
        'SELECT id, nome, email, criado_em FROM usuarios'
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route('/deletar_usuario/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    db = get_db()
    db.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    db.commit()
    return ('', 204)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()
    user = db.execute(
        'SELECT * FROM usuarios WHERE email = ?', (data['email'],)
    ).fetchone()
    if user and bcrypt.check_password_hash(user['senha_hash'], data['senha']):
        session['user_id'] = user['id']
        return ('', 204)
    return ('Credenciais inválidas', 401)


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return ('', 204)


# === Rotas de Criptomoedas ===

@app.route('/cryptos', methods=['GET'])
def listar_cryptos():
    if 'user_id' not in session:
        return ('Unauthorized', 401)
    db = get_db()
    rows = db.execute('SELECT symbol, preco, atualizado_em FROM cryptos').fetchall()
    return jsonify([dict(r) for r in rows])


@app.route('/cryptos', methods=['POST'])
def cadastrar_crypto():
    if 'user_id' not in session:
        return ('Unauthorized', 401)
    symbol = request.get_json().get('symbol', '').upper()
    price = fetch_price(symbol)
    now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    db = get_db()
    db.execute(
        'INSERT OR IGNORE INTO cryptos (symbol, preco, atualizado_em) VALUES (?,?,?)',
        (symbol, price, now)
    )
    db.commit()
    return ('', 201)


@app.route('/cryptos/atualizar', methods=['POST'])
def atualizar_precos():
    if 'user_id' not in session:
        return ('Unauthorized', 401)
    db = get_db()
    for row in db.execute('SELECT symbol FROM cryptos').fetchall():
        sym = row['symbol']
        price = fetch_price(sym)
        now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        db.execute(
            'UPDATE cryptos SET preco = ?, atualizado_em = ? WHERE symbol = ?',
            (price, now, sym)
        )
    db.commit()
    return ('', 204)


@app.route('/cryptos/<symbol>', methods=['DELETE'])
def remover_crypto(symbol):
    if 'user_id' not in session:
        return ('Unauthorized', 401)
    db = get_db()
    db.execute('DELETE FROM cryptos WHERE symbol = ?', (symbol.upper(),))
    db.commit()
    return ('', 204)


# === Swagger Spec Route & UI ===

@app.route('/swagger.yaml')
def swagger_spec():
    return send_from_directory(os.path.dirname(__file__), 'swagger.yaml')


SWAGGER_URL = '/docs'
API_URL = '/swagger.yaml'
swagger_ui = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'Crypto Dashboard API'}
)
app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app.run(debug=True)
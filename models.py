# models.py
import sqlite3
import os

# Caminho para o arquivo de banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

def get_db():
    """
    Retorna uma conexão SQLite com row_factory configurada
    para que possamos acessar colunas por nome.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Cria as tabelas 'usuarios' e 'cryptos' caso ainda não existam.
    Deve ser chamado no boot da aplicação.
    """
    db = get_db()
    # Tabela de usuários
    db.execute('''
      CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP
      )
    ''')
    # Tabela de criptomoedas
    db.execute('''
      CREATE TABLE IF NOT EXISTS cryptos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT UNIQUE NOT NULL,
        preco REAL,
        atualizado_em TEXT
      )
    ''')
    db.commit()

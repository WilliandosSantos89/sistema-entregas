import sqlite3
from datetime import date

def conectar():
    return sqlite3.connect("entregas.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS entregas")

    cursor.execute("""
        CREATE TABLE entregas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_pedido TEXT NOT NULL,
            cliente TEXT NOT NULL,
            endereco TEXT NOT NULL,
            horario_previsto TEXT,
            horario_real TEXT,
            status TEXT NOT NULL,
            motivo_atraso TEXT,
            data TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados criado com sucesso.")
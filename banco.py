import sqlite3
from datetime import date, datetime

def conectar():
    return sqlite3.connect("entregas.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entregas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_pedido TEXT NOT NULL,
            cliente TEXT NOT NULL,
            endereco TEXT NOT NULL,
            horario_previsto TEXT,
            horario_real TEXT,
            status TEXT NOT NULL,
            acompanhamento TEXT,
            data TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entrega_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            horario TEXT NOT NULL,
            FOREIGN KEY (entrega_id) REFERENCES entregas(id)
        )
    """)

    conn.commit()
    conn.close()

def gerar_numero_pedido():
    conn = conectar()
    cursor = conn.cursor()
    hoje = date.today().isoformat()
    cursor.execute("SELECT COUNT(*) FROM entregas WHERE data = ?", (hoje,))
    total = cursor.fetchone()[0]
    conn.close()
    return f"ENT-{str(total + 1).zfill(3)}"

def registrar_historico(entrega_id, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historico_status (entrega_id, status, horario)
        VALUES (?, ?, ?)
    """, (entrega_id, status, datetime.now().strftime("%H:%M")))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados criado com sucesso.")
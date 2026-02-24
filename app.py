import tkinter as tk
from tkinter import messagebox, ttk
from banco import conectar, criar_tabelas
from datetime import datetime, date

COR_FUNDO      = "#f4f6f9"
COR_PRIMARIA   = "#2d6a4f"
COR_SECUNDARIA = "#40916c"
COR_TEXTO      = "#1b1b1b"
COR_BRANCO     = "#ffffff"
FONTE_TITULO   = ("Segoe UI", 16, "bold")
FONTE_NORMAL   = ("Segoe UI", 10)
FONTE_BTN      = ("Segoe UI", 10, "bold")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Entregas")
        self.root.geometry("500x600")
        self.root.configure(bg=COR_FUNDO)
        self.root.resizable(False, False)
        criar_tabelas()
        self.tela_principal()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ── TELA PRINCIPAL ───────────────────────────────────────
    def tela_principal(self):
        self.limpar_tela()
        self.root.geometry("500x400")

        tk.Label(self.root, text="Sistema de Entregas",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_PRIMARIA).pack(pady=30)

        tk.Label(self.root, text="O que você quer fazer?",
                 font=FONTE_NORMAL, bg=COR_FUNDO,
                 fg=COR_TEXTO).pack(pady=5)

        botoes = [
            ("📦  Registrar Entrega",    self.tela_registrar),
            ("📋  Ver Entregas do Dia",  self.tela_ver_entregas),
            ("📊  Gerar Relatório",      self.tela_relatorio),
        ]

        for texto, comando in botoes:
            tk.Button(self.root, text=texto, command=comando,
                      font=FONTE_BTN, bg=COR_PRIMARIA,
                      fg=COR_BRANCO, width=28, pady=8,
                      relief="flat", cursor="hand2",
                      activebackground=COR_SECUNDARIA,
                      activeforeground=COR_BRANCO).pack(pady=8)

    # ── TELA REGISTRAR ───────────────────────────────────────
    def tela_registrar(self):
        self.limpar_tela()
        self.root.geometry("500x600")

        tk.Label(self.root, text="Registrar Nova Entrega",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_PRIMARIA).pack(pady=15)

        frame = tk.Frame(self.root, bg=COR_FUNDO)
        frame.pack(padx=30, fill="x")

        campos = {}

        def campo(label, chave):
            tk.Label(frame, text=label, font=FONTE_NORMAL,
                     bg=COR_FUNDO, fg=COR_TEXTO,
                     anchor="w").pack(fill="x", pady=(8, 0))
            entry = tk.Entry(frame, font=FONTE_NORMAL, relief="solid", bd=1)
            entry.pack(fill="x", ipady=5)
            campos[chave] = entry

        campo("Número do Pedido", "numero_pedido")
        campo("Nome do Cliente",  "cliente")
        campo("Endereço",         "endereco")
        campo("Horário Previsto (HH:MM)", "horario_previsto")

        tk.Label(frame, text="Status", font=FONTE_NORMAL,
                 bg=COR_FUNDO, fg=COR_TEXTO,
                 anchor="w").pack(fill="x", pady=(8, 0))
        status_var = tk.StringVar(value="Entregue")
        status_menu = ttk.Combobox(frame, textvariable=status_var,
                                   values=["Entregue", "Atrasado", "Devolvido", "Pendente"],
                                   state="readonly", font=FONTE_NORMAL)
        status_menu.pack(fill="x", ipady=5)

        campo("Motivo do Atraso (se houver)", "motivo_atraso")

        def salvar():
            dados = {k: v.get().strip() for k, v in campos.items()}
            if not dados["numero_pedido"] or not dados["cliente"] or not dados["endereco"]:
                messagebox.showwarning("Atenção", "Preencha pelo menos pedido, cliente e endereço.")
                return

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO entregas
                (numero_pedido, cliente, endereco, horario_previsto, horario_real, status, motivo_atraso, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dados["numero_pedido"],
                dados["cliente"],
                dados["endereco"],
                dados["horario_previsto"],
                datetime.now().strftime("%H:%M"),
                status_var.get(),
                dados["motivo_atraso"],
                date.today().isoformat()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Entrega registrada!")
            self.tela_principal()

        tk.Button(frame, text="✔  Salvar Entrega", command=salvar,
                  font=FONTE_BTN, bg=COR_PRIMARIA, fg=COR_BRANCO,
                  width=25, pady=8, relief="flat",
                  cursor="hand2").pack(pady=15)

        tk.Button(frame, text="← Voltar", command=self.tela_principal,
                  font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_PRIMARIA,
                  relief="flat", cursor="hand2").pack(pady=(0, 15))

    # ── TELA VER ENTREGAS ────────────────────────────────────
    def tela_ver_entregas(self):
        self.limpar_tela()
        self.root.geometry("500x450")

        tk.Label(self.root, text="Entregas de Hoje",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_PRIMARIA).pack(pady=15)

        frame = tk.Frame(self.root, bg=COR_FUNDO)
        frame.pack(fill="both", expand=True, padx=15)

        colunas = ("Pedido", "Cliente", "Status", "Horário Real")
        tabela = ttk.Treeview(frame, columns=colunas, show="headings", height=10)

        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=110, anchor="center")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT numero_pedido, cliente, status, horario_real
            FROM entregas WHERE data = ?
        """, (date.today().isoformat(),))
        for row in cursor.fetchall():
            tabela.insert("", "end", values=row)
        conn.close()

        tabela.pack(fill="both", expand=True)

        tk.Button(self.root, text="← Voltar", command=self.tela_principal,
                  font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_PRIMARIA,
                  relief="flat", cursor="hand2").pack(pady=10)

    # ── TELA RELATÓRIO ───────────────────────────────────────
    def tela_relatorio(self):
        self.limpar_tela()
        self.root.geometry("500x420")

        tk.Label(self.root, text="Relatório do Dia",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_PRIMARIA).pack(pady=15)

        conn = conectar()
        cursor = conn.cursor()
        hoje = date.today().isoformat()

        cursor.execute("SELECT COUNT(*) FROM entregas WHERE data = ?", (hoje,))
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM entregas WHERE data = ? AND status = 'Entregue'", (hoje,))
        entregues = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM entregas WHERE data = ? AND status = 'Atrasado'", (hoje,))
        atrasados = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM entregas WHERE data = ? AND status = 'Devolvido'", (hoje,))
        devolvidos = cursor.fetchone()[0]

        cursor.execute("""
            SELECT motivo_atraso, COUNT(*) as total
            FROM entregas WHERE data = ? AND motivo_atraso != ''
            GROUP BY motivo_atraso ORDER BY total DESC LIMIT 1
        """, (hoje,))
        motivo = cursor.fetchone()
        conn.close()

        pct_prazo = round((entregues / total * 100), 1) if total > 0 else 0

        frame = tk.Frame(self.root, bg=COR_BRANCO, relief="flat", bd=0)
        frame.pack(padx=30, pady=5, fill="both", expand=True)

        def linha(label, valor, cor=COR_TEXTO):
            f = tk.Frame(frame, bg=COR_BRANCO)
            f.pack(fill="x", padx=20, pady=6)
            tk.Label(f, text=label, font=FONTE_NORMAL,
                     bg=COR_BRANCO, fg=COR_TEXTO, anchor="w").pack(side="left")
            tk.Label(f, text=valor, font=("Segoe UI", 10, "bold"),
                     bg=COR_BRANCO, fg=cor, anchor="e").pack(side="right")

        linha("📦 Total de entregas",   str(total))
        linha("✅ Entregues no prazo",   f"{entregues} ({pct_prazo}%)", "#2d6a4f")
        linha("⏰ Atrasadas",           str(atrasados), "#e07b00")
        linha("🔁 Devolvidas",          str(devolvidos), "#c1121f")
        linha("⚠️  Causa mais comum",   motivo[0] if motivo else "Nenhuma", "#555")

        tk.Button(self.root, text="← Voltar", command=self.tela_principal,
                  font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_PRIMARIA,
                  relief="flat", cursor="hand2").pack(pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
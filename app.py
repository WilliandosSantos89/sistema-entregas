import tkinter as tk
from tkinter import messagebox, ttk
from banco import conectar, criar_tabelas, gerar_numero_pedido, registrar_historico, iniciar_cronometro, registrar_saida
from datetime import datetime, date

COR_FUNDO      = "#f4f6f9"
COR_PRIMARIA   = "#2d6a4f"
COR_SECUNDARIA = "#40916c"
COR_TEXTO      = "#1b1b1b"
COR_BRANCO     = "#ffffff"
COR_ALERTA     = "#e07b00"
COR_PERIGO     = "#c1121f"
FONTE_TITULO   = ("Segoe UI", 16, "bold")
FONTE_NORMAL   = ("Segoe UI", 10)
FONTE_BTN      = ("Segoe UI", 10, "bold")
FONTE_TIMER    = ("Segoe UI", 36, "bold")

STATUS_OPCOES = [
    "Aguardando Retirada",
    "Em Rota",
    "Entregue",
    "Devolvido",
    "Pendente"
]

COR_STATUS = {
    "Aguardando Retirada": "#555555",
    "Em Rota":             "#1565c0",
    "Entregue":            "#2d6a4f",
    "Devolvido":           "#c1121f",
    "Pendente":            "#e07b00",
}

TEMPO_ROTA = 5 * 60  # 5 minutos em segundos


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Entregas")
        self.root.configure(bg=COR_FUNDO)
        self.root.resizable(False, False)
        self._timer_job = None
        self._tempo_restante = 0
        self._registro_id = None
        criar_tabelas()
        self.tela_principal()

    def limpar_tela(self):
        if self._timer_job:
            self.root.after_cancel(self._timer_job)
            self._timer_job = None
        for widget in self.root.winfo_children():
            widget.destroy()

    # ── TELA PRINCIPAL ───────────────────────────────────────
    def tela_principal(self):
        self.limpar_tela()
        self.root.geometry("500x450")

        tk.Label(self.root, text="Sistema de Entregas",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_PRIMARIA).pack(pady=25)

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
                      activeforeground=COR_BRANCO).pack(pady=7)

        # botão iniciar rota — destaque visual diferente
        tk.Button(self.root, text="🚗  Iniciar Rota",
                  command=self.tela_cronometro,
                  font=FONTE_BTN, bg=COR_ALERTA,
                  fg=COR_BRANCO, width=28, pady=8,
                  relief="flat", cursor="hand2").pack(pady=7)

    # ── TELA CRONÔMETRO ──────────────────────────────────────
    def tela_cronometro(self):
        self.limpar_tela()
        self.root.geometry("500x420")

        tk.Label(self.root, text="Cronômetro de Saída",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_ALERTA).pack(pady=20)

        tk.Label(self.root,
                 text="Organize os pedidos e saia em até 5 minutos.",
                 font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO).pack()

        # display do timer
        self._timer_label = tk.Label(self.root, text="05:00",
                                      font=FONTE_TIMER, bg=COR_FUNDO,
                                      fg=COR_PRIMARIA)
        self._timer_label.pack(pady=30)

        self._status_label = tk.Label(self.root, text="",
                                       font=FONTE_NORMAL, bg=COR_FUNDO,
                                       fg=COR_TEXTO)
        self._status_label.pack()

        self._btn_iniciar = tk.Button(self.root, text="▶  Iniciar Cronômetro",
                                       command=self._iniciar_timer,
                                       font=FONTE_BTN, bg=COR_PRIMARIA,
                                       fg=COR_BRANCO, width=25, pady=8,
                                       relief="flat", cursor="hand2")
        self._btn_iniciar.pack(pady=15)

        self._btn_saiu = tk.Button(self.root, text="✔  Confirmar Saída",
                                    command=self._confirmar_saida,
                                    font=FONTE_BTN, bg=COR_SECUNDARIA,
                                    fg=COR_BRANCO, width=25, pady=8,
                                    relief="flat", cursor="hand2",
                                    state="disabled")
        self._btn_saiu.pack(pady=5)

        tk.Button(self.root, text="← Voltar", command=self.tela_principal,
                  font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_PRIMARIA,
                  relief="flat", cursor="hand2").pack(pady=10)

    def _iniciar_timer(self):
        self._tempo_restante = TEMPO_ROTA
        self._registro_id = iniciar_cronometro()
        self._btn_iniciar.config(state="disabled")
        self._btn_saiu.config(state="normal")
        self._status_label.config(text="Cronômetro rodando...", fg=COR_PRIMARIA)
        self._tick()

    def _tick(self):
        if self._tempo_restante <= 0:
            self._timer_label.config(text="00:00", fg=COR_PERIGO)
            self._status_label.config(
                text="⚠️  Tempo esgotado! Saia imediatamente.", fg=COR_PERIGO)
            self.root.bell()
            return

        minutos = self._tempo_restante // 60
        segundos = self._tempo_restante % 60
        texto = f"{minutos:02d}:{segundos:02d}"
        self._timer_label.config(text=texto)

        # muda cor para vermelho nos últimos 60 segundos
        if self._tempo_restante <= 60:
            self._timer_label.config(fg=COR_PERIGO)
        elif self._tempo_restante <= 120:
            self._timer_label.config(fg=COR_ALERTA)

        self._tempo_restante -= 1
        self._timer_job = self.root.after(1000, self._tick)

    def _confirmar_saida(self):
        if self._timer_job:
            self.root.after_cancel(self._timer_job)
            self._timer_job = None

        saiu_no_prazo = self._tempo_restante > 0
        registrar_saida(self._registro_id, saiu_no_prazo)

        if saiu_no_prazo:
            mins = self._tempo_restante // 60
            segs = self._tempo_restante % 60
            messagebox.showinfo("Boa saída!",
                f"Saída confirmada com {mins:02d}:{segs:02d} de sobra. Bom trabalho!")
        else:
            messagebox.showwarning("Saída atrasada",
                "Saída confirmada após o tempo. Registrado como atraso.")

        self.tela_principal()

    # ── TELA REGISTRAR ───────────────────────────────────────
    def tela_registrar(self):
        self.limpar_tela()
        self.root.geometry("500x620")

        tk.Label(self.root, text="Registrar Nova Entrega",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_PRIMARIA).pack(pady=15)

        frame = tk.Frame(self.root, bg=COR_FUNDO)
        frame.pack(padx=30, fill="x")

        campos = {}

        def campo(label, chave, valor_inicial=""):
            tk.Label(frame, text=label, font=FONTE_NORMAL,
                     bg=COR_FUNDO, fg=COR_TEXTO,
                     anchor="w").pack(fill="x", pady=(8, 0))
            var = tk.StringVar(value=valor_inicial)
            entry = tk.Entry(frame, textvariable=var,
                             font=FONTE_NORMAL, relief="solid", bd=1)
            entry.pack(fill="x", ipady=5)
            campos[chave] = entry
            return entry

        tk.Label(frame, text="Número do Pedido", font=FONTE_NORMAL,
                 bg=COR_FUNDO, fg=COR_TEXTO, anchor="w").pack(fill="x", pady=(8, 0))
        num_var = tk.StringVar(value=gerar_numero_pedido())
        num_entry = tk.Entry(frame, textvariable=num_var, font=FONTE_NORMAL,
                             relief="solid", bd=1, state="disabled",
                             disabledforeground="#555", disabledbackground="#e8ece8")
        num_entry.pack(fill="x", ipady=5)

        campo("Nome do Cliente",  "cliente")
        campo("Endereço",         "endereco")

        tk.Label(frame, text="Horário Previsto", font=FONTE_NORMAL,
                 bg=COR_FUNDO, fg=COR_TEXTO, anchor="w").pack(fill="x", pady=(8, 0))
        horario_var = tk.StringVar(value=datetime.now().strftime("%H:%M"))
        horario_entry = tk.Entry(frame, textvariable=horario_var,
                                 font=FONTE_NORMAL, relief="solid", bd=1)
        horario_entry.pack(fill="x", ipady=5)
        campos["horario_previsto"] = horario_entry

        tk.Label(frame, text="Status", font=FONTE_NORMAL,
                 bg=COR_FUNDO, fg=COR_TEXTO,
                 anchor="w").pack(fill="x", pady=(8, 0))
        status_var = tk.StringVar(value="Aguardando Retirada")
        ttk.Combobox(frame, textvariable=status_var,
                     values=STATUS_OPCOES,
                     state="readonly", font=FONTE_NORMAL).pack(fill="x", ipady=5)

        tk.Label(frame, text="Acompanhamento", font=FONTE_NORMAL,
                 bg=COR_FUNDO, fg=COR_TEXTO,
                 anchor="w").pack(fill="x", pady=(8, 0))
        acomp_entry = tk.Entry(frame, font=FONTE_NORMAL, relief="solid", bd=1)
        acomp_entry.pack(fill="x", ipady=5)

        def salvar():
            dados = {k: v.get().strip() for k, v in campos.items()}
            if not dados["cliente"] or not dados["endereco"]:
                messagebox.showwarning("Atenção", "Preencha cliente e endereço.")
                return

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO entregas
                (numero_pedido, cliente, endereco, horario_previsto,
                 horario_real, status, acompanhamento, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                num_var.get(),
                dados["cliente"],
                dados["endereco"],
                dados["horario_previsto"],
                datetime.now().strftime("%H:%M"),
                status_var.get(),
                acomp_entry.get().strip(),
                date.today().isoformat()
            ))
            entrega_id = cursor.lastrowid
            conn.commit()
            conn.close()

            registrar_historico(entrega_id, status_var.get())
            messagebox.showinfo("Sucesso", f"Entrega {num_var.get()} registrada!")
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
        self.root.geometry("700x500")

        tk.Label(self.root, text="Entregas de Hoje",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_PRIMARIA).pack(pady=15)

        frame = tk.Frame(self.root, bg=COR_FUNDO)
        frame.pack(fill="both", expand=True, padx=15)

        colunas = ("Pedido", "Cliente", "Status", "Horário", "Acompanhamento")
        tabela = ttk.Treeview(frame, columns=colunas, show="headings", height=12)

        larguras = [90, 140, 150, 70, 180]
        for col, larg in zip(colunas, larguras):
            tabela.heading(col, text=col)
            tabela.column(col, width=larg, anchor="center")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT numero_pedido, cliente, status, horario_real, acompanhamento
            FROM entregas WHERE data = ?
            ORDER BY id ASC
        """, (date.today().isoformat(),))
        for row in cursor.fetchall():
            tabela.insert("", "end", values=row)
        conn.close()

        tabela.pack(fill="both", expand=True)

        def atualizar_status():
            selecionado = tabela.selection()
            if not selecionado:
                messagebox.showwarning("Atenção", "Selecione uma entrega.")
                return
            valores = tabela.item(selecionado[0])["values"]
            self.tela_atualizar_status(valores[0])

        tk.Button(self.root, text="🔄  Atualizar Status", command=atualizar_status,
                  font=FONTE_BTN, bg=COR_SECUNDARIA, fg=COR_BRANCO,
                  width=20, pady=6, relief="flat",
                  cursor="hand2").pack(pady=8)

        tk.Button(self.root, text="← Voltar", command=self.tela_principal,
                  font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_PRIMARIA,
                  relief="flat", cursor="hand2").pack(pady=(0, 10))

    # ── TELA ATUALIZAR STATUS ────────────────────────────────
    def tela_atualizar_status(self, numero_pedido):
        self.limpar_tela()
        self.root.geometry("500x420")

        tk.Label(self.root, text="Atualizar Status",
                 font=FONTE_TITULO, bg=COR_FUNDO,
                 fg=COR_PRIMARIA).pack(pady=15)

        frame = tk.Frame(self.root, bg=COR_FUNDO)
        frame.pack(padx=30, fill="x")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, numero_pedido, cliente, status, acompanhamento
            FROM entregas WHERE numero_pedido = ?
        """, (numero_pedido,))
        entrega = cursor.fetchone()
        conn.close()

        entrega_id, num, cliente, status_atual, acomp_atual = entrega

        tk.Label(frame, text=f"Pedido: {num}  |  Cliente: {cliente}",
                 font=("Segoe UI", 10, "bold"), bg=COR_FUNDO,
                 fg=COR_TEXTO).pack(anchor="w", pady=(0, 10))

        tk.Label(frame, text=f"Status atual: {status_atual}",
                 font=FONTE_NORMAL, bg=COR_FUNDO,
                 fg=COR_STATUS.get(status_atual, COR_TEXTO)).pack(anchor="w", pady=(0, 15))

        tk.Label(frame, text="Novo Status", font=FONTE_NORMAL,
                 bg=COR_FUNDO, fg=COR_TEXTO, anchor="w").pack(fill="x", pady=(0, 4))
        novo_status_var = tk.StringVar(value=status_atual)
        ttk.Combobox(frame, textvariable=novo_status_var,
                     values=STATUS_OPCOES,
                     state="readonly", font=FONTE_NORMAL).pack(fill="x", ipady=5)

        tk.Label(frame, text="Acompanhamento", font=FONTE_NORMAL,
                 bg=COR_FUNDO, fg=COR_TEXTO, anchor="w").pack(fill="x", pady=(12, 4))
        acomp_entry = tk.Entry(frame, font=FONTE_NORMAL, relief="solid", bd=1)
        acomp_entry.insert(0, acomp_atual or "")
        acomp_entry.pack(fill="x", ipady=5)

        def salvar_atualizacao():
            novo = novo_status_var.get()
            acomp = acomp_entry.get().strip()

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE entregas SET status = ?, acompanhamento = ?
                WHERE numero_pedido = ?
            """, (novo, acomp, numero_pedido))
            conn.commit()
            conn.close()

            registrar_historico(entrega_id, novo)
            messagebox.showinfo("Sucesso", "Status atualizado!")
            self.tela_ver_entregas()

        tk.Button(frame, text="✔  Salvar Atualização", command=salvar_atualizacao,
                  font=FONTE_BTN, bg=COR_PRIMARIA, fg=COR_BRANCO,
                  width=25, pady=8, relief="flat",
                  cursor="hand2").pack(pady=15)

        tk.Button(frame, text="← Voltar", command=self.tela_ver_entregas,
                  font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_PRIMARIA,
                  relief="flat", cursor="hand2").pack()

    # ── TELA RELATÓRIO ───────────────────────────────────────
    def tela_relatorio(self):
        self.limpar_tela()
        self.root.geometry("500x560")

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

        cursor.execute("SELECT COUNT(*) FROM entregas WHERE data = ? AND status = 'Em Rota'", (hoje,))
        em_rota = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM entregas WHERE data = ? AND status = 'Aguardando Retirada'", (hoje,))
        aguardando = cursor.fetchone()[0]

        cursor.execute("""
            SELECT acompanhamento, COUNT(*) as total
            FROM entregas WHERE data = ? AND acompanhamento != ''
            GROUP BY acompanhamento ORDER BY total DESC LIMIT 1
        """, (hoje,))
        acomp = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM registros_saida WHERE data = ?", (hoje,))
        total_saidas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM registros_saida WHERE data = ? AND saiu_no_prazo = 1", (hoje,))
        saidas_prazo = cursor.fetchone()[0]

        conn.close()

        pct_prazo     = round((entregues / total * 100), 1) if total > 0 else 0
        pct_saida     = round((saidas_prazo / total_saidas * 100), 1) if total_saidas > 0 else 0

        frame = tk.Frame(self.root, bg=COR_BRANCO)
        frame.pack(padx=30, pady=5, fill="both", expand=True)

        def linha(label, valor, cor=COR_TEXTO):
            f = tk.Frame(frame, bg=COR_BRANCO)
            f.pack(fill="x", padx=20, pady=6)
            tk.Label(f, text=label, font=FONTE_NORMAL,
                     bg=COR_BRANCO, fg=COR_TEXTO, anchor="w").pack(side="left")
            tk.Label(f, text=valor, font=("Segoe UI", 10, "bold"),
                     bg=COR_BRANCO, fg=cor, anchor="e").pack(side="right")

        linha("📦 Total de entregas",       str(total))
        linha("⏳ Aguardando Retirada",     str(aguardando), "#555555")
        linha("🚗 Em Rota",                 str(em_rota),    "#1565c0")
        linha("✅ Entregues",               f"{entregues} ({pct_prazo}%)", "#2d6a4f")
        linha("⏰ Atrasadas",              str(atrasados),  "#e07b00")
        linha("🔁 Devolvidas",             str(devolvidos), "#c1121f")
        linha("📝 Acomp. mais frequente",  acomp[0] if acomp else "Nenhum", "#555")

        # separador
        tk.Frame(frame, bg="#ddd", height=1).pack(fill="x", padx=20, pady=8)

        linha("🏁 Saídas realizadas",       str(total_saidas))
        linha("✅ Saídas no prazo",          f"{saidas_prazo} ({pct_saida}%)", "#2d6a4f")

        tk.Button(self.root, text="← Voltar", command=self.tela_principal,
                  font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_PRIMARIA,
                  relief="flat", cursor="hand2").pack(pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
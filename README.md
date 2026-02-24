# 📦 Sistema de Entregas

Aplicação desktop desenvolvida em Python para registro, acompanhamento e análise de entregas no setor logístico — construída a partir de um problema real observado na operação diária.

---

## 💡 Origem do Projeto

Trabalhando diretamente na operação de entregas de uma empresa farmacêutica, identifiquei gargalos concretos no processo: ausência de rastreabilidade por etapa, conferência manual em papel no encerramento do turno e falta de visibilidade sobre as causas de atraso.

Este sistema foi desenvolvido para resolver esses problemas de forma prática, leve e sem dependência de infraestrutura externa.

---

## ✅ Funcionalidades

- Registro de entregas com numeração automática sequencial (`ENT-001`, `ENT-002`...)
- Horário de registro preenchido automaticamente e editável
- Acompanhamento em tempo real com campo de observações por entrega
- Fluxo completo de status: `Aguardando Retirada → Em Rota → Entregue / Devolvido / Pendente`
- Atualização de status com histórico registrado por horário
- Listagem de todas as entregas do dia em tabela
- Relatório diário automático com totais, percentual de entregas no prazo e acompanhamento mais frequente

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Python 3.11 | Linguagem principal |
| Tkinter | Interface gráfica desktop |
| SQLite | Banco de dados local |

Sem dependências externas. Roda diretamente com Python instalado.

---

## 📁 Estrutura do Projeto

```
sistema-entregas/
│
├── app.py        # Interface gráfica e lógica de navegação
├── banco.py      # Conexão, criação de tabelas e funções de banco
└── entregas.db   # Banco de dados gerado automaticamente na primeira execução
```

---

## ▶️ Como Executar

**Pré-requisito:** Python 3.8 ou superior instalado.

```bash
# Clone o repositório
git clone https://github.com/WilliandosSantos89/sistema-entregas.git

# Acesse a pasta
cd sistema-entregas

# Execute
python app.py
```

O banco de dados é criado automaticamente na primeira execução.

---

## 🗺️ Próximos Passos

- [ ] Exportação do relatório diário em PDF ou CSV
- [ ] Filtro de entregas por status e período
- [ ] Sistema web integrado com notificação ao cliente no momento do despacho
- [ ] Painel gerencial com histórico por entregador

---

## 👤 Autor

**Willian dos Santos**  
Desenvolvedor em formação | ADS | Administração  
[LinkedIn](https://www.linkedin.com/in/willian-dos-santos) • [GitHub](https://github.com/WilliandosSantos89)

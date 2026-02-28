# 📦 Sistema de Entregas

Aplicação desktop desenvolvida em Python para registro, acompanhamento e análise de entregas no setor logístico farmacêutico — primeiro módulo do projeto FarmaFlow.

---

## 💡 Origem do Projeto

Operações de entrega no setor farmacêutico enfrentam desafios comuns: ausência de rastreabilidade por etapa, conferência manual no encerramento do turno, falta de visibilidade sobre causas de atraso e nenhum controle sobre o tempo de organização antes da saída para rota.

Este módulo foi desenvolvido para resolver esses problemas de forma prática, leve e sem dependência de infraestrutura externa.

---

## ✅ Funcionalidades

### 📦 Registro de Entregas
- Numeração automática sequencial no formato `ENT-001`, `ENT-002`...
- Horário de registro preenchido automaticamente e editável
- Campo de acompanhamento para observações em tempo real
- Fluxo completo de status:

```
Aguardando Retirada → Em Rota → Entregue / Devolvido / Pendente
```

### 🔄 Acompanhamento
- Listagem de todas as entregas do dia em tabela
- Atualização de status com novo acompanhamento a qualquer momento
- Histórico completo de cada mudança de status registrado por horário

### 🚗 Cronômetro de Saída
- Botão Iniciar Rota dispara cronômetro regressivo de 5 minutos
- Alerta visual progressivo: verde → amarelo (2 min) → vermelho (1 min)
- Alerta sonoro ao zerar o tempo
- Confirmação de saída registra horário real e se saiu dentro do prazo

### 📊 Relatório Diário
- Total de entregas e distribuição por status
- Percentual de entregas concluídas no prazo
- Acompanhamento mais frequente do dia
- Total de saídas realizadas e percentual dentro do prazo

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

- [ ] Migração para o repositório central FarmaFlow
- [ ] Integração com o módulo de Caixa e Conferência
- [ ] Exportação do relatório diário em PDF ou CSV
- [ ] Sistema web com notificação ao cliente no momento do despacho
- [ ] Otimização de rota no mapa com ponto de partida fixo

---

## 🌿 Parte do Projeto FarmaFlow

Este repositório é o Módulo 01 do [FarmaFlow](https://github.com/WilliandosSantos89/farmaflow) — sistema modular de gestão para redes farmacêuticas.

---

## 👤 Autor

**Willian dos Santos**
Desenvolvedor em formação | ADS | Administração
[LinkedIn](https://www.linkedin.com/in/willian-dos-santos) • [GitHub](https://github.com/WilliandosSantos89)
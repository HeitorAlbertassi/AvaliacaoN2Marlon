# Sistema de Agendamento de Barbearia - Backend

Sistema de agendamento de barbearia implementado em Python, simulando uma arquitetura AWS com Flask, TinyDB e filas de processamento.

## Arquitetura

<img width="973" height="392" alt="image" src="https://github.com/user-attachments/assets/dfa4e2f7-adb0-4fc5-b02f-03657bff1177" />

## Componentes

### 1. Lambda AcessoCliente
- Verifica se o email já está cadastrado
- Cria nova conta se o email não existir
- Retorna erro se o email já estiver em uso

### 2. Lambda DefineAgendamento
- Recebe dados do agendamento (barbeiro, data, horário)
- Valida formato do horário (intervalos de 30min)
- Envia para a fila SQS de processamento

### 3. Lambda ValidaAgendamento
- Processa mensagens da fila SQS
- Verifica conflitos de agendamento
- Retorna horários disponíveis se houver conflito
- Confirma agendamento e salva no banco

### 4. Lambda NotificarAtividadeAgendamento
- Prepara mensagens para SNS
- Envia notificações para cliente e barbeiro

### 5. SNS NotificaAgendamento
- Simula envio de SMS e E-mail via print/log
- Notifica cliente e barbeiro sobre o agendamento

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute a aplicação:
```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

## Endpoints

### POST /cliente/acesso
Cria ou verifica acesso do cliente.

**Body:**
```json
{
  "nome": "João",
  "sobrenome": "Silva",
  "email": "joao@email.com",
  "celular": "11999999999"
}
```

### POST /agendamento/definir
Define um agendamento.

**Body:**
```json
{
  "cliente_email": "joao@email.com",
  "barbeiro": "Carlos",
  "data": "2024-01-15",
  "horario": "14:00"
}
```

**Nota:** O horário deve ser em intervalos de 30 minutos (ex: 09:00, 09:30, 10:00)

### GET /agendamento/listar
Lista todos os agendamentos.

### GET /cliente/listar
Lista todos os clientes.

### GET /health
Health check da API.

## Estrutura do Projeto

```
.
├── app.py                          # API Gateway (Flask)
├── requirements.txt                # Dependências
├── database/
│   ├── db_manager.py              # Gerenciador TinyDB
│   └── data/                      # Dados JSON (criado automaticamente)
│       ├── tabela_cliente.json
│       └── tabela_agendamento.json
├── lambdas/
│   ├── acesso_cliente.py          # Lambda AcessoCliente
│   ├── define_agendamento.py      # Lambda DefineAgendamento
│   ├── valida_agendamento.py      # Lambda ValidaAgendamento
│   └── notificar_atividade_agendamento.py  # Lambda NotificarAtividadeAgendamento
├── queue/
│   └── sqs_simulator.py           # Simulador SQS
└── sns/
    └── sns_simulator.py           # Simulador SNS
```

## Fluxo de Uso

1. **Criar Cliente:**
   - POST `/cliente/acesso` com dados do cliente
   - Se o email já existir, retorna erro
   - Se não existir, cria a conta

2. **Definir Agendamento:**
   - POST `/agendamento/definir` com dados do agendamento
   - O sistema valida o cliente e envia para a fila

3. **Processamento Automático:**
   - A fila SQS processa automaticamente
   - ValidaAgendamento verifica conflitos
   - Se confirmado, salva no banco e envia notificações

4. **Notificações:**
   - As notificações são exibidas no console (simulação SNS)
   - Cliente recebe email e SMS
   - Barbeiro recebe email

## Exemplo de Uso com Postman

### 1. Criar Cliente
```
POST http://localhost:5000/cliente/acesso
Content-Type: application/json

{
  "nome": "João",
  "sobrenome": "Silva",
  "email": "joao@email.com",
  "celular": "11999999999"
}
```

### 2. Definir Agendamento
```
POST http://localhost:5000/agendamento/definir
Content-Type: application/json

{
  "cliente_email": "joao@email.com",
  "barbeiro": "Carlos",
  "data": "2024-01-15",
  "horario": "14:00"
}
```

## Observações

- Os dados são persistidos em arquivos JSON (TinyDB)
- As notificações SNS são simuladas via print no console
- A fila SQS processa mensagens automaticamente em background
- Horários devem ser em intervalos de 30 minutos
- O sistema valida conflitos e retorna horários disponíveis quando necessário

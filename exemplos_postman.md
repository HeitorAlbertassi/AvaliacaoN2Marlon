# Exemplos de Requisições - Postman

## 1. Criar Cliente

**Método:** POST  
**URL:** `http://localhost:5000/cliente/acesso`  
**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "nome": "João",
  "sobrenome": "Silva",
  "email": "joao@email.com",
  "celular": "11999999999"
}
```

**Resposta de Sucesso (201):**
```json
{
  "success": true,
  "message": "Conta criada com sucesso",
  "cliente_id": 1,
  "email": "joao@email.com"
}
```

**Resposta de Erro - Email já existe (409):**
```json
{
  "success": false,
  "message": "Já existe uma conta criada com o e-mail joao@email.com"
}
```

---

## 2. Definir Agendamento

**Método:** POST  
**URL:** `http://localhost:5000/agendamento/definir`  
**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "cliente_email": "joao@email.com",
  "barbeiro": "Carlos",
  "data": "2024-01-15",
  "horario": "14:00"
}
```

**Resposta de Sucesso (200):**
```json
{
  "success": true,
  "message": "Agendamento enviado para processamento",
  "agendamento": {
    "cliente_email": "joao@email.com",
    "cliente_nome": "João Silva",
    "cliente_celular": "11999999999",
    "barbeiro": "Carlos",
    "data": "2024-01-15",
    "horario": "14:00"
  }
}
```

**Resposta de Erro - Cliente não encontrado (404):**
```json
{
  "success": false,
  "message": "Cliente com email joao@email.com não encontrado"
}
```

**Resposta de Erro - Horário inválido (400):**
```json
{
  "success": false,
  "message": "Horário deve ser em intervalos de 30 minutos (ex: 09:00, 09:30, 10:00)"
}
```

**Resposta de Erro - Conflito de agendamento (409):**
```json
{
  "success": false,
  "message": "Já existe um agendamento para o barbeiro Carlos na data 2024-01-15 no horário 14:00",
  "horarios_disponiveis": [
    "08:00",
    "08:30",
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "12:30",
    "13:00",
    "13:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
    "17:00",
    "17:30"
  ]
}
```

---

## 3. Listar Clientes

**Método:** GET  
**URL:** `http://localhost:5000/cliente/listar`

**Resposta (200):**
```json
{
  "success": true,
  "clientes": [
    {
      "nome": "João",
      "sobrenome": "Silva",
      "email": "joao@email.com",
      "celular": "11999999999"
    }
  ]
}
```

---

## 4. Listar Agendamentos

**Método:** GET  
**URL:** `http://localhost:5000/agendamento/listar`

**Resposta (200):**
```json
{
  "success": true,
  "agendamentos": [
    {
      "cliente_email": "joao@email.com",
      "barbeiro": "Carlos",
      "data": "2024-01-15",
      "horario": "14:00",
      "status": "confirmado"
    }
  ]
}
```

---

## 5. Health Check

**Método:** GET  
**URL:** `http://localhost:5000/health`

**Resposta (200):**
```json
{
  "status": "ok",
  "message": "API Gateway funcionando"
}
```

---

## Fluxo Completo de Teste

1. **Criar primeiro cliente:**
   - POST `/cliente/acesso` com dados do João

2. **Tentar criar cliente duplicado:**
   - POST `/cliente/acesso` com mesmo email (deve retornar erro 409)

3. **Criar segundo cliente:**
   - POST `/cliente/acesso` com dados de outro cliente

4. **Definir primeiro agendamento:**
   - POST `/agendamento/definir` para João com barbeiro Carlos, data 2024-01-15, horário 14:00
   - Aguardar processamento automático (verificar console para notificações)

5. **Tentar agendamento conflitante:**
   - POST `/agendamento/definir` para outro cliente com mesmo barbeiro, data e horário
   - Deve retornar erro 409 com horários disponíveis

6. **Verificar dados:**
   - GET `/cliente/listar` - ver todos os clientes
   - GET `/agendamento/listar` - ver todos os agendamentos

---

## Observações

- Os horários devem ser em intervalos de 30 minutos (ex: 08:00, 08:30, 09:00, etc.)
- O formato de data deve ser YYYY-MM-DD (ex: 2024-01-15)
- O formato de horário deve ser HH:MM (ex: 14:00)
- As notificações SNS aparecem no console do servidor
- O processamento da fila SQS é automático em background


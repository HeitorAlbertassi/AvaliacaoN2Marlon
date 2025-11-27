# Tecnologias Usadas no Sistema

## ✅ Flask (API Gateway)

**Localização:** `app.py`

**Uso:**
- Framework web para criar a API Gateway
- Roteamento HTTP (GET, POST)
- Recebe requisições do cliente
- Encaminha para as Lambdas apropriadas
- Retorna respostas JSON

**Exemplo de uso:**
```python
@app.route('/cliente/acesso', methods=['POST'])
def acesso_cliente():
    dados = request.get_json()
    resultado = acesso_cliente_handler(dados)
    return jsonify(resultado['body']), resultado['statusCode']
```

**Endpoints criados:**
- `POST /cliente/acesso` - Criar/verificar cliente
- `POST /agendamento/definir` - Criar agendamento
- `GET /agendamento/listar` - Listar agendamentos
- `GET /cliente/listar` - Listar clientes
- `GET /health` - Health check

---

## ✅ TinyDB (NoSQL - Simula DynamoDB)

**Localização:** `database/db_manager.py`

**Uso:**
- Banco de dados NoSQL baseado em documentos JSON
- Simula o DynamoDB da AWS
- Armazena dados em arquivos JSON
- Consultas usando Query API

**Tabelas criadas:**
1. **tabela_cliente.json** - Armazena dados dos clientes
2. **tabela_agendamento.json** - Armazena dados dos agendamentos

**Funções de acesso ao banco:**
```python
# Clientes
get_cliente_by_email(email)  # Busca cliente por email
create_cliente(...)           # Cria novo cliente
get_cliente_by_email_object(email)  # Retorna objeto completo

# Agendamentos
get_agendamento_by_barbeiro_data_horario(...)  # Busca agendamento específico
get_agendamentos_by_barbeiro_data(...)         # Busca agendamentos do dia
create_agendamento(...)                        # Cria novo agendamento
```

**Onde é usado:**
- `lambdas/acesso_cliente.py` - Verifica e cria clientes
- `lambdas/define_agendamento.py` - Valida se cliente existe
- `lambdas/valida_agendamento.py` - Verifica conflitos e salva agendamentos
- `app.py` - Lista clientes e agendamentos

---

## ✅ Características NoSQL do TinyDB

**Por que é NoSQL:**
1. ✅ **Baseado em documentos** - Armazena documentos JSON
2. ✅ **Sem schema fixo** - Não precisa definir estrutura de tabelas
3. ✅ **Consultas flexíveis** - Query API permite buscas complexas
4. ✅ **Persistência em JSON** - Dados salvos em arquivos JSON
5. ✅ **Similar ao DynamoDB** - Mesma filosofia de banco de documentos

**Exemplo de documento armazenado:**
```json
{
  "nome": "João",
  "sobrenome": "Silva",
  "email": "joao@email.com",
  "celular": "11999999999"
}
```

---

## ✅ Sistema Funcional

**Confirmação de funcionalidade:**

1. ✅ **Flask está rodando** - API Gateway ativo na porta 5000
2. ✅ **TinyDB está persistindo** - Dados salvos em arquivos JSON
3. ✅ **Lambdas estão integradas** - Todas as funções chamadas corretamente
4. ✅ **Fila SQS funciona** - Processamento automático em background
5. ✅ **SNS simula notificações** - Print/log das mensagens

**Para testar:**
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Iniciar servidor
python app.py

# 3. Em outro terminal, testar
python teste_sistema.py
```

**Ou usar Postman:**
- Ver arquivo `exemplos_postman.md` para exemplos completos

---

## 📊 Fluxo de Dados

```
Cliente (Postman)
    ↓ HTTP Request
Flask API Gateway (app.py)
    ↓ Chama Lambda
Lambda (ex: acesso_cliente.py)
    ↓ Usa funções do db_manager
TinyDB (database/db_manager.py)
    ↓ Salva em JSON
Arquivo JSON (database/data/tabela_*.json)
```

---

## 🔍 Verificação Rápida

**Flask está sendo usado?**
- ✅ Sim, em `app.py` como API Gateway
- ✅ Rotas HTTP configuradas
- ✅ Servidor Flask rodando na porta 5000

**TinyDB está sendo usado?**
- ✅ Sim, em `database/db_manager.py`
- ✅ Duas tabelas criadas (clientes e agendamentos)
- ✅ Todas as lambdas usam TinyDB

**É NoSQL?**
- ✅ Sim, TinyDB é um banco NoSQL baseado em documentos JSON
- ✅ Similar ao DynamoDB da AWS

**Está funcional?**
- ✅ Sim, sistema completo e testável
- ✅ Execute `python app.py` e teste com Postman ou `teste_sistema.py`


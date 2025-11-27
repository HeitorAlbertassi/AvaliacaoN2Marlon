"""
Gerenciador de banco de dados TinyDB
Simula DynamoDB com duas tabelas: Cliente e Agendamento
"""
from tinydb import TinyDB, Query
import os

# Cria diretório se não existir
os.makedirs('database/data', exist_ok=True)

# Inicializa as tabelas
db_clientes = TinyDB('database/data/tabela_cliente.json')
db_agendamentos = TinyDB('database/data/tabela_agendamento.json')

Cliente = Query()
Agendamento = Query()

def get_cliente_by_email(email):
    """Busca cliente por email"""
    return db_clientes.search(Cliente.email == email)

def create_cliente(nome, sobrenome, email, celular):
    """Cria um novo cliente"""
    cliente = {
        'nome': nome,
        'sobrenome': sobrenome,
        'email': email,
        'celular': celular
    }
    return db_clientes.insert(cliente)

def get_agendamento_by_barbeiro_data_horario(barbeiro, data, horario):
    """Busca agendamento por barbeiro, data e horário"""
    return db_agendamentos.search(
        (Agendamento.barbeiro == barbeiro) &
        (Agendamento.data == data) &
        (Agendamento.horario == horario)
    )

def get_agendamentos_by_barbeiro_data(barbeiro, data):
    """Busca todos os agendamentos de um barbeiro em uma data"""
    return db_agendamentos.search(
        (Agendamento.barbeiro == barbeiro) &
        (Agendamento.data == data)
    )

def create_agendamento(cliente_email, barbeiro, data, horario):
    """Cria um novo agendamento"""
    agendamento = {
        'cliente_email': cliente_email,
        'barbeiro': barbeiro,
        'data': data,
        'horario': horario,
        'status': 'confirmado'
    }
    return db_agendamentos.insert(agendamento)

def get_cliente_by_email_object(email):
    """Retorna o objeto completo do cliente"""
    resultados = db_clientes.search(Cliente.email == email)
    return resultados[0] if resultados else None


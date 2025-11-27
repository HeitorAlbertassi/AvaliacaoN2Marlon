"""
Script de teste para verificar se o sistema está funcional
Execute: python teste_sistema.py
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def testar_sistema():
    print("="*60)
    print("TESTE DO SISTEMA DE AGENDAMENTO")
    print("="*60)
    
    # 1. Teste Health Check
    print("\n1. Testando Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   ✓ Status: {response.status_code}")
        print(f"   ✓ Resposta: {response.json()}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
        print("   ⚠ Certifique-se de que o servidor está rodando (python app.py)")
        return
    
    # 2. Criar Cliente
    print("\n2. Criando cliente...")
    cliente_data = {
        "nome": "João",
        "sobrenome": "Silva",
        "email": "joao.teste@email.com",
        "celular": "11999999999"
    }
    try:
        response = requests.post(f"{BASE_URL}/cliente/acesso", json=cliente_data)
        print(f"   ✓ Status: {response.status_code}")
        print(f"   ✓ Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
        return
    
    # 3. Tentar criar cliente duplicado
    print("\n3. Tentando criar cliente duplicado...")
    try:
        response = requests.post(f"{BASE_URL}/cliente/acesso", json=cliente_data)
        print(f"   ✓ Status: {response.status_code} (esperado: 409)")
        print(f"   ✓ Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # 4. Definir Agendamento
    print("\n4. Definindo agendamento...")
    agendamento_data = {
        "cliente_email": "joao.teste@email.com",
        "barbeiro": "Carlos",
        "data": "2024-01-15",
        "horario": "14:00"
    }
    try:
        response = requests.post(f"{BASE_URL}/agendamento/definir", json=agendamento_data)
        print(f"   ✓ Status: {response.status_code}")
        print(f"   ✓ Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # 5. Aguardar processamento
    print("\n5. Aguardando processamento da fila (3 segundos)...")
    time.sleep(3)
    
    # 6. Listar Agendamentos
    print("\n6. Listando agendamentos...")
    try:
        response = requests.get(f"{BASE_URL}/agendamento/listar")
        print(f"   ✓ Status: {response.status_code}")
        agendamentos = response.json().get('agendamentos', [])
        print(f"   ✓ Total de agendamentos: {len(agendamentos)}")
        if agendamentos:
            print(f"   ✓ Último agendamento: {json.dumps(agendamentos[-1], indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # 7. Listar Clientes
    print("\n7. Listando clientes...")
    try:
        response = requests.get(f"{BASE_URL}/cliente/listar")
        print(f"   ✓ Status: {response.status_code}")
        clientes = response.json().get('clientes', [])
        print(f"   ✓ Total de clientes: {len(clientes)}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    print("\n" + "="*60)
    print("TESTE CONCLUÍDO!")
    print("="*60)
    print("\nVerifique o console do servidor para ver as notificações SNS")

if __name__ == "__main__":
    testar_sistema()


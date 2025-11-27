"""
API Gateway - Flask
Roteamento para todas as Lambdas do sistema de agendamento
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from lambdas.acesso_cliente import handler as acesso_cliente_handler
from lambdas.define_agendamento import handler as define_agendamento_handler
from lambdas.valida_agendamento import handler as valida_agendamento_handler
from lambdas.notificar_atividade_agendamento import handler as notificar_handler
from queue.sqs_simulator import sqs_queue
import json

app = Flask(__name__)
CORS(app)

def processar_fila_sqs():
    """Processa mensagens da fila SQS e chama ValidaAgendamento"""
    def callback(mensagem):
        # Chama Lambda ValidaAgendamento
        resultado = valida_agendamento_handler(mensagem)
        
        # Se o agendamento foi confirmado, chama NotificarAtividadeAgendamento
        if resultado['statusCode'] == 200 and resultado['body'].get('success'):
            dados_agendamento = {
                'dados': resultado['body'].get('dados')
            }
            notificar_handler(dados_agendamento)
    
    # Inicia o processador da fila
    sqs_queue.start_processor(callback)

# Inicia o processador da fila ao iniciar a aplicação
processar_fila_sqs()

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({'status': 'ok', 'message': 'API Gateway funcionando'}), 200

@app.route('/cliente/acesso', methods=['POST'])
def acesso_cliente():
    """
    Endpoint: AcessoCliente Lambda
    Cria ou verifica acesso do cliente
    """
    try:
        dados = request.get_json()
        resultado = acesso_cliente_handler(dados)
        return jsonify(resultado['body']), resultado['statusCode']
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro no gateway: {str(e)}'
        }), 500

@app.route('/agendamento/definir', methods=['POST'])
def definir_agendamento():
    """
    Endpoint: DefineAgendamento Lambda
    Define um agendamento e envia para a fila
    """
    try:
        dados = request.get_json()
        resultado = define_agendamento_handler(dados)
        return jsonify(resultado['body']), resultado['statusCode']
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro no gateway: {str(e)}'
        }), 500

@app.route('/agendamento/listar', methods=['GET'])
def listar_agendamentos():
    """
    Endpoint auxiliar para listar agendamentos
    """
    try:
        from database.db_manager import db_agendamentos
        agendamentos = db_agendamentos.all()
        return jsonify({
            'success': True,
            'agendamentos': agendamentos
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar: {str(e)}'
        }), 500

@app.route('/cliente/listar', methods=['GET'])
def listar_clientes():
    """
    Endpoint auxiliar para listar clientes
    """
    try:
        from database.db_manager import db_clientes
        clientes = db_clientes.all()
        return jsonify({
            'success': True,
            'clientes': clientes
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("="*60)
    print("🚀 API Gateway iniciado!")
    print("="*60)
    print("\nEndpoints disponíveis:")
    print("  POST /cliente/acesso - Criar/verificar acesso do cliente")
    print("  POST /agendamento/definir - Definir agendamento")
    print("  GET  /agendamento/listar - Listar agendamentos")
    print("  GET  /cliente/listar - Listar clientes")
    print("  GET  /health - Health check")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)


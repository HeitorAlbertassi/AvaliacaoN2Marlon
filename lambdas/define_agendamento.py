"""
Lambda DefineAgendamento
Recebe dados do agendamento e envia para a fila SQS (ProcessarAgendamento)
"""
from queue.sqs_simulator import sqs_queue
from database.db_manager import get_cliente_by_email_object
import json

def handler(event):
    """
    Define um agendamento e envia para a fila de processamento
    
    Args:
        event: Dicionário com os dados do agendamento
            - cliente_email: str (email do cliente)
            - barbeiro: str
            - data: str (formato: YYYY-MM-DD)
            - horario: str (formato: HH:MM)
    
    Returns:
        dict: Resposta com status e mensagem
    """
    try:
        # Extrai dados do evento
        cliente_email = event.get('cliente_email')
        barbeiro = event.get('barbeiro')
        data = event.get('data')
        horario = event.get('horario')
        
        # Validação dos campos obrigatórios
        if not all([cliente_email, barbeiro, data, horario]):
            return {
                'statusCode': 400,
                'body': {
                    'success': False,
                    'message': 'Todos os campos são obrigatórios'
                }
            }
        
        # Verifica se o cliente existe
        cliente = get_cliente_by_email_object(cliente_email)
        if not cliente:
            return {
                'statusCode': 404,
                'body': {
                    'success': False,
                    'message': f'Cliente com email {cliente_email} não encontrado'
                }
            }
        
        # Valida formato do horário (intervalo de 30min)
        hora, minuto = map(int, horario.split(':'))
        if minuto not in [0, 30]:
            return {
                'statusCode': 400,
                'body': {
                    'success': False,
                    'message': 'Horário deve ser em intervalos de 30 minutos (ex: 09:00, 09:30, 10:00)'
                }
            }
        
        # Prepara mensagem para a fila SQS
        mensagem = {
            'cliente_email': cliente_email,
            'cliente_nome': f"{cliente['nome']} {cliente['sobrenome']}",
            'cliente_celular': cliente['celular'],
            'barbeiro': barbeiro,
            'data': data,
            'horario': horario
        }
        
        # Envia para a fila
        sqs_queue.send_message(json.dumps(mensagem))
        
        return {
            'statusCode': 200,
            'body': {
                'success': True,
                'message': 'Agendamento enviado para processamento',
                'agendamento': mensagem
            }
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'success': False,
                'message': f'Erro ao processar: {str(e)}'
            }
        }


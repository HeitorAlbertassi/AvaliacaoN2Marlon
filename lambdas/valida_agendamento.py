"""
Lambda ValidaAgendamento
Valida o agendamento verificando conflitos e horários disponíveis
"""
from database.db_manager import (
    get_agendamento_by_barbeiro_data_horario,
    get_agendamentos_by_barbeiro_data,
    create_agendamento
)
import json

def gerar_horarios_disponiveis(barbeiro, data, horarios_ocupados):
    """
    Gera lista de horários disponíveis para um barbeiro em uma data
    
    Args:
        barbeiro: str
        data: str
        horarios_ocupados: list de strings (horários já agendados)
    
    Returns:
        list: Lista de horários disponíveis
    """
    # Horários de funcionamento: 08:00 às 18:00 em intervalos de 30min
    horarios_possiveis = []
    for hora in range(8, 18):
        for minuto in [0, 30]:
            horario = f"{hora:02d}:{minuto:02d}"
            horarios_possiveis.append(horario)
    
    # Remove horários ocupados
    horarios_disponiveis = [h for h in horarios_possiveis if h not in horarios_ocupados]
    
    return horarios_disponiveis

def handler(event):
    """
    Valida um agendamento verificando conflitos
    
    Args:
        event: String JSON com os dados do agendamento
            - cliente_email: str
            - cliente_nome: str
            - cliente_celular: str
            - barbeiro: str
            - data: str
            - horario: str
    
    Returns:
        dict: Resposta com status e mensagem
    """
    try:
        # Parse da mensagem JSON
        if isinstance(event, str):
            dados = json.loads(event)
        else:
            dados = event
        
        barbeiro = dados.get('barbeiro')
        data = dados.get('data')
        horario = dados.get('horario')
        cliente_email = dados.get('cliente_email')
        
        # Verifica se já existe agendamento para o mesmo barbeiro, data e horário
        agendamento_existente = get_agendamento_by_barbeiro_data_horario(barbeiro, data, horario)
        
        if agendamento_existente:
            # Busca todos os agendamentos do barbeiro na data para retornar horários disponíveis
            agendamentos_do_dia = get_agendamentos_by_barbeiro_data(barbeiro, data)
            horarios_ocupados = [ag['horario'] for ag in agendamentos_do_dia]
            horarios_disponiveis = gerar_horarios_disponiveis(barbeiro, data, horarios_ocupados)
            
            return {
                'statusCode': 409,
                'body': {
                    'success': False,
                    'message': f'Já existe um agendamento para o barbeiro {barbeiro} na data {data} no horário {horario}',
                    'horarios_disponiveis': horarios_disponiveis
                }
            }
        
        # Confirma o agendamento
        agendamento_id = create_agendamento(cliente_email, barbeiro, data, horario)
        
        # Retorna dados completos para notificação
        return {
            'statusCode': 200,
            'body': {
                'success': True,
                'message': 'Agendamento confirmado com sucesso',
                'agendamento_id': agendamento_id,
                'dados': dados
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


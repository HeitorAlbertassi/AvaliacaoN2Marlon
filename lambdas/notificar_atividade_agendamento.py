"""
Lambda NotificarAtividadeAgendamento
Prepara a mensagem para o SNS
"""
from sns.sns_simulator import sns_notifier

def handler(event):
    """
    Prepara e envia notificação do agendamento
    
    Args:
        event: Dicionário com os dados do agendamento confirmado
            - dados: dict com informações completas do agendamento
    
    Returns:
        dict: Resposta com status e mensagem
    """
    try:
        dados_agendamento = event.get('dados', {})
        
        if not dados_agendamento:
            return {
                'statusCode': 400,
                'body': {
                    'success': False,
                    'message': 'Dados do agendamento não fornecidos'
                }
            }
        
        # Prepara mensagem para SNS
        mensagem_cliente = {
            'tipo': 'email',
            'destinatario': dados_agendamento.get('cliente_email'),
            'assunto': 'Agendamento Confirmado - Barbearia',
            'corpo': f"""
Olá {dados_agendamento.get('cliente_nome')},

Seu agendamento foi confirmado com sucesso!

Detalhes:
- Barbeiro: {dados_agendamento.get('barbeiro')}
- Data: {dados_agendamento.get('data')}
- Horário: {dados_agendamento.get('horario')}

Aguardamos você!
            """.strip()
        }
        
        mensagem_sms_cliente = {
            'tipo': 'sms',
            'destinatario': dados_agendamento.get('cliente_celular'),
            'mensagem': f"Agendamento confirmado! Barbeiro: {dados_agendamento.get('barbeiro')}, Data: {dados_agendamento.get('data')}, Horário: {dados_agendamento.get('horario')}"
        }
        
        mensagem_barbeiro = {
            'tipo': 'email',
            'destinatario': f"{dados_agendamento.get('barbeiro').lower().replace(' ', '')}@barbearia.com",
            'assunto': 'Novo Agendamento - Barbearia',
            'corpo': f"""
Olá {dados_agendamento.get('barbeiro')},

Você tem um novo agendamento!

Detalhes:
- Cliente: {dados_agendamento.get('cliente_nome')}
- Email: {dados_agendamento.get('cliente_email')}
- Celular: {dados_agendamento.get('cliente_celular')}
- Data: {dados_agendamento.get('data')}
- Horário: {dados_agendamento.get('horario')}
            """.strip()
        }
        
        # Envia notificações via SNS
        sns_notifier.publish(mensagem_cliente)
        sns_notifier.publish(mensagem_sms_cliente)
        sns_notifier.publish(mensagem_barbeiro)
        
        return {
            'statusCode': 200,
            'body': {
                'success': True,
                'message': 'Notificações enviadas com sucesso'
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


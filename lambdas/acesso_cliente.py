"""
Lambda AcessoCliente
Verifica se o email já está cadastrado e cria conta se não existir
"""
from database.db_manager import get_cliente_by_email, create_cliente

def handler(event):
    """
    Processa o acesso/criação de cliente
    
    Args:
        event: Dicionário com os dados do formulário
            - nome: str
            - sobrenome: str
            - email: str
            - celular: str
    
    Returns:
        dict: Resposta com status e mensagem
    """
    try:
        # Extrai dados do evento
        nome = event.get('nome')
        sobrenome = event.get('sobrenome')
        email = event.get('email')
        celular = event.get('celular')
        
        # Validação dos campos obrigatórios
        if not all([nome, sobrenome, email, celular]):
            return {
                'statusCode': 400,
                'body': {
                    'success': False,
                    'message': 'Todos os campos são obrigatórios'
                }
            }
        
        # Verifica se o email já está cadastrado
        cliente_existente = get_cliente_by_email(email)
        
        if cliente_existente:
            return {
                'statusCode': 409,
                'body': {
                    'success': False,
                    'message': f'Já existe uma conta criada com o e-mail {email}'
                }
            }
        
        # Cria novo cliente
        cliente_id = create_cliente(nome, sobrenome, email, celular)
        
        return {
            'statusCode': 201,
            'body': {
                'success': True,
                'message': 'Conta criada com sucesso',
                'cliente_id': cliente_id,
                'email': email
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


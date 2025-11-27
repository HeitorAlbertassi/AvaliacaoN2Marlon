"""
Simulador de SNS (Simple Notification Service)
Envia notificações via SMS e E-mail (simulado via print/log)
"""
import json
from datetime import datetime

class SNSSimulator:
    def __init__(self):
        self.notifications_log = []
    
    def publish(self, message):
        """
        Publica uma notificação
        
        Args:
            message: Dicionário com:
                - tipo: 'email' ou 'sms'
                - destinatario: str
                - assunto: str (apenas para email)
                - corpo: str (apenas para email)
                - mensagem: str (apenas para sms)
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if message.get('tipo') == 'email':
            print("\n" + "="*60)
            print(f"[SNS - EMAIL] {timestamp}")
            print(f"Para: {message.get('destinatario')}")
            print(f"Assunto: {message.get('assunto')}")
            print("-" * 60)
            print(message.get('corpo', ''))
            print("="*60 + "\n")
        
        elif message.get('tipo') == 'sms':
            print("\n" + "="*60)
            print(f"[SNS - SMS] {timestamp}")
            print(f"Para: {message.get('destinatario')}")
            print("-" * 60)
            print(message.get('mensagem', ''))
            print("="*60 + "\n")
        
        # Armazena no log
        log_entry = {
            'timestamp': timestamp,
            'message': message
        }
        self.notifications_log.append(log_entry)
        
        return True
    
    def get_log(self):
        """Retorna o log de notificações"""
        return self.notifications_log

# Instância global do SNS
sns_notifier = SNSSimulator()


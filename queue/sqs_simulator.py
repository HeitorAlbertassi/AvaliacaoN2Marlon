"""
Simulador de SQS (Simple Queue Service)
Fila de processamento de agendamentos
"""
import queue
import threading
import time

class SQSSimulator:
    def __init__(self):
        self.queue = queue.Queue()
        self.is_processing = False
        self.processor_thread = None
    
    def send_message(self, message_body):
        """Envia mensagem para a fila"""
        self.queue.put(message_body)
        print(f"[SQS] Mensagem adicionada à fila: {message_body}")
        return True
    
    def receive_message(self):
        """Recebe mensagem da fila (não bloqueante)"""
        try:
            return self.queue.get_nowait()
        except queue.Empty:
            return None
    
    def start_processor(self, callback):
        """Inicia o processador de mensagens em background"""
        if self.is_processing:
            return
        
        self.is_processing = True
        
        def process_messages():
            while self.is_processing:
                message = self.receive_message()
                if message:
                    print(f"[SQS] Processando mensagem: {message}")
                    callback(message)
                else:
                    time.sleep(0.5)  # Aguarda antes de verificar novamente
        
        self.processor_thread = threading.Thread(target=process_messages, daemon=True)
        self.processor_thread.start()
        print("[SQS] Processador de mensagens iniciado")
    
    def stop_processor(self):
        """Para o processador de mensagens"""
        self.is_processing = False
        if self.processor_thread:
            self.processor_thread.join(timeout=1)
        print("[SQS] Processador de mensagens parado")

# Instância global da fila
sqs_queue = SQSSimulator()


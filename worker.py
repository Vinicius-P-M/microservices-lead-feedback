import os
import time
import json
from redis import Redis

# Configuração de conexão (mesmo padrão da API)
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = Redis(host=redis_host, port=6379, db=0)

def process_feedback(feedback_data):

    lead_id = feedback_data.get("id")
    message = feedback_data.get("feedback")
    
    print(f"--- [PROCESSANDO FEEDBACK] ---")
    print(f"Lead ID: {lead_id} | Feedback: {message}")
    # Simulando um processamento demorado (ex: consulta a banco de dados)
    time.sleep(2) 
    print(f"Status: Feedback do lead {lead_id} processado com sucesso!")

if __name__ == "__main__":
    print(f"Worker iniciado. Escutando a fila 'leads_queue' no host {redis_host}...")
    
    while True:
        result = redis_client.blpop("leads_queue", timeout=0)
        
        if result:
            # O Redis retorna uma tupla (nome_da_fila, valor)
            _, payload_string = result
            data = json.loads(payload_string)
            process_feedback(data)
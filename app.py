from flask import Flask, request, jsonify
from redis import Redis
import os
import json

app = Flask(__name__)


redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = Redis(host=redis_host, port=6379, db=0)

@app.route('/health', methods=['GET'])
def health_check():
    try:
        redis_client.ping()
        redis_status = "connected"
    except Exception:
        redis_status = "disconnected"
        
    return jsonify({
        "status": "healthy", 
        "redis": redis_status,
        "environment": os.getenv("ENV", "development")
    }), 200

@app.route('/webhook/lead', methods=['POST'])
def receive_lead():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid payload"}), 400
    

    payload_string = json.dumps(data)
    
   
    redis_client.rpush("leads_queue", payload_string)
    
    print(f"Lead enviado para a fila Redis: {data}")
    return jsonify({"message": "Lead feedback queued successfully."}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
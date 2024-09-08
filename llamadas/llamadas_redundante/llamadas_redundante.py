from flask import Flask, jsonify, request
import redis

app = Flask(__name__)

redis_client = redis.Redis(host='redis', port=6379, db=0)

@app.route('/comando', methods=['POST'])
def handle_comando():
    data = request.get_json()
    redis_client.lpush('comandos', str(data))
    print(f"Comando recibido en redundante: {data}")
    return jsonify({"status": "comando procesado en redundante", "data": data}), 200

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "redundante activo"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
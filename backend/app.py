# app.py
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime

# Configurar o caminho para a pasta frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

# Inicializar Flask apontando para o diretório frontend
app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)  # Garante que o diretório existe

# Helper functions
def generate_code():
    year = datetime.now().year
    files = [f for f in os.listdir(DATA_DIR) if f.startswith(str(year))]
    sequence = len(files) + 1
    return f"{year}-{sequence:03d}"

def save_os(data):
    code = data['codigo']
    filename = os.path.join(DATA_DIR, f"{code}.json")
    with open(filename, 'w') as f:
        json.dump(data, f)
    return code

# API Endpoints
@app.route('/api/os', methods=['POST'])
def create_os():
    data = request.json
    data['codigo'] = generate_code()
    data['data_entrada'] = datetime.now().isoformat()
    save_os(data)
    return jsonify(data), 201

@app.route('/api/os', methods=['GET'])
def list_os():
    search = request.args.get('search', '')
    os_list = []
    print(f"Diretório de dados: {DATA_DIR}")  # Debug
    print(f"Arquivos encontrados: {os.listdir(DATA_DIR)}")  # Debug
    
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(DATA_DIR, filename)
            print(f"Lendo arquivo: {file_path}")  # Debug
            try:
                with open(file_path) as f:
                    os_data = json.load(f)
                    if (search.lower() in os_data.get('codigo', '').lower() or
                        search.lower() in os_data.get('nome_cliente', '').lower() or
                        search.lower() in os_data.get('equipamento', '').lower()):
                        os_list.append(os_data)
            except Exception as e:
                print(f"Erro ao ler arquivo {filename}: {str(e)}")  # Debug
    
    print(f"Total de OS encontradas: {len(os_list)}")  # Debug
    return jsonify(os_list)

@app.route('/api/os/<code>', methods=['GET', 'PUT', 'DELETE'])
def manage_os(code):
    filename = os.path.join(DATA_DIR, f"{code}.json")
    
    if request.method == 'GET':
        with open(filename) as f:
            return jsonify(json.load(f))
    
    elif request.method == 'PUT':
        data = request.json
        with open(filename, 'w') as f:
            json.dump(data, f)
        return jsonify(data)
    
    elif request.method == 'DELETE':
        os.remove(filename)
        return '', 204

# Serve frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port="80", debug=False)
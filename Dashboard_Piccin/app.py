from flask import Flask, jsonify, Response  # Importa Response
from flask_cors import CORS  # Importa CORS per abilitare CORS
from pymongo import MongoClient
from bson import json_util
import json

app = Flask(__name__)
CORS(app)  # Permette richieste da qualsiasi origine

# Configurazione MongoDB
MONGO_URI = "mongodb://localhost:27017/"  # URI per connettersi al server MongoDB
DB_NAME = "EnvironmentGateway_SoC2"  # Nome del database
COLLECTION_NAME = "EnvironmentGateway_SoC2"  # Nome della collezione

# Connessione al client MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/')
def index():
    return 'Flask app is running!'

@app.route('/api/sensors', methods=['GET'])
def get_sensors_data():
    try:
        # Recupera l'ultimo documento inserito nella collezione
        sensor_data = collection.find().sort([('_id', -1)]).limit(1)  # Ordina in ordine decrescente per _id e prendi solo l'ultimo
        sensor_data = list(sensor_data)  # Converte il cursore in lista

        if len(sensor_data) > 0:
            # Utilizza json_util per serializzare correttamente i dati
            return Response(json.dumps(sensor_data, default=json_util.default), mimetype="application/json")
        else:
            return jsonify({"message": "Nessun dato trovato"}), 404

    except Exception as e:
        # Stampa l'errore nel terminale per debug
        print(f"Errore: {str(e)}")
        return jsonify({"error": "Errore nel recupero dei dati", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

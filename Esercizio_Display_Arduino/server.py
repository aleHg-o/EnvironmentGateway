from flask import Flask, request, jsonify
import serial
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configura la porta seriale per COM6
SERIAL_PORT = 'COM6'  # Assicurati che COM6 sia corretta
BAUD_RATE = 9600  # La velocità di comunicazione seriale

# Tenta di connettersi alla porta seriale
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print("Connessione seriale riuscita.")
except serial.SerialException as e:
    print(f"Errore nella connessione alla porta {SERIAL_PORT}: {e}")
    ser = None  # Imposta ser a None se non è riuscito a connettersi

@app.route('/send-to-arduino', methods=['POST'])
def send_to_arduino():
    if ser is None:
        return jsonify({'error': 'Impossibile connettersi alla porta seriale.'}), 500

    data = request.get_json()
    message = data.get('message', '')  # Estrai il messaggio

    if not message:
        return jsonify({'error': 'Messaggio vuoto!'}), 400

    try:
        # Scrivi il messaggio sulla porta seriale
        ser.write((message + '\n').encode())
        time.sleep(1)  # Attendi un po' per permettere ad Arduino di visualizzare il messaggio
        return jsonify({'message': f'Messaggio inviato: {message}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')  # Ascolta su tutte le interfacce di rete

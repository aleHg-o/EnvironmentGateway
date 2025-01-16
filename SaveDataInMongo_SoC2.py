import serial
import json
from pymongo import MongoClient

# Configurazione della porta seriale
SERIAL_PORT = "COM5"  # Cambia con la porta seriale usata da Arduino (es. "/dev/ttyUSB0" su Linux)
BAUD_RATE = 9600  # Deve corrispondere a quello impostato su Arduino

# Configurazione MongoDB
MONGO_URI = "mongodb://localhost:27017/"  # URI per connettersi al server MongoDB
DB_NAME = "EnvironmentGateway_SoC2"  # Nome del database
COLLECTION_NAME = "EnvironmentGateway_SoC2"  # Nome della collezione


def main():
    try:
        # Connessione a MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        print(f"Connesso al database MongoDB '{DB_NAME}', collezione '{COLLECTION_NAME}'.")

        # Apri la connessione seriale
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connesso alla porta {SERIAL_PORT} a {BAUD_RATE} baud.")

        while True:
            # Leggi una riga dalla seriale
            line = ser.readline().decode('utf-8').strip()

            if line:
                try:
                    # Decodifica il JSON ricevuto
                    data = json.loads(line)

                    # Stampa i dati JSON in un formato leggibile
                    print(json.dumps(data, indent=4))

                    # Salva i dati nel database MongoDB
                    result = collection.insert_one(data)
                    print(f"Dati salvati nel database con ID: {result.inserted_id}")

                except json.JSONDecodeError:
                    print(f"Errore nel decodificare il JSON: {line}")

    except serial.SerialException as e:
        print(f"Errore nella connessione seriale: {e}")
    except Exception as e:
        print(f"Errore generico: {e}")
    except KeyboardInterrupt:
        print("Programma interrotto dall'utente.")
    finally:
        # Chiudi la connessione seriale
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Connessione seriale chiusa.")
        # Chiudi la connessione a MongoDB
        if 'client' in locals():
            client.close()
            print("Connessione a MongoDB chiusa.")


if __name__ == "__main__":
    main()
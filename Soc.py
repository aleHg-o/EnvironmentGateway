import serial
import json

# Configurazione della porta seriale
SERIAL_PORT = "COM3"  # Cambia con la porta seriale usata da Arduino (es. "/dev/ttyUSB0" su Linux)
BAUD_RATE = 9600  # Deve corrispondere a quello impostato su Arduino


def main():
    try:
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
                except json.JSONDecodeError:
                    print(f"Errore nel decodificare il JSON: {line}")

    except serial.SerialException as e:
        print(f"Errore nella connessione seriale: {e}")
    except KeyboardInterrupt:
        print("Programma interrotto dall'utente.")
    finally:
        # Chiudi la connessione seriale
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Connessione seriale chiusa.")


if __name__ == "__main__":
    main()

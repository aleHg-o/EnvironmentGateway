import serial
import json
from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Configurazione della porta seriale
SERIAL_PORT = "COM5"  # Cambia con la porta seriale usata da Arduino
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

        # Creazione dell'interfaccia grafica
        def close_program():
            if messagebox.askokcancel("Esci", "Vuoi davvero uscire?"):
                root.destroy()
                if ser.is_open:
                    ser.close()
                    print("Connessione seriale chiusa.")
                client.close()
                print("Connessione a MongoDB chiusa.")

        def update_table(data):
            # Aggiorna le colonne se necessario
            nonlocal current_columns
            keys = list(data.keys())
            if keys != current_columns:
                current_columns = keys
                table.delete(*table.get_children())
                table["columns"] = current_columns

                for col in current_columns:
                    table.heading(col, text=col)
                    table.column(col, width=150)

            # Aggiungi i dati alla tabella
            values = [data.get(key, "") for key in current_columns]
            tag = "even" if len(table.get_children()) % 2 == 0 else "odd"
            table.insert("", tk.END, values=values, tags=(tag,))

        def update_data():
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    try:
                        # Decodifica il JSON ricevuto
                        data = json.loads(line)

                        # Aggiorna la tabella
                        update_table(data)

                        # Salva i dati nel database MongoDB
                        result = collection.insert_one(data)
                        print(f"Dati salvati nel database con ID: {result.inserted_id}")
                    except json.JSONDecodeError:
                        print(f"Errore nel decodificare il JSON: {line}")
            except Exception as e:
                print(f"Errore durante la lettura seriale: {e}")
            root.after(100, update_data)  # Richiama questa funzione ogni 100 ms

        root = tk.Tk()
        root.title("Visualizzazione Dati JSON")
        root.geometry("1000x600")

        # Applica un tema ttk
        style = ttk.Style(root)
        style.theme_use("clam")

        # Tabella per visualizzare i dati
        current_columns = []
        table = ttk.Treeview(root, show="headings")
        table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configura i tag per le righe alternate
        table.tag_configure("even", background="#E8E8E8")
        table.tag_configure("odd", background="#FFFFFF")

        # Aggiungi una barra di scorrimento verticale
        scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=table.yview)
        table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Pulsante per chiudere il programma
        exit_button = tk.Button(
            root,
            text="Esci",
            command=close_program,
            bg="#347083",
            fg="white",
            font=("Helvetica", 10, "bold"),
        )
        exit_button.pack(pady=10)

        # Avvia l'aggiornamento dei dati
        root.after(100, update_data)

        # Avvia il ciclo principale di Tkinter
        root.protocol("WM_DELETE_WINDOW", close_program)
        root.mainloop()

    except serial.SerialException as e:
        print(f"Errore nella connessione seriale: {e}")
    except Exception as e:
        print(f"Errore generico: {e}")


if __name__ == "__main__":
    main()

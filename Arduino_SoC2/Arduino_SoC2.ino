#include <DHT.h>
#include <ArduinoJson.h>

// Definizioni per i sensori
#define DHTPIN 2           // Pin digitale collegato al sensore DHT11
#define DHTTYPE DHT11      // Tipo di sensore DHT
DHT dht(DHTPIN, DHTTYPE);  // Inizializzazione sensore DHT11

// Pin del sensore PIR
const int pirPin = 7;      // Pin digitale collegato al PIR
int pirState = LOW;        // Stato iniziale del sensore PIR
int pirVal = 0;            // Variabile per memorizzare lo stato del PIR

// Pin per il modulo analogico/digitale
const int analogPin = A0;  // Pin analogico per il modulo
const int digitalPin = 3;  // Pin digitale per il modulo
const int ledPin = 13;     // LED integrato su Arduino

// Pin per la fotoresistenza
const int ldrPin = A1;     // Pin analogico per la fotoresistenza

void setup() {
  // Inizializzazione pin
  pinMode(pirPin, INPUT);
  pinMode(digitalPin, INPUT);
  pinMode(ledPin, OUTPUT);

  // Inizializzazione seriale
  Serial.begin(9600);
  Serial.println("Sistema avviato.");

  // Avvia il sensore DHT11
  dht.begin();
}

void loop() {
  // --- Lettura sensore PIR ---
  pirVal = digitalRead(pirPin);
  if (pirVal == HIGH) {
    digitalWrite(ledPin, HIGH); // Accende il LED
    pirState = HIGH;
  } else {
    digitalWrite(ledPin, LOW); // Spegne il LED
    pirState = LOW;
  }

  // --- Lettura modulo analogico/digitale ---
  int analogValue = analogRead(analogPin); // Legge il valore analogico
  int digitalValue = digitalRead(digitalPin); // Legge il valore digitale

  // --- Lettura fotoresistenza ---
  int ldrValue = analogRead(ldrPin); // Legge il valore della fotoresistenza

  // --- Lettura sensore DHT11 ---
  float humidity = dht.readHumidity();         // Legge l'umidità
  float temperature = dht.readTemperature();  // Legge la temperatura in Celsius

  // --- Creazione dell'oggetto JSON ---
  StaticJsonDocument<256> jsonDoc; // Dimensione del buffer JSON

  jsonDoc["Motion sensor"] = pirState ? "HIGH" : "LOW";
  jsonDoc["Sound sensor"]= analogValue;
  jsonDoc["Photoresistor"] = ldrValue;

  if (isnan(humidity) || isnan(temperature)) {
    jsonDoc["dht"]["error"] = "Sensore non disponibile";
  } else {
    jsonDoc["humidity"] = humidity;
    jsonDoc["temperature"] = temperature;
  }

  // Serializza l'oggetto JSON e invialo alla seriale
  serializeJson(jsonDoc, Serial);
  Serial.println();

  // --- Pausa tra le letture ---
  delay(2000); // Aspetta 2 secondi prima della prossima iterazione
}

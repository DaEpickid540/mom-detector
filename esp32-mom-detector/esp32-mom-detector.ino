#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid     = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
const char* pcIP     = "192.168.1.XXX"; // your PC's local IP
const int   pcPort   = 5555;

const int DOOR_PIN = 14;
bool lastState = HIGH;
unsigned long lastTrigger = 0;

void setup() {
  Serial.begin(115200);
  pinMode(DOOR_PIN, INPUT_PULLUP);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  Serial.println("WiFi connected");
}

void loop() {
  bool currentState = digitalRead(DOOR_PIN);

  // Door opened = went from LOW (closed/magnet near) to HIGH (open)
  if (currentState == HIGH && lastState == LOW && millis() - lastTrigger > 3000) {
    lastTrigger = millis();
    Serial.println("Door opened! Alerting PC...");

    HTTPClient http;
    String url = "http://" + String(pcIP) + ":" + String(pcPort) + "/trigger";
    http.begin(url);
    http.GET();
    http.end();
  }

  lastState = currentState;
  delay(50);
}



#include <WiFi.h>
#include <HTTPClient.h>
#include "credentials.h"

const char* ssid     = SSID;
const char* password = PASSWORD;
const char* pcIP     = PC_IP;
const int   pcPort   = PC_PORT;

const int DOOR_PIN = 14;

// RTC memory survives deep sleep (unlike normal RAM)
RTC_DATA_ATTR uint32_t bootCount = 0;

void setup() {
  Serial.begin(115200);
  delay(100);
  
  bootCount++;
  Serial.println("\n\n=== Mom Detector Woke Up ===");
  Serial.println("Boot count: " + String(bootCount));
  
  pinMode(DOOR_PIN, INPUT_PULLUP);
  
  // Read pin to see why we woke up
  bool doorState = digitalRead(DOOR_PIN);
  Serial.println("Door state: " + String(doorState ? "OPEN" : "CLOSED"));
  
  // If door is actually open (HIGH), send alert
  if (doorState == HIGH) {
    connectAndAlert();
  } else {
    // False trigger (noise/bounce), go back to sleep immediately
    Serial.println("False trigger, sleeping...");
    goToSleep();
  }
}

void connectAndAlert() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected! Sending alert...");
    
    HTTPClient http;
    String url = "http://" + String(pcIP) + ":" + String(pcPort) + "/trigger";
    http.begin(url);
    int code = http.GET();
    Serial.println("Response: " + String(code));
    http.end();
    
    WiFi.disconnect(true); // Turn off WiFi radio to save power
    delay(500);
  } else {
    Serial.println("\nWiFi failed, sleeping anyway...");
  }
  
  goToSleep();
}

void goToSleep() {
  Serial.println("Going to deep sleep, waiting for door...");
  delay(100); // Let serial flush
  
  // Configure GPIO14 (DOOR_PIN) to wake on LOW->HIGH transition
  // (door magnet pulls away = pin goes HIGH)
  esp_sleep_enable_ext0_wakeup(GPIO_NUM_14, 1); // 1 = HIGH level wakes
  
  // Go to deep sleep
  // RTC memory (bootCount) persists across sleep
  esp_deep_sleep_start();
}

void loop() {
  // Never reached—we sleep in setup() and wake from GPIO interrupt
}

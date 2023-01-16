#include <WiFiClientSecure.h>
#include <PubSubClient.h>

#define WIFI_SSID "interactieve-palen-ap"
#define WIFI_PASS "roottoor"
#define MQTT_IP "10.42.0.1"
#define MQTT_PORT 1883

#define PIN_BUTTON 13


uint64_t esp_id;
String esp_id_str;

WiFiClient wifi;

PubSubClient mqttClient(wifi);

//#region MQTT

void reconnectMQTT() {
    // Loop until we're reconnected
    while (!mqttClient.connected()) {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (mqttClient.connect("ESP32Client")) {
            Serial.println("connected");
            // Subscribe
            mqttClient.subscribe("unit/output");
//            sendMQTTAliveMessage();
        } else {
            Serial.print("failed, rc=");
            Serial.print(mqttClient.state());
            Serial.println(" try again in 5 seconds");
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}

void onMQTTMessage(char *topic, byte *message, unsigned int length) {
    Serial.print("Message arrived on topic: ");
    Serial.print(topic);
    Serial.print(". Message: ");
    String messageTemp;

    for (int i = 0; i < length; i++) {
        Serial.print((char) message[i]);
        messageTemp += (char) message[i];
    }
    Serial.println();
}

void sendMQTT(const String &topic, const String &payload) {
    if (!mqttClient.connected()) {
        reconnectMQTT();
    }

    String fullTopic = "unit/" + esp_id_str + "/" + topic;

    Serial.println("Sending MQTT message \"" + payload + "\" to topic \"" + fullTopic + "\"");

    mqttClient.publish(fullTopic.c_str(), payload.c_str());

    Serial.println("done");
}

void sendMQTTMessage(const String &message) {
    sendMQTT("message", message);
}

void sendMQTTAliveMessage() {
    sendMQTT("alive", "true");
}


void setupMqtt() {
    mqttClient.setServer(MQTT_IP, MQTT_PORT);
    mqttClient.setCallback(onMQTTMessage);
}
//#endregion

//#region WiFi
void setupWifi() {
    Serial.print("Connecting to WIFI_SSID: ");
    Serial.println(WIFI_SSID);

    WiFi.begin(WIFI_SSID, WIFI_PASS);
    WiFi.setHostname(("ESP32-" + esp_id_str).c_str());

    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(1000);
    }

    Serial.print("Connected to ");
    Serial.println(WIFI_SSID);
}
//#endregion

void setupEspId() {
    esp_id = ESP.getEfuseMac();
    esp_id_str = String(esp_id, HEX);

    Serial.print("ESP MAC: ");
    Serial.println(esp_id_str);
}

void setup() {
    Serial.begin(9600);
    setupWifi();
    setupMqtt();
    setupEspId();

    pinMode(PIN_BUTTON, INPUT_PULLUP);
}

void onButtonPressed() {
    Serial.println("Button pressed");
    sendMQTT("button", "pressed");
}

int lastButtonState = HIGH;

void loop() {
    if (!mqttClient.connected()) {
        reconnectMQTT();
    }
    mqttClient.loop();

    int status = digitalRead(PIN_BUTTON);

    if (status == LOW && lastButtonState == HIGH) {
        // dirty but interrupts are not working due to mqtt
        onButtonPressed();
    }
    lastButtonState = status;
    delay(100);
}
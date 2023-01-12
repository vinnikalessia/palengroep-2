#include <WiFiClientSecure.h>
#include <PubSubClient.h>

#define SSID "telenet-60138"
#define PASS "UnRVkkuEmBt0"
#define MQTT_IP "192.168.0.250"
#define MQTT_PORT 1883

const char *ssid = SSID;
const char *wifipassword = PASS;

uint64_t esp_id;
String esp_id_str;

WiFiClient wifi;

PubSubClient mqttClient(wifi);

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

void sendMQTTMessage(const String &message) {

    const String& payload = message;
    String topic = "unit/" + esp_id_str + "/message";

    Serial.print("Publish message: ");
    Serial.println(payload);
    mqttClient.publish(topic.c_str(), payload.c_str());
}

void sendMQTTAliveMessage() {
    String payload = "Im alive!!!!";
    String topic = "unit/" + esp_id_str + "/alive";

    Serial.print("Publish message: ");
    Serial.println(payload);
    mqttClient.publish(topic.c_str(), payload.c_str());
}

void setupWifi() {
    Serial.print("Connecting to SSID: ");
    Serial.println(ssid);

    WiFi.begin(ssid, wifipassword);

    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(1000);
    }

    Serial.print("Connected to ");
    Serial.println(ssid);
}

void setupMqtt() {
    mqttClient.setServer(MQTT_IP, MQTT_PORT);
    mqttClient.setCallback(onMQTTMessage);
}

void reconnect() {
    // Loop until we're reconnected
    while (!mqttClient.connected()) {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (mqttClient.connect("ESP32Client")) {
            Serial.println("connected");
            // Subscribe
            mqttClient.subscribe("esp32/output");
            sendMQTTAliveMessage();
        } else {
            Serial.print("failed, rc=");
            Serial.print(mqttClient.state());
            Serial.println(" try again in 5 seconds");
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}


void setup() {
    Serial.begin(9600);
    setupWifi();
    setupMqtt();

    esp_id = ESP.getEfuseMac();
    esp_id_str = String(esp_id, HEX);

    Serial.print("ESP MAC: ");
    Serial.println(esp_id_str);
}

void loop() {
    if (!mqttClient.connected()) {
        reconnect();
    }
    mqttClient.loop();

    // Publish a message
    sendMQTTMessage("Ping");
    delay(2000);
}
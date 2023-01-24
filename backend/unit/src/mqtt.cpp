#include <PubSubClient.h>

#include "mqtt.h"

#define ESP_ID          String(ESP.getEfuseMac(), HEX)

MQTTService::MQTTService(const char *apSSID,
                         const char *apPASS,
                         const char *mqttIP,
                         int mqttPort,
                         const std::function<void(String, String)> &handleMessage) {
    wifi_ssid = apSSID;
    wifi_pass = apPASS;
    mqtt_ip = mqttIP;
    mqtt_port = mqttPort;

    handleMQTTMessage = handleMessage;


//    mqttClient = PubSubClient(wifi);
}

void MQTTService::setup() {

    setupWifi();
    setupMqtt();
}


void MQTTService::loop() {
    if (!mqttClient.connected()) {
        Serial.println("loop1");
        reconnect();
    }
    mqttClient.loop();
}


void MQTTService::reconnect() {
    // Loop until we're reconnected
    while (!mqttClient.connected()) {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (mqttClient.connect(ESP_ID.c_str())) {
            Serial.println("connected");

            subscribeToTopics();
            Serial.println("Subscribed to topics");
        } else {
            Serial.print("failed, rc=");
            Serial.print(mqttClient.state());
            Serial.println(" try again in 5 seconds");
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}

void MQTTService::setupWifi() const {
    Serial.print("Connecting to SSID: ");
    Serial.println(wifi_ssid);

    WiFi.begin(wifi_ssid, wifi_pass);

    while (WiFiClass::status() != WL_CONNECTED) {
        Serial.print(".");
        delay(1000);
    }

    Serial.print("Connected to ");
    Serial.println(wifi_ssid);
}

void MQTTService::setupMqtt() {
    mqttClient.setServer(mqtt_ip, mqtt_port);

    std::function<void(char *, byte *, unsigned int)> lambda =
            [this](char *topic, byte *message, unsigned int length) {
                onMQTTMessage(topic, message, length);
            };

    mqttClient.setCallback(lambda);
    subscribeToTopics();
}

void MQTTService::subscribeToTopics() {
    mqttClient.subscribe("notification/+");
    mqttClient.subscribe("configure/+");

    String my_command = "command/" + ESP_ID + "/#";
    mqttClient.subscribe(my_command.c_str());
    mqttClient.subscribe("command/all/light");
}

void MQTTService::sendMQTTMessage(const String &topic, const String &message) {

    const String &payload = message;

    Serial.print("Publish message: ");
    Serial.println(payload);
    mqttClient.publish(topic.c_str(), payload.c_str());
}


void MQTTService::logMQTT(const String &message) {
    String topic = "unit/" + ESP_ID + "/log";

    sendMQTTMessage(topic, message);
}

void MQTTService::sendMQTTAliveMessage() {
    String topic = "unit/" + ESP_ID + "/alive";

    sendMQTTMessage(topic, ESP_ID);
}

void MQTTService::onMQTTMessage(char *topic, byte *message, unsigned int length) const {
    String str_topic = String(topic);

    Serial.print("Message arrived on topic: ");
    Serial.print(topic);
    Serial.print(". Message: ");
    String messageTemp;

    for (int i = 0; i < length; i++) {
        Serial.print((char) message[i]);
        messageTemp += (char) message[i];
    }
    Serial.println();

    handleMQTTMessage(str_topic, messageTemp);
}

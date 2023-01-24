#ifndef MQTTSERVICE_H
#define MQTTSERVICE_H

#include <WiFi.h>
#include <PubSubClient.h>

class MQTTService {
private:
    WiFiClient wifi;
    PubSubClient mqttClient;

    const std::function<void(String, String)> handleMQTTMessage;
    const char *wifi_ssid;
    const char *wifi_pass;
    const char *mqtt_ip;
    int mqtt_port;

    void setupWifi();
    void setupMqtt();
    void subscribeToTopics();
    void reconnect();
    void onMQTTMessage(char *topic, byte *message, unsigned int length);

public:
    MQTTService(const String &wifi_ssid,
                const String &wifi_pass,
                const String &mqtt_ip,
                int mqtt_port,
                const std::function<void(String, String)> &handleMQTTMessage);

    void loop();
};

#endif

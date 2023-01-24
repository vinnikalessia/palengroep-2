#ifndef MQTTSERVICE_H
#define MQTTSERVICE_H

#include <WiFi.h>
#include <PubSubClient.h>

class MQTTService {
public:

    WiFiClient wifi;
    PubSubClient mqttClient = PubSubClient(wifi);

    std::function<void(String, String)> handleMQTTMessage;
    const char *wifi_ssid;
    const char *wifi_pass;
    const char *mqtt_ip;
    int mqtt_port;

    void setupWifi() const;

    void setupMqtt();

    void subscribeToTopics();

    void reconnect();

    void onMQTTMessage(char *topic, byte *message, unsigned int length) const;


    MQTTService(const char *wifi_ssid,
                const char *wifi_pass,
                const char *mqtt_ip,
                int mqtt_port,
                const std::function<void(String, String)> &handleMQTTMessage);

    void loop();

    void setup();

    void sendMQTTMessage(const String &topic, const String &message);

    void logMQTT(const String &message);

    void sendMQTTAliveMessage();

};

#endif

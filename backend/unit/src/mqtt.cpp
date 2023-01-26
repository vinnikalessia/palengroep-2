#include <WiFiClientSecure.h>
#include <PubSubClient.h>


#define ESP_ID          String(ESP.getEfuseMac(), HEX)

class MQTTService {
    WiFiClient wifi;
    PubSubClient mqttClient;

    std::function<void(char*, char*)> handleMQTTMessage;
    const char *wifi_ssid;
    const char *wifi_pass;
    const char *mqtt_ip;
    int mqtt_port;
public:
    MQTTService(const char *apSSID,
                const char *apPASS,
                const char *mqttIP,
                int mqttPort,
                const std::function<void(char*, char*)> &handleMessage) {
        wifi_ssid = apSSID;
        wifi_pass = apPASS;
        mqtt_ip = mqttIP;
        mqtt_port = mqttPort;

        handleMQTTMessage = handleMessage;


        mqttClient = PubSubClient(wifi);


    }

    void setup() {

        setupWifi();
        setupMqtt();
    }


    void loop() {
        if (!mqttClient.connected()) {
            reconnect();
        }
        mqttClient.loop();
    }


    void reconnect() {
        // Loop until we're reconnected
        while (!mqttClient.connected()) {
            Serial.print("Attempting MQTT connection...");
            // Attempt to connect
            if (mqttClient.connect(ESP_ID.c_str())) {
                Serial.println("connected");

                subscribeToTopics();
            } else {
                Serial.print("failed, rc=");
                Serial.print(mqttClient.state());
                Serial.println(" try again in 5 seconds");
                // Wait 5 seconds before retrying
                delay(5000);
            }
        }
    }

    void setupWifi() {
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

    void setupMqtt() {
        mqttClient.setServer(mqtt_ip, mqtt_port);

        std::function<void(char *, byte *, unsigned int)> lambda =
                [this](char *topic, byte *message, unsigned int length) {
                    onMQTTMessage(topic, message, length);
                };

        mqttClient.setCallback(lambda);
        subscribeToTopics();
    }

    void subscribeToTopics() {
        mqttClient.subscribe("notification/+");
        mqttClient.subscribe("configure/+");

        String my_command = "command/" + ESP_ID + "/#";
        mqttClient.subscribe(my_command.c_str());
        mqttClient.subscribe("command/all/light");
    }

    void sendMQTTMessage(const String &topic, const String &message) {

        const String &payload = message;

        Serial.print("Publish message: ");
        Serial.println(payload);
        mqttClient.publish(topic.c_str(), payload.c_str());
    }


    void logMQTT(const String &message) {
        String topic = "unit/" + ESP_ID + "/log";

        sendMQTTMessage(topic, message);
    }

    void sendMQTTAliveMessage() {
        String topic = "unit/" + ESP_ID + "/alive";

        sendMQTTMessage(topic, ESP_ID);
    }

    void onMQTTMessage(char *topic, byte *message, unsigned int length) {
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

        handleMQTTMessage(str_topic.c_str(), messageTemp.c_str());
    }
};
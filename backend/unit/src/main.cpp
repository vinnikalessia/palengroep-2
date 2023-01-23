#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>

#define SSID "interactieve-palen-ap"
#define PASS "roottoor"
#define MQTT_IP "10.42.0.1"
#define MQTT_PORT 1883
#define PIN_NEO_PIXEL  4   // Arduino pin that connects to NeoPixel
#define NUM_PIXELS     10  // The number of LEDs (pixels) on NeoPixel

const char *ssid = SSID;
const char *wifipassword = PASS;

uint64_t esp_id;
String esp_id_str;

WiFiClient wifi;

Adafruit_NeoPixel NeoPixel(NUM_PIXELS, PIN_NEO_PIXEL, NEO_GRB + NEO_KHZ800);

PubSubClient mqttClient(wifi);

void sendMQTTMessage(const String &topic, const String &message) {

    const String &payload = message;
//    String topic = "unit/" + esp_id_str + "/message";

    Serial.print("Publish message: ");
    Serial.println(payload);
    mqttClient.publish(topic.c_str(), payload.c_str());
}

void sendMQTTMessage(const String &message) {
    String topic = "unit/" + esp_id_str + "/message";

    sendMQTTMessage(topic, message);
}

void sendMQTTAliveMessage() {
    String topic = "unit/" + esp_id_str + "/alive";

    sendMQTTMessage(topic, esp_id_str);
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

    if (str_topic == "notification/general") {
        if (messageTemp == "GAME_START_NOTIFICATION") {
            sendMQTTAliveMessage();
            Serial.println("send alive message");
        }
    } else if (str_topic.startsWith("command/")) {
        String text = "received command: " + messageTemp;
        Serial.println(text.c_str());
    }
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

void subscribeToMQTT() {
    mqttClient.subscribe("notification/+");
    mqttClient.subscribe("configure/+");

    String my_command = "command/" + esp_id_str + "/#";
    mqttClient.subscribe(my_command.c_str());
    mqttClient.subscribe("command/all/light");
}

void setupMqtt() {
    mqttClient.setServer(MQTT_IP, MQTT_PORT);
    mqttClient.setCallback(onMQTTMessage);
    subscribeToMQTT();
}

void reconnect() {
    // Loop until we're reconnected
    while (!mqttClient.connected()) {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (mqttClient.connect("ESP32Client")) {
            Serial.println("connected");

            subscribeToMQTT();
        } else {
            Serial.print("failed, rc=");
            Serial.print(mqttClient.state());
            Serial.println(" try again in 5 seconds");
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}

void NeoPixelLeds(int red, int green, int blue){
  // turn on all pixels to red at the same time for two seconds
      for (int pixel = 0; pixel < NUM_PIXELS; pixel++) { // for each pixel
        if((pixel % 2) == 0){
          NeoPixel.setPixelColor(pixel, NeoPixel.Color(red, green, blue)); // it only takes effect if pixels.show() is called
        }
      }
      NeoPixel.show(); // send the updated pixel colors to the NeoPixel hardware.
}


void setup() {
    Serial.begin(9600);
    NeoPixel.begin();
    setupWifi();
    setupMqtt();

    esp_id = ESP.getEfuseMac();
    esp_id_str = String(esp_id, HEX);

    Serial.print("ESP MAC: ");
    Serial.println(esp_id_str);
    delay(1000);
}

void loop() {
    if (!mqttClient.connected()) {
        reconnect();
    }
    mqttClient.loop();

    NeoPixel.clear(); // set all pixel colors to 'off'. It only takes effect if pixels.show() is called

    if(btnPrevState == 0){
        NeoPixelLeds(255,0,0);
    }
    else{
        NeoPixel.clear();
        NeoPixel.show();
    }

    // Publish a message
//    sendMQTTMessage("Ping");
//    delay(1000);
}
#include <Adafruit_NeoPixel.h>

#include "mqtt.h"
#include "neopixel.h"

#define ESP_ID          String(ESP.getEfuseMac(), HEX)

#define WIFI_SSID       "interactieve-palen-ap"
#define WIFI_PASS       "roottoor"
#define MQTT_IP         "10.42.0.1"
#define MQTT_PORT       1883

#define PIN_NEO_PIXEL   4
#define NUM_PIXELS      10

#define PIN_BUTTON      15

bool lastButtonState = HIGH;

void handleMQTTMessage(const String &topic, const String &message);

MQTTService mqttService(WIFI_SSID, WIFI_PASS, MQTT_IP, MQTT_PORT, handleMQTTMessage);
NeoPixel NeoPixel(NUM_PIXELS, PIN_NEO_PIXEL);


void splitCommandStringToRGB(const String &rgb, int &r, int &g, int &b) {
    // receives in format "on 255 255 255"
    int firstSpace = rgb.indexOf(' ');
    int secondSpace = rgb.indexOf(' ', firstSpace + 1);
    int thirdSpace = rgb.indexOf(' ', secondSpace + 1);


    // this works because of pointer-fuckery and passing by reference
    r = rgb.substring(firstSpace + 1, secondSpace).toInt();
    g = rgb.substring(secondSpace + 1, thirdSpace).toInt();
    b = rgb.substring(thirdSpace + 1).toInt();
}

void handleCommandMessage(const String &topic, const String &command) {
    if (topic.endsWith("/light")) {
        if (command.startsWith("off")) {
            NeoPixel.turnOff();
            mqttService.logMQTT("set light to off");
        } else if (command.startsWith("on")) {
            int r, g, b;
            splitCommandStringToRGB(command, r, g, b);
            NeoPixel.turnOn(r, g, b);
            mqttService.logMQTT("set light to on with rgb: " + String(r) + " " + String(g) + " " + String(b));
        }
    }
}

void handleMQTTMessage(const String &topic, const String &message) {
    if (topic == "notification/general") {
        if (message == "GAME_START_NOTIFICATION") {
            mqttService.sendMQTTAliveMessage();
        }
    } else if (topic.startsWith("command/")) {
        String text = "received command: " + message;
        Serial.println(text.c_str());
        handleCommandMessage(topic, message);
    }
}

void setup() {
    Serial.begin(9600);
    Serial.print("ESP MAC: ");
    Serial.println(ESP_ID);

    mqttService.setup();
    pinMode(PIN_BUTTON, INPUT_PULLUP);

    delay(1000);
}

void onButtonPressed() {
    Serial.println("Button pressed");
    mqttService.sendMQTTMessage("action", "button_pressed");
}


void loop() {
    mqttService.loop();
    Serial.println("loop");
    /*int status = digitalRead(PIN_BUTTON);

    if (status == LOW && lastButtonState == HIGH) {
        // dirty but interrupts are not working due to mqtt
        onButtonPressed();
    }
    lastButtonState = status;
    delay(100);*/
}
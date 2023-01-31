#include <Adafruit_NeoPixel.h>
#include <WiFiClient.h>
#include <WiFi.h>

#include "PubSubClient.h"

#define ESP_ID          String("oranjevisjes")

#define ESP_TOPIC       ("unit/" + ESP_ID)


#define WIFI_SSID       "interactieve-palen-ap"
#define WIFI_PASS       "roottoor"
#define MQTT_IP         "10.42.0.1"
#define MQTT_PORT       1883

#define PIN_NEO_PIXEL   4
#define NUM_PIXELS      12

#define PIN_BUTTON      17


const char *wifi_ssid = WIFI_SSID;
const char *wifi_pass = WIFI_PASS;
const char *mqtt_ip = MQTT_IP;
int mqtt_port = MQTT_PORT;

WiFiClient wifi;
PubSubClient mqttClient(wifi);


enum class OnPress {
    ON,
    OFF,
    CONTINUE
};

OnPress onPress = OnPress::ON;
Adafruit_NeoPixel neoPixel = Adafruit_NeoPixel(NUM_PIXELS, PIN_NEO_PIXEL, NEO_BRG + NEO_KHZ400);

void turnOn(int red, int green, int blue) {
    unsigned int color = neoPixel.Color(red, green, blue);

    for (int pixel = 0; pixel < NUM_PIXELS; pixel++) {
        if ((pixel % 2) == 0) {
            neoPixel.setPixelColor(pixel, color);
        }
    }
//    neoPixel.fill(color, 0, 10);

    neoPixel.show();


}

void turnOff() {
    neoPixel.clear();
    neoPixel.show();
}

void splitCommandStringToRGB(const String &rgb, int &r, int &g, int &b) {
    // receives in format "on 255 255 255"
    int firstSpace = rgb.indexOf(' ');
    int secondSpace = rgb.indexOf(' ', firstSpace + 1);
    int thirdSpace = rgb.indexOf(' ', secondSpace + 1);


    // this works because of pointer-fuckery and passing by reference
    r = rgb.substring(firstSpace + 1, secondSpace).toInt();
    g = rgb.substring(secondSpace + 1, thirdSpace).toInt();
    b = rgb.substring(thirdSpace + 1).toInt();

    if (r > 255)
        r = 255;
    if (g > 255)
        g = 255;
    if (b > 255)
        b = 255;
}


void sendMQTTMessage(const String &topic, const String &message) {

    const String &payload = message;

//    Serial.println("sending message: " + topic + " - " + payload);
    mqttClient.publish(topic.c_str(), payload.c_str());
}

void log(const String &message) {


    String topic = ESP_TOPIC + "/log";

    Serial.println(message);
    sendMQTTMessage(topic, message);
}

void handleCommandMessage(const String &topic, const String &command) {
    if (topic.endsWith("/light")) {
        if (command.startsWith("off")) {
            turnOff();
            log("set light to off");
        } else if (command.startsWith("on")) {
            log("HEREEE");
            int r, g, b;
            splitCommandStringToRGB(command, r, g, b);
            log("set light to on with rgb: " + String(r) + " " + String(g) + " " + String(b));
            turnOn(r, g, b);
        }
    }
}

void handleConfigureMessage(const String &topic, const String &command) {
    if (topic.endsWith("on_press")) {
        if (command == "led_off") {
            onPress = OnPress::OFF;
            log("set on_press to led_off");
        } else if (command == "led_on") {
            onPress = OnPress::ON;
            log("set on_press to led_on");
        } else if (command == "led_continue") {
            onPress = OnPress::CONTINUE;
            log("set on_press to continue");
        }
    }
}

void subscribeToTopics() {
    mqttClient.subscribe("notification/+");
    mqttClient.subscribe("configure/+");

    String my_command = "command/" + ESP_ID + "/#";
    mqttClient.subscribe(my_command.c_str());
    mqttClient.subscribe("command/all/light");
}

void sendMQTTAliveMessage() {
    String topic = "unit/" + ESP_ID + "/alive";

    sendMQTTMessage(topic, ESP_ID);
}

void handleMQTTMessage(const String &topic, const String &message) {
    if (topic == "notification/general") {
        if (message == "GAME_START_NOTIFICATION") {
            sendMQTTAliveMessage();
        }
    } else if (topic.startsWith("command/")) {
        String text = "received command: " + message;
        log(text.c_str());
        handleCommandMessage(topic, message);
    } else if (topic.startsWith("configure/")) {
        String text = "received configure: " + message;
        log(text.c_str());
        handleConfigureMessage(topic, message);
    }
}

void onMQTTMessage(char *topic, byte *payload, unsigned int length) {

    String topicString = String(topic);
    String tempMessage = "";

    for (int i = 0; i < length; i++) {
        tempMessage += (char) payload[i];
    }

    log("received message: " + topicString + " - " + tempMessage);
    handleMQTTMessage(topicString, tempMessage);
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

void setupMQTT() {
    setupWifi();

    mqttClient.setServer(mqtt_ip, mqtt_port);
    mqttClient.setCallback(onMQTTMessage);
    subscribeToTopics();
}


void reconnectMQTT() {
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

void onBtnPress() {
    if (onPress == OnPress::ON) {
        turnOn(255,105,180);
    } else if (onPress == OnPress::OFF) {
        turnOff();
    } else {

    }

    sendMQTTMessage(ESP_TOPIC + "/action", "button pressed");
    log("button pressed");
}

void setup() {
    Serial.begin(9600);
    Serial.print("ESP MAC: ");
    Serial.println(ESP_ID);


    pinMode(PIN_BUTTON, INPUT_PULLUP);

    Serial.println("im here");
    neoPixel.begin();
//    neoPixel.setBrightness(10);
    neoPixel.clear();
    neoPixel.show();
    Serial.println("fml");

    setupMQTT();
    delay(1000);
}

int btnPrevState = 0;


bool a = 0;

void loop() {

    if (!mqttClient.connected()) {
        turnOn(0, 0, 128);
        reconnectMQTT();
    }
    mqttClient.loop();

//    NeoPixel.clear(); // set all pixel colors to 'off'. It only takes effect if pixels.show() is called
//

    int currentBtnState = digitalRead(PIN_BUTTON);


    if (btnPrevState == 1 && currentBtnState == 0) {
        Serial.println("neopixel on");
        onBtnPress();
    } else {
//        neoPixel.turnOff();
    }

    btnPrevState = currentBtnState;
//    delay(10);

}
#include "neopixel.h"

#include <Adafruit_NeoPixel.h>

NeoPixel::NeoPixel(short pin, short count) : neoPixel(count, pin, NEO_GRB + NEO_KHZ800) {
    neoPixelCount = count;
}

void NeoPixel::setup() {
    neoPixel.begin();
    neoPixel.show();
}

void NeoPixel::turnOn(int red, int green, int blue) {
    unsigned int color = Adafruit_NeoPixel::Color(red, green, blue);

    for (short pixel = 0; pixel < neoPixelCount; pixel++) {
        if ((pixel % 2) == 0) {
            neoPixel.setPixelColor(pixel, color);
        }
    }
    neoPixel.show();
}

void NeoPixel::turnOff() {
    neoPixel.clear();
    neoPixel.show();
}
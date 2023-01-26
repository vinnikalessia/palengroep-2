#ifndef NEOPIXEL_H
#define NEOPIXEL_H

#include <Adafruit_NeoPixel.h>

class NeoPixel {
private:
    Adafruit_NeoPixel neoPixel;
    short neoPixelCount;

public:
    NeoPixel(short pin, short count);

    void setup();

    void turnOn(int red, int green, int blue);

    void turnOff();
};

#endif
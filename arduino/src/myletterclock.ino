// Date and time functions using a DS1307 RTC connected via I2C and Wire lib
#include <Wire.h>
#include "RTClib.h"
#include "Adafruit_NeoPixel.h"
RTC_DS1307 rtc;
//define the data pin
#define PIN 10
//define number of pixels
#define NUMPIXEL 144
// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXEL, PIN, NEO_GRB | NEO_KHZ800);

unsigned int i = 0;

void setup () {
    Serial.begin(57600);
#ifdef AVR
    Wire.begin();
#else
    Wire1.begin(); // Shield I2C pins connect to alt I2C bus on Arduino Due
#endif
    rtc.begin();
    if (! rtc.isrunning()) {
        Serial.println("RTC is NOT running!");
        // following line sets the RTC to the date & time this sketch was compiled
        rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
        // This line sets the RTC with an explicit date & time, for example to set
        // January 21, 2014 at 3am you would call:
        // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
    }
    strip.begin();                  // Initialize NeoPixel object
    strip.show();                   // Initialize all pixels to '}ff'
}
void loop () {
    DateTime now = rtc.now();
    Serial.print(now.year(), DEC);
    Serial.print('/');
    Serial.print(now.month(), DEC);
    Serial.print('/');
    Serial.print(now.day(), DEC);
    Serial.print(' ');
    Serial.print(now.hour(), DEC);
    Serial.print(':');
    Serial.print(now.minute(), DEC);
    Serial.print(':');
    Serial.print(now.second(), DEC);
    Serial.println();
    Serial.print(" since midnight 1/1/1970 = ");
    Serial.print(now.unixtime());
    Serial.print("s = ");
    Serial.print(now.unixtime() / 86400L);
    Serial.println("d");
    // calculate a date which is 7 days and 30 seconds into the future
    DateTime future (now.unixtime() + 7 * 86400L + 30);
    Serial.print(" now + 7d + 30s: ");
    Serial.print(future.year(), DEC);
    Serial.print('/');
    Serial.print(future.month(), DEC);
    Serial.print('/');
    Serial.print(future.day(), DEC);
    Serial.print(' ');
    Serial.print(future.hour(), DEC);
    Serial.print(':');
    Serial.print(future.minute(), DEC);
    Serial.print(':');
    Serial.print(future.second(), DEC);
    Serial.println();
    Serial.println();
    uint32_t color = 0;
    color = strip.Color(0,0,0);
    for(int j = 0; j < NUMPIXEL; j++)
    {
        strip.setPixelColor(j,color);
    }
    color = strip.Color(50,50,50);
    strip.setPixelColor(i++,color);
    strip.setPixelColor(6,color);
    strip.setPixelColor(7,color);
    strip.setPixelColor(8,color);
    strip.setPixelColor(9,color);
    strip.setPixelColor(10,color);
    strip.setPixelColor(11,color);
    strip.setPixelColor(31,color);
    strip.setPixelColor(32,color);
    strip.setPixelColor(33,color);
    strip.setPixelColor(34,color);
    strip.setPixelColor(77,color);
    strip.setPixelColor(78,color);
    strip.setPixelColor(79,color);
    strip.setPixelColor(97,color);
    strip.setPixelColor(98,color);
    strip.setPixelColor(99,color);
    strip.setPixelColor(100,color);
    strip.setPixelColor(101,color);
    strip.setPixelColor(102,color);
    strip.setPixelColor(103,color);
    strip.setPixelColor(132,color);
    strip.setPixelColor(133,color);
    strip.setPixelColor(138,color);
    strip.setPixelColor(139,color);
    strip.setPixelColor(140,color);
    strip.show();
    delay(3000);
}

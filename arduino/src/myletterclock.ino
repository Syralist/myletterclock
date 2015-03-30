// Date and time functions using a DS1307 RTC connected via I2C and Wire lib
#include <Wire.h>
#include "RTClib.h"
#include "Adafruit_NeoPixel.h"
#include "TimerOne.h"

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

typedef uint32_t Color;
Color cBlack = 0;
Color cWhite = 0;
Color cRed = 0;
Color cGreen = 0;
Color cBlue = 0;

/* void lightHalb(Color color); */

void setup ()
{
    Timer1.initialize(1000000);       // Initialize timer to 1s
    Timer1.attachInterrupt(checktime);  // Attach funciton checktime to timer interupt   
    Serial.begin(57600);
#ifdef AVR
    Wire.begin();
#else
    Wire1.begin(); // Shield I2C pins connect to alt I2C bus on Arduino Due
#endif
    rtc.begin();
    if (! rtc.isrunning())
    {
        Serial.println("RTC is NOT running!");
        // following line sets the RTC to the date & time this sketch was compiled
        rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
        // This line sets the RTC with an explicit date & time, for example to set
        // January 21, 2014 at 3am you would call:
        // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
    }
    strip.begin();                  // Initialize NeoPixel object
    strip.show();                   // Initialize all pixels to '}ff'

    // define global colors
    cBlack = strip.Color(0,0,0);
    cWhite = strip.Color(127,127,127);
    cRed = strip.Color(127,0,0);
    cGreen = strip.Color(0,127,0);
    cBlue = strip.Color(0,0,127);
}

void loop ()
{
    /* DateTime now = rtc.now(); */
    /* Serial.print(now.year(), DEC); */
    /* Serial.print('/'); */
    /* Serial.print(now.month(), DEC); */
    /* Serial.print('/'); */
    /* Serial.print(now.day(), DEC); */
    /* Serial.print(' '); */
    /* Serial.print(now.hour(), DEC); */
    /* Serial.print(':'); */
    /* Serial.print(now.minute(), DEC); */
    /* Serial.print(':'); */
    /* Serial.print(now.second(), DEC); */
    /* Serial.println(); */
    /* Serial.print(" since midnight 1/1/1970 = "); */
    /* Serial.print(now.unixtime()); */
    /* Serial.print("s = "); */
    /* Serial.print(now.unixtime() / 86400L); */
    /* Serial.println("d"); */
    /* // calculate a date which is 7 days and 30 seconds into the future */
    /* DateTime future (now.unixtime() + 7 * 86400L + 30); */
    /* Serial.print(" now + 7d + 30s: "); */
    /* Serial.print(future.year(), DEC); */
    /* Serial.print('/'); */
    /* Serial.print(future.month(), DEC); */
    /* Serial.print('/'); */
    /* Serial.print(future.day(), DEC); */
    /* Serial.print(' '); */
    /* Serial.print(future.hour(), DEC); */
    /* Serial.print(':'); */
    /* Serial.print(future.minute(), DEC); */
    /* Serial.print(':'); */
    /* Serial.print(future.second(), DEC); */
    /* Serial.println(); */
    /* Serial.println(); */
    /* uint32_t color = 0; */
    /* color = strip.Color(0,0,0); */
    /* for(int j = 0; j < NUMPIXEL; j++) */
    /* { */
    /*     strip.setPixelColor(j,color); */
    /* } */
    /* color = strip.Color(50,50,50); */
    /* strip.setPixelColor(i++,color); */
    /* strip.setPixelColor(6,color); */
    /* strip.setPixelColor(7,color); */
    /* strip.setPixelColor(8,color); */
    /* strip.setPixelColor(9,color); */
    /* strip.setPixelColor(10,color); */
    /* strip.setPixelColor(11,color); */
    /* strip.setPixelColor(31,color); */
    /* strip.setPixelColor(32,color); */
    /* strip.setPixelColor(33,color); */
    /* strip.setPixelColor(34,color); */
    /* strip.setPixelColor(77,color); */
    /* strip.setPixelColor(78,color); */
    /* strip.setPixelColor(79,color); */
    /* strip.setPixelColor(97,color); */
    /* strip.setPixelColor(98,color); */
    /* strip.setPixelColor(99,color); */
    /* strip.setPixelColor(100,color); */
    /* strip.setPixelColor(101,color); */
    /* strip.setPixelColor(102,color); */
    /* strip.setPixelColor(103,color); */
    /* strip.setPixelColor(132,color); */
    /* strip.setPixelColor(133,color); */
    /* strip.setPixelColor(138,color); */
    /* strip.setPixelColor(139,color); */
    /* strip.setPixelColor(140,color); */
    /* strip.show(); */
    /* delay(3000); */
}

void checktime()
{
    DateTime now = rtc.now();
    int hour = now.hour();
    int minute = now.minute();
    int minutemod5 = minute % 5;
    int second = now.second();
    Color cBackground = cBlack;
    Color cForeground = cWhite;
    for(int j = 0; j < NUMPIXEL; j++)
    {
        strip.setPixelColor(j,cBackground);
    }
    lightEs(cForeground);
    if((minutemod5 == 1 || minutemod5 == 2) && (minute != 0))
    {
        lightWar(cForeground);
    }
    if(minutemod5 == 0 || minutemod5 == 3 || minutemod5 == 4)
    {
        lightIst(cForeground);
    }
    if(minutemod5 == 3 || minutemod5 == 4)
    {
        lightGleich(cForeground);
    }
    if(minute == 0)
    {
        lightGenau(cForeground);
    }
    if((minutemod5 == 0 || minutemod5 == 1 || minutemod5 == 2) && (minute != 0))
    {
        lightGerade(cForeground);
    }
    if((minute >= 3 && minute <= 7) || 
            (minute >= 23 && minute <= 27) || 
            (minute >= 33 && minute <= 37) ||
            (minute >= 53 && minute <= 57))
    {
        lightFuenf1(cForeground);
    }
    if((minute >= 13 && minute <= 17) || 
            (minute >= 43 && minute <= 47))
    {
        lightViertel(cForeground);
    }
    if((minute >= 8 && minute <= 12) || 
            (minute >= 48 && minute <= 52))
    {
        lightZehn1(cForeground);
    }
    if((minute >= 18 && minute <= 22) || 
            (minute >= 38 && minute <= 42))
    {
        lightZwanzig(cForeground);
    }
    if((minute >= 3 && minute <= 22) || 
            (minute >= 33 && minute <= 37))
    {
        lightNach1(cForeground);
    }
    if((minute >= 23 && minute <= 27) || 
            (minute >= 38 && minute <= 57))
    {
        lightVor1(cForeground);
    }
    if(minute >= 23 && minute <= 37)
    {
        lightHalb(cForeground);
    }
    if(((hour ==  1 || hour == 13) && minute <= 22) || 
            ((hour ==  0 || hour == 12) && minute >= 23))
    {
        lightEins(cForeground);
    }
    if(((hour ==  2 || hour == 14) && minute <= 22) || 
            ((hour ==  1 || hour == 13) && minute >= 23))
    {
        lightZwei(cForeground);
    }
    if(((hour ==  3 || hour == 15) && minute <= 22) || 
            ((hour ==  2 || hour == 14) && minute >= 23))
    {
        lightDrei(cForeground);
    }
    if(((hour ==  4 || hour == 16) && minute <= 22) || 
            ((hour ==  3 || hour == 15) && minute >= 23))
    {
        lightVier(cForeground);
    }
    if(((hour ==  5 || hour == 17) && minute <= 22) || 
            ((hour ==  4 || hour == 16) && minute >= 23))
    {
        lightFuenf2(cForeground);
    }
    if(((hour ==  6 || hour == 18) && minute <= 22) || 
            ((hour ==  5 || hour == 17) && minute >= 23))
    {
        lightSechs(cForeground);
    }
    if(((hour ==  7 || hour == 19) && minute <= 22) || 
            ((hour ==  6 || hour == 18) && minute >= 23))
    {
        lightSieben(cForeground);
    }
    if(((hour ==  8 || hour == 20) && minute <= 22) || 
            ((hour ==  7 || hour == 19) && minute >= 23))
    {
        lightAcht(cForeground);
    }
    if(((hour ==  9 || hour == 21) && minute <= 22) || 
            ((hour ==  8 || hour == 20) && minute >= 23))
    {
        lightNeun(cForeground);
    }
    if(((hour ==  10 || hour == 22) && minute <= 22) || 
            ((hour ==  9 || hour == 21) && minute >= 23))
    {
        lightZehn2(cForeground);
    }
    if(((hour ==  11 || hour == 23) && minute <= 22) || 
            ((hour ==  10 || hour == 22) && minute >= 23))
    {
        lightElf(cForeground);
    }
    if(((hour ==  12 || hour == 0) && minute <= 22) || 
            ((hour ==  11 || hour == 23) && minute >= 23))
    {
        lightZwoelf(cForeground);
    }
    if(minute >= 58 || minute <= 2)
    {
        lightUhr(cForeground);
    }
    if((hour ==  5  && minute >= 23) || 
            (hour >= 6 && hour <= 10) ||
            (hour ==  11  && minute <= 22))
    {
        lightVor2(cForeground);
        lightMittag(cForeground);
    }
    if((hour ==  12  && minute >= 23) || 
            (hour >= 13 && hour <= 18) ||
            (hour ==  19  && minute <= 22))
    {
        lightNach2(cForeground);
        lightMittag(cForeground);
    }
    if((hour ==  19  && minute >= 23) || 
            (hour >= 20 || hour <= 5) ||
            (hour ==  5  && minute <= 22))
    {
        lightNachts(cForeground);
    }
    if((hour ==  11  && minute >= 23) || 
            (hour ==  12  && minute <= 22))
    {
        lightMittag(cForeground);
    }
}

void lightEs(uint32_t color)
{
    strip.setPixelColor(132, color);
    strip.setPixelColor(133, color);
}

void lightWar(uint32_t color)
{
    strip.setPixelColor(135, color);
    strip.setPixelColor(136, color);
    strip.setPixelColor(137, color);
}

void lightIst(uint32_t color)
{
    strip.setPixelColor(138, color);
    strip.setPixelColor(139, color);
    strip.setPixelColor(140, color);
}

void lightGleich(uint32_t color)
{
    strip.setPixelColor(131, color);
    strip.setPixelColor(130, color);
    strip.setPixelColor(129, color);
    strip.setPixelColor(128, color);
    strip.setPixelColor(127, color);
    strip.setPixelColor(126, color);
}

void lightGenau(uint32_t color)
{
    strip.setPixelColor(124, color);
    strip.setPixelColor(123, color);
    strip.setPixelColor(122, color);
    strip.setPixelColor(121, color);
    strip.setPixelColor(120, color);
}

void lightGerade(uint32_t color)
{
    strip.setPixelColor(108, color);
    strip.setPixelColor(109, color);
    strip.setPixelColor(110, color);
    strip.setPixelColor(111, color);
    strip.setPixelColor(112, color);
    strip.setPixelColor(113, color);
}

void lightFuenf1(uint32_t color)
{
    strip.setPixelColor(115, color);
    strip.setPixelColor(116, color);
    strip.setPixelColor(117, color);
    strip.setPixelColor(118, color);
}

void lightViertel(uint32_t color)
{
    strip.setPixelColor(103, color);
    strip.setPixelColor(102, color);
    strip.setPixelColor(101, color);
    strip.setPixelColor(100, color);
    strip.setPixelColor(99, color);
    strip.setPixelColor(98, color);
    strip.setPixelColor(97, color);
}

void lightZehn1(uint32_t color)
{
    strip.setPixelColor(84, color);
    strip.setPixelColor(85, color);
    strip.setPixelColor(86, color);
    strip.setPixelColor(87, color);
}

void lightZwanzig(uint32_t color)
{
    strip.setPixelColor(88, color);
    strip.setPixelColor(89, color);
    strip.setPixelColor(90, color);
    strip.setPixelColor(91, color);
    strip.setPixelColor(92, color);
    strip.setPixelColor(93, color);
    strip.setPixelColor(94, color);
}

void lightNach1(uint32_t color)
{
    strip.setPixelColor(83, color);
    strip.setPixelColor(82, color);
    strip.setPixelColor(81, color);
    strip.setPixelColor(80, color);
}

void lightVor1(uint32_t color)
{
    strip.setPixelColor(79, color);
    strip.setPixelColor(78, color);
    strip.setPixelColor(77, color);
}

void lightHalb(uint32_t color)
{
    strip.setPixelColor(75, color);
    strip.setPixelColor(74, color);
    strip.setPixelColor(73, color);
    strip.setPixelColor(72, color);
}

void lightEins(uint32_t color)
{
    strip.setPixelColor(62, color);
    strip.setPixelColor(63, color);
    strip.setPixelColor(64, color);
    strip.setPixelColor(65, color);
}

void lightZwei(uint32_t color)
{
    strip.setPixelColor(40, color);
    strip.setPixelColor(41, color);
    strip.setPixelColor(42, color);
    strip.setPixelColor(43, color);
}

void lightDrei(uint32_t color)
{
    strip.setPixelColor(60, color);
    strip.setPixelColor(61, color);
    strip.setPixelColor(62, color);
    strip.setPixelColor(63, color);
}

void lightVier(uint32_t color)
{
    strip.setPixelColor(36, color);
    strip.setPixelColor(37, color);
    strip.setPixelColor(38, color);
    strip.setPixelColor(39, color);
}

void lightFuenf2(uint32_t color)
{
    strip.setPixelColor(57, color);
    strip.setPixelColor(56, color);
    strip.setPixelColor(55, color);
    strip.setPixelColor(54, color);
}

void lightSechs(uint32_t color)
{
    strip.setPixelColor(29, color);
    strip.setPixelColor(28, color);
    strip.setPixelColor(27, color);
    strip.setPixelColor(26, color);
    strip.setPixelColor(25, color);
}

void lightSieben(uint32_t color)
{
    strip.setPixelColor(65, color);
    strip.setPixelColor(66, color);
    strip.setPixelColor(67, color);
    strip.setPixelColor(68, color);
    strip.setPixelColor(69, color);
    strip.setPixelColor(70, color);
}

void lightAcht(uint32_t color)
{
    strip.setPixelColor(44, color);
    strip.setPixelColor(45, color);
    strip.setPixelColor(46, color);
    strip.setPixelColor(47, color);
}

void lightNeun(uint32_t color)
{
    strip.setPixelColor(34, color);
    strip.setPixelColor(33, color);
    strip.setPixelColor(32, color);
    strip.setPixelColor(31, color);
}

void lightZehn2(uint32_t color)
{
    strip.setPixelColor(12, color);
    strip.setPixelColor(13, color);
    strip.setPixelColor(14, color);
    strip.setPixelColor(15, color);
}

void lightElf(uint32_t color)
{
    strip.setPixelColor(59, color);
    strip.setPixelColor(58, color);
    strip.setPixelColor(57, color);
}

void lightZwoelf(uint32_t color)
{
    strip.setPixelColor(52, color);
    strip.setPixelColor(51, color);
    strip.setPixelColor(50, color);
    strip.setPixelColor(49, color);
    strip.setPixelColor(48, color);
}

void lightUhr(uint32_t color)
{
    strip.setPixelColor(17, color);
    strip.setPixelColor(18, color);
    strip.setPixelColor(19, color);
}

void lightVor2(uint32_t color)
{
    strip.setPixelColor(21, color);
    strip.setPixelColor(22, color);
    strip.setPixelColor(23, color);
}

void lightNach2(uint32_t color)
{
    strip.setPixelColor(11, color);
    strip.setPixelColor(10, color);
    strip.setPixelColor(9, color);
    strip.setPixelColor(8, color);
}

void lightNachts(uint32_t color)
{
    strip.setPixelColor(11, color);
    strip.setPixelColor(10, color);
    strip.setPixelColor(9, color);
    strip.setPixelColor(8, color);
    strip.setPixelColor(7, color);
    strip.setPixelColor(6, color);
}

void lightMittag(uint32_t color)
{
    strip.setPixelColor(5, color);
    strip.setPixelColor(4, color);
    strip.setPixelColor(3, color);
    strip.setPixelColor(2, color);
    strip.setPixelColor(1, color);
    strip.setPixelColor(0, color);
}

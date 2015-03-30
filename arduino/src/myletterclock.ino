// Date and time functions using a DS1307 RTC connected via I2C and Wire lib
#include <Wire.h>
#include <DS1307RTC.h>
#include <Time.h>
#include "Adafruit_NeoPixel.h"
/* #include "TimerOne.h" */
#include "DCF77.h"

#define DCF_PIN 2                // Connection pin to DCF 77 device
#define DCF_INTERRUPT 0          // Interrupt number associated with pin
DCF77 DCF = DCF77(DCF_PIN,DCF_INTERRUPT, true);

//define the data pin
#define LEDPIN 10
//define number of pixels
#define NUMPIXEL 144
// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXEL, LEDPIN, NEO_GRB | NEO_KHZ800);

unsigned int i = 0;
static unsigned long msLast = 0;

typedef uint32_t Color;
Color cBlack = 0;
Color cWhite = 0;
Color cRed = 0;
Color cGreen = 0;
Color cBlue = 0;

void setup ()
{
    /* Timer1.initialize(1000000);       // Initialize timer to 1s */
    /* Timer1.attachInterrupt(checktime);  // Attach funciton checktime to timer interupt */
    Serial.begin(57600);
    strip.begin();                  // Initialize NeoPixel object
    strip.show();                   // Initialize all pixels to '}ff'

    msLast = millis();

    DCF.Start();

    // define global colors
    cBlack = strip.Color(0,0,0);
    cWhite = strip.Color(127,127,127);
    cRed = strip.Color(127,0,0);
    cGreen = strip.Color(0,127,0);
    cBlue = strip.Color(0,0,127);
}

void loop ()
{
    unsigned long msNow = millis();
    if((msNow - msLast > 999) || (msNow < msLast)) 
    {
        msLast= millis();
        checktime();
    }
}

void checktime()
{
    tmElements_t tm;
    RTC.read(tm);
    int hour = tm.Hour;
    int minute = tm.Minute;
    int minutemod5 = minute % 5;
    int second = tm.Second;
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
    else// if(minutemod5 == 0 || minutemod5 == 3 || minutemod5 == 4)
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

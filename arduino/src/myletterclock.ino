// Date and time functions using a DS1307 RTmillis() connected via I2C and Wire lib
#include <Wire.h>
#include <Time.h>
#include <Timezone.h>
#include <DS1307RTC.h>
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

#define TIME_MSG_LEN  11   // time sync to PC is HEADER followed by unix time_t as ten ascii digits
#define TIME_HEADER  'T'   // Header tag for serial time sync message
#define TIME_REQUEST  7    // ASCII bell character requests a time sync message

//Central European Time (Frankfurt, Paris)
TimeChangeRule CEST = {"CEST", Last, Sun, Mar, 2, 120};     //Central European Summer Time
TimeChangeRule CET = {"CET ", Last, Sun, Oct, 3, 60};       //Central European Standard Time
Timezone CE(CEST, CET);
TimeChangeRule *tcr;        //pointer to the time change rule, use to get the TZ abbrev
time_t utc;

unsigned int i = 0;
static unsigned long msLast = 0;

typedef uint32_t Color;
Color cBlack = 0;
/* Color cWhite = 0x7F7F7F; */
Color cWhite = 0x555555;
Color cRed = 0x7F0000;
Color cGreen = 0x7F00;
Color cBlue = 0x7F;

void setup ()
{
    /* Timer1.initialize(1000000);       // Initialize timer to 1s */
    /* Timer1.attachInterrupt(checktime);  // Attach funciton checktime to timer interupt */
    Serial.begin(9600);
    /* setSyncProvider( requestSync);  //set function to call when sync required */


    strip.begin();                  // Initialize NeoPixel object
    strip.show();                   // Initialize all pixels to '}ff'

    msLast = millis();

    DCF.Start();

    setSyncProvider(RTC.get);
    // define global colors
    /* cBlack = strip.Color(0,0,0); */
    /* cWhite = 0x7F7F7F;//strip.Color(127,127,127); */
    /* cRed = 0x7F0000;//strip.Color(127,0,0); */
    /* cGreen = 0x7F00;//strip.Color(0,127,0); */
    /* cBlue = 0x7F;//strip.Color(0,0,127); */
}

void loop ()
{
    if(Serial.available())
    {
        processSyncMessage();
    }
    /* unsigned long msNow = millis(); */
    if((millis() - msLast > 999) || (millis() < msLast))
    {
        msLast = millis();
        i++;
        utc = now();
        displaytime(CE.toLocal(utc, &tcr));
    }
    if(i == 300)
    {
        time_t DCFtime = DCF.getTime();
        if((DCFtime != 0) && (DCFtime != now()))
        {
            RTC.set(DCFtime);
        }
    }
}

void processSyncMessage() {
    // if time sync available from serial port, update time and return true
    while(Serial.available() >=  TIME_MSG_LEN ){  // time message consists of a header and ten ascii digits
        char c = Serial.read();
        Serial.print(c);
        if( c == TIME_HEADER )
        {
            time_t pctime = 0;
            for(int i=0; i < TIME_MSG_LEN -1; i++)
            {
                c = Serial.read();
                if( c >= '0' && c <= '9')
                {
                    pctime = (10 * pctime) + (c - '0') ; // convert digits to a number
                }
            }
            RTC.set(pctime);   // Sync Arduino clock to the time received on the serial port
            Serial.print("Time set to: ");
            Serial.print(pctime);
        }
    }
}

time_t requestSync()
{
    Serial.write(TIME_REQUEST);
    return 0; // the time will be sent later in response to serial mesg
}

void displaytime(time_t t)
{
    int Hour = hour(t);
    int Minute = minute(t);
    int Second = second(t);
    int Minutemod5 = Minute % 5;
    Color cBackground = cBlack;
    Color cForeground = cWhite;
    for(int j = 0; j < NUMPIXEL; j++)
    {
        strip.setPixelColor(j,cBackground);
    }
    lightEs(cForeground);
    if((Minutemod5 == 1 || Minutemod5 == 2) && (Minute != 0))
    {
        lightWar(cForeground);
    }
    else// if(Minutemod5 == 0 || Minutemod5 == 3 || Minutemod5 == 4)
    {
        lightIst(cForeground);
    }
    if(Minutemod5 == 3 || Minutemod5 == 4)
    {
        lightGleich(cForeground);
    }
    if(Minute == 0)
    {
        lightGenau(cForeground);
    }
    if((Minutemod5 == 0 || Minutemod5 == 1 || Minutemod5 == 2) && (Minute != 0))
    {
        lightGerade(cForeground);
    }
    if((Minute >= 3 && Minute <= 7) ||
            (Minute >= 23 && Minute <= 27) ||
            (Minute >= 33 && Minute <= 37) ||
            (Minute >= 53 && Minute <= 57))
    {
        lightFuenf1(cForeground);
    }
    if((Minute >= 13 && Minute <= 17) ||
            (Minute >= 43 && Minute <= 47))
    {
        lightViertel(cForeground);
    }
    if((Minute >= 8 && Minute <= 12) ||
            (Minute >= 48 && Minute <= 52))
    {
        lightZehn1(cForeground);
    }
    if((Minute >= 18 && Minute <= 22) ||
            (Minute >= 38 && Minute <= 42))
    {
        lightZwanzig(cForeground);
    }
    if((Minute >= 3 && Minute <= 22) ||
            (Minute >= 33 && Minute <= 37))
    {
        lightNach1(cForeground);
    }
    if((Minute >= 23 && Minute <= 27) ||
            (Minute >= 38 && Minute <= 57))
    {
        lightVor1(cForeground);
    }
    if(Minute >= 23 && Minute <= 37)
    {
        lightHalb(cForeground);
    }
    if(((Hour ==  1 || Hour == 13) && Minute <= 22) ||
            ((Hour ==  0 || Hour == 12) && Minute >= 23))
    {
        lightEins(cForeground);
    }
    if(((Hour ==  2 || Hour == 14) && Minute <= 22) ||
            ((Hour ==  1 || Hour == 13) && Minute >= 23))
    {
        lightZwei(cForeground);
    }
    if(((Hour ==  3 || Hour == 15) && Minute <= 22) ||
            ((Hour ==  2 || Hour == 14) && Minute >= 23))
    {
        lightDrei(cForeground);
    }
    if(((Hour ==  4 || Hour == 16) && Minute <= 22) ||
            ((Hour ==  3 || Hour == 15) && Minute >= 23))
    {
        lightVier(cForeground);
    }
    if(((Hour ==  5 || Hour == 17) && Minute <= 22) ||
            ((Hour ==  4 || Hour == 16) && Minute >= 23))
    {
        lightFuenf2(cForeground);
    }
    if(((Hour ==  6 || Hour == 18) && Minute <= 22) ||
            ((Hour ==  5 || Hour == 17) && Minute >= 23))
    {
        lightSechs(cForeground);
    }
    if(((Hour ==  7 || Hour == 19) && Minute <= 22) ||
            ((Hour ==  6 || Hour == 18) && Minute >= 23))
    {
        lightSieben(cForeground);
    }
    if(((Hour ==  8 || Hour == 20) && Minute <= 22) ||
            ((Hour ==  7 || Hour == 19) && Minute >= 23))
    {
        lightAcht(cForeground);
    }
    if(((Hour ==  9 || Hour == 21) && Minute <= 22) ||
            ((Hour ==  8 || Hour == 20) && Minute >= 23))
    {
        lightNeun(cForeground);
    }
    if(((Hour ==  10 || Hour == 22) && Minute <= 22) ||
            ((Hour ==  9 || Hour == 21) && Minute >= 23))
    {
        lightZehn2(cForeground);
    }
    if(((Hour ==  11 || Hour == 23) && Minute <= 22) ||
            ((Hour ==  10 || Hour == 22) && Minute >= 23))
    {
        lightElf(cForeground);
    }
    if(((Hour ==  12 || Hour == 0) && Minute <= 22) ||
            ((Hour ==  11 || Hour == 23) && Minute >= 23))
    {
        lightZwoelf(cForeground);
    }
    if(Minute >= 58 || Minute <= 2)
    {
        lightUhr(cForeground);
    }
    if((Hour ==  5  && Minute >= 23) ||
            (Hour >= 6 && Hour <= 10) ||
            (Hour ==  11  && Minute <= 22))
    {
        lightVor2(cForeground);
        lightMittag(cForeground);
    }
    if((Hour ==  12  && Minute >= 23) ||
            (Hour >= 13 && Hour <= 18) ||
            (Hour ==  19  && Minute <= 22))
    {
        lightNach2(cForeground);
        lightMittag(cForeground);
    }
    if((Hour ==  19  && Minute >= 23) ||
            (Hour >= 20 || Hour <= 5) ||
            (Hour ==  5  && Minute <= 22))
    {
        lightNachts(cForeground);
    }
    if((Hour ==  11  && Minute >= 23) ||
            (Hour ==  12  && Minute <= 22))
    {
        lightMittag(cForeground);
    }
    strip.show();
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
    strip.setPixelColor(89, color);
    strip.setPixelColor(90, color);
    strip.setPixelColor(91, color);
    strip.setPixelColor(92, color);
    strip.setPixelColor(93, color);
    strip.setPixelColor(94, color);
    strip.setPixelColor(95, color);
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

import serial
ardu = serial.Serial('/dev/ttyUSB0',9600)
ardu.write('T1428413847\n')

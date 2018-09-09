'''
Howard Webb
Date: 8/2/2018
simple GPS reader of USB serial port
This implements a callback so other applications can hook into the data
Being a serial read, only one application can access the port at a time
If multi access is needed, implement gpsd

HOLUX puck uses ttyUSB0
Vk-172 (U-Block) uses ttyACM0

'''

import pynmea2
import serial
from datetime import datetime

class GPS(object):

    def __init__(self, callback):
        '''get callback and setup GPS'''
        self._callback = callback
        self.read()

    def read(self):
        '''For each new record, pass it to the callback'''
        lon = 00.00
        lat = 00.00

        serialStream = serial.Serial("/dev/ttyACM0", 4800, timeout=0.5)
        while True:
            sentence = serialStream.readline()
            if (sentence):
#        print sentence
                try:
                    data = pynmea2.parse(sentence)
                except Exception:
                    print Exception
                    continue
                if data.sentence_type == 'RMC':
                    ts = data.timestamp                    
                    lat = data.latitude
                    lon = data.longitude
                    date = str(data.datetime)
                    values = [date, lat, lon]
                    self._callback(values)
                    

def callback(rec):
    print rec

def test():
    gps = GPS(callback)
    
if __name__=="__main__":
    test()

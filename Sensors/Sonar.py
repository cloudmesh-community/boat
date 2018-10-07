'''
USB Sonar handler, dependent on gpsd service
gpsd setup is done in /home/pi/Scripts/Startup.sh:
sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock

NMEA 9182
Talker ID: YX - Transducer
Sentences: $SDDBT, DDPT - depth
Temperature: YXMTW - water temperature

$--DBT,x.x,f.x.x,M,x.x,F*hh
Depth, feet
f = feet
Depth, meters
M = Meters
Depth Fathoms
Checksum

'''

import serial


class Sonar(object):

    def __init__(self, callback, port='/dev/ttyUSB1'):
        '''get callback and setup GPS'''
        self._callback = callback
        self._port = None
        try:
            self._port = serial.Serial(port, baudrate=4800, timeout=1)
        except Exception:
            print Exception

    def watch(self):
        '''For each new record, parse it and pass it to the callback'''
        while True:
            self.getSentence()

    def getSentence(self):
        if self._port is None:
            values = {'name':None, 'data':None}
            self._callback(values)
            return
        if(self._port.inWaiting()>0):
            ''' Get sentence without blocking '''                
            new_data = self._port.readline().decode('ascii', errors='replace')            
            if new_data:
                values = []
                sentence = new_data.split(',')
                if sentence[0]=='$SDDBT':
                    values = self.parseDepth(sentence)
                    self._callback(values)
                elif sentence[0] == '$YXMTW':
                    values = self.parseTemp(sentence)
                    self._callback(values)                    

    def parseDepth(self, sentence):
        FEET = 1                                   
        return {'name':sentence[0][1:], 'data':{'depth':sentence[FEET]}}
        pass

    def parseTemp(self, sentence):
        TEMP = 1                                   
        return {'name':sentence[0][1:], 'data':{'temp':sentence[TEMP]}}

def testCallback(value):
    print value
                                   
def test():
    s = Sonar(testCallback)
    s.watch()                

if __name__=="__main__":
    test()                                   
                                   

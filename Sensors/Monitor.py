'''
# Author: Howard Webb
# Data: 8/28/2018
Logs sensor data to a file
This is driven by the GPS serial port getting new GPS sentences, then calling a callback
'''

from GPS import GPS
from oneWireTemp import getTempC
from Turbidity import Turbidity

class Monitor(object):

    def __init__(self):
        self._tur = Turbidity()
        self._file_name = self.getFileName()
        self._file = self.openFile()
        # call GPS loop with callback
        self._gps = GPS(self.logger)

    def logger(self, values):
        '''For every GPS message, get the other sensors and log data'''
        temp1 = getTempC(0)
        temp2 = getTempC(1)
        tb = self._tur.getRaw()
#        tb = 20000
        rec = "{}, {}, {}, {}, {}, {}\n".format(values[0], values[1], values[2], temp1, temp2, tb)
        self.save(rec)    

    def getFileName(self):
        '''Assumes format 'Log_000.txt'
            Will incriment the number for the next file
         '''   
        import glob
        filename = '/home/pi/Data/Log_000.txt'
        files =  glob.glob("/home/pi/Data/*.txt")
        if len(files) > 0:
            files.sort()
            last_file = files[-1]
            next_nbr = int(last_file.split('.')[0].split('_')[1])
            next_nbr += 1
            filename = "{}{}{}".format('/home/pi/Data/Log_', format(next_nbr, '0>3'), '.txt')
        print "Logging to:", filename
        return filename

    def openFile(self):
        '''Open a file for logging data'''
        return open(self._file_name, 'a')

    def save(self, rec):
        '''Append record to the file'''
        self._file.write(rec)
        self._file.flush()
        print(rec)
    
def test():
    mon = Monitor()

if __name__=="__main__":
    test()
    

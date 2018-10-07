'''
Author: Howard Webb
Date: 10/09/2018

Controller to collect GPS and Sonar data and integrate into a single record
May also collect non-serial data (ie. turbidity)
Store to a file, incrementing for each new run
'''
from GPS import GPS
from Sonar import Sonar
#from oneWireTemp import getTempC
#from Turbidity import Turbidity
import serial
# Routine to check serial ports for GPS or Sonar messages
# No guarantee which device is on which port
from PortStart import getPorts

class Monitor(object):

    def __init__(self, logger=None):
        ''' Build monitor with GPS and Sonar '''
        # Object level holders for data
        self._rmc = None
        self._dpt = None
        self._mtw = None
        # Option to use test logger or recording logger
        self._logger = self.logger
        if logger is not None:
            self._logger = logger
#        self._tur = Turbidity()
        # Get file for logging data
        self._file_name = self.getFileName()
        self._file = self.openFile()
        self._GPS = None
        self._Sonar = None
        # Get list of ports and check who is using
        #  avoids problems when switch USB location
        list = getPorts()
        if 'GPS' in list.keys():
            self._GPS = GPS(self._logger, list['GPS'])
        else:
            # Fail gracefully
            self._GPS = GPS(self._logger)
        if 'Sonar' in list.keys():            
            self._Sonar = Sonar(self._logger, list['Sonar'])
        else:
            # Fail gracefully
            self._Sonar = Sonar(self._logger)
        print "Serial Port Usage: ", list
        # Start data looping
        while (True):
            self._GPS.getSentence()
            self._Sonar.getSentence()

    def getFileName(self):
        ''' Create file name for next log
            Assumes format 'Log_000.txt'
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
    

    def logger(self, values):
        '''Callback to get messages, when have all three - save them as one record'''
#        print "Values", values
        if values['name'] is None:
            pass
        if values['name']=='GPRMC':   # Time and location
            self._rmc = values['data']
        elif values['name']=='SDDBT': # Depth
            self._dpt = values['data']
        elif values['name']=='YXMTW': # Temperature
            self._mtw = values['data']
        # Save record when have all parts            
        if (self._rmc is not None)  and (self._dpt is not None) and (self._mtw is not None):
            self.finishLogging()
            # clear data for next round of sentences
            self._rmc = None
            self._dpt = None
            self._mtw = None

    def finishLogging(self):
        ''' Save data to file '''
        # Get non serial data
#        temp1 = getTempC(0)
#        temp2 = getTempC(1)
#        tb = self._tur.getRaw()
        rec = "{}, {}, {}, {}, {}".format(self._rmc['time'], self._rmc['lat'], self._rmc['lon'], self._dpt['depth'], self._mtw["temp"])
#        print rec
        self.save(rec)    

def testLogger(values):
    ''' Dummy logger for testing '''
    print values

def test():
    ''' Quick test with dummy logger '''
    mon = Monitor(testLogger)

if __name__=="__main__":
#    test()
    mon = Monitor()
    

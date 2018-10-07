'''
Code modified from:
apps.fishandwhistle.net/archives/1155

Simple utility for checking serial port usage
Scan all ports and check if have GPS or Sonar message

'''

import serial
import sys
import glob

def readSerial(port):
    print "Read", port
    try:
        with serial.Serial(port, baudrate=4800, timeout=1) as ser:
            # read 10 lines from the serial output
            for i in range(10):
                line = ser.readline().decode('ascii', errors='replace')
                print "Line", line
                msg = line.split(',')
                print msg[0]
                if msg[0] == '$GPGGA':
    #                print msg
                    pass
                elif msg[0] == '$GPRMC':
                    print "Time: ", '20' + msg[9][4:6] + '/' + msg[9][2:4] + '/' + msg[9][0:2]
                else:
    #                print msg
                    pass
    except Exception as e:
        print e
            


def _scan_ports():
    if sys.platform.startswith('win'):
        print "scan Windows"
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        print "scan Linux"
        # this excludes your current terminal "/dev/tty"
        patterns = ('/dev/tty[A-Za-z]*', '/dev/ttyUSB*')
        ports = [glob.glob(pattern) for pattern in patterns]
        ports = [item for sublist in ports for item in sublist]  # flatten
    elif sys.platform.startswith('darwin'):
        print "scan Darwin"
        patterns = ('/dev/*serial*', '/dev/ttyUSB*', '/dev/ttyS*')
        ports = [glob.glob(pattern) for pattern in patterns]
        ports = [item for sublist in ports for item in sublist]  # flatten
    else:
        raise EnvironmentError('Unsupported platform')
    return ports
'''
def parseNMEA():
    import pynmea2
    nmea = '$GPRMC,164125,A,4425.8988,N,07543.5370,W,000.0,000.0,151116,,,A*67'
    nmeaobj = pynmea2.parse(nmea)
    ['%s: %s' % (nmeaobj.fields[i][0], nmeaobj.data[i]) 
         for i in range(len(nmeaobj.fields))]

import pynmea2, serial, os, time, sys, glob, datetime

def logfilename():
    now = datetime.datetime.now()
    return 'NMEA_%0.4d-%0.2d-%0.2d_%0.2d-%0.2d-%0.2d.nmea' % \
                (now.year, now.month, now.day,
                 now.hour, now.minute, now.second)



def test():
    try:
        while True:
            ports = _scan_ports()
            if len(ports) == 0:
                sys.stderr.write('No ports found, waiting 10 seconds...press Ctrl-C to quit...\n')
                time.sleep(10)
                continue

            for port in ports:
                # try to open serial port
                sys.stderr.write('Trying port %s\n' % port)
                try:
                    # try to read a line of data from the serial port and parse
                    with serial.Serial(port, 4800, timeout=1) as ser:
                        # 'warm up' with reading some input
                        for i in range(10):
                            ser.readline()
                        # try to parse (will throw an exception if input is not valid NMEA)
                        pynmea2.parse(ser.readline().decode('ascii', errors='replace'))

                        # log data
                        outfname = logfilename()
                        sys.stderr.write('Logging data on %s to %s\n' % (port, outfname))
                        with open(outfname, 'wb') as f:
                            # loop will exit with Ctrl-C, which raises a
                            # KeyboardInterrupt
                            while True:
                                line = ser.readline()
                                print(line.decode('ascii', errors='replace').strip())
                                f.write(line)

                except Exception as e:
                    sys.stderr.write('Error reading serial port %s: %s\n' % (type(e).__name__, e))
                except KeyboardInterrupt as e:
                    sys.stderr.write('Ctrl-C pressed, exiting log of %s to %s\n' % (port, outfname))

            sys.stderr.write('Scanned all ports, waiting 10 seconds...press Ctrl-C to quit...\n')
            time.sleep(10)
    except KeyboardInterrupt:
        sys.stderr.write('Ctrl-C pressed, exiting port scanner\n')    
'''

            
if __name__=="__main__":
    ports = _scan_ports()
    print ports
    port = ports[0]
    for port in ports:
        readSerial(port)
    

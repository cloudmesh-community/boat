'''
Code modified from:
apps.fishandwhistle.net/archives/1155

'''

import serial
import sys
import glob

list = {}

def identifyPort(port):        
    global list
    try:
        with serial.Serial(port, baudrate=4800, timeout=1) as ser:
            # read 10 lines from the serial output
            for i in range(10):
                line = ser.readline().decode('ascii', errors='replace')
                msg = line.split(',')
                if msg[0] == '$GPRMC':
                    list['GPS'] = port
                    return
                elif msg[0] == '$SDDBT':
                    list['Sonar'] = port
                    return
                    
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

def getPorts():
    ports = _scan_ports()
    print ports
    for port in ports:
        identifyPort(port)
    global list        
    return list

def test():            
    list = getPorts()
    print list
    
if __name__=="__main__":
    test()    

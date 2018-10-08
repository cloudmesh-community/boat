'''
 Code to read One-Wire temperature sensor(s) DS18B20
 
# Code modified from: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20
# This code requires modifying /boot/config.txt for modprobe
# This code requires using modprobe (see above website)
# This is set up for multiple probes being read (the x in the functions)

Author: Howard Webb
Date: 10/8/2018

'''

import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'


def read_temp_raw(sensor_id):
    ''' Read file assigned to this sensor
    Input:sensor_id
    Output: record from OneWire file for the device
    Throws: None

    '''    
    device_folder = glob.glob(base_dir + '28*')[sensor_id]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def getTempC(sensor_id):
    ''' Check the record and strip out the relevant data
    Input:sensor_id
    Output: temperature (Centegrade)
    Throws: None

    '''
    lines = read_temp_raw(sensor_id)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
#        temp_f = temp_c * 9.0 / 5.0 + 32.0
#        return temp_c, temp_f
        return temp_c
	
def test():

    ''' Quick test of the sensors
    Input: None
    Output: None
    Throws: None

    '''
    # Get count of sensors running
    sensors = len(glob.glob(base_dir + '28*'))
    for x in range (0, sensors):
        print "Device: ", x
        # Get several records to test
        for y in range(1, 4):
            tempC = getTempC(x)
            print ("Temp : %.2f C" %tempC)

if __name__=="__main__":
    test()




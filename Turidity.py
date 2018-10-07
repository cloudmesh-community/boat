"""
Test of the Turbidity meter using an ADC
# The Turbidity sensor mapped from 0 to 1023 (0 - 5 volts)
# ADC maps values -32768 to 32767, GND is 0 (-5 - 5 v)
# Voltage conversion is volts = (reading / 32767) * 5
# This may need some calibration adjustment


"""
# Import the ADS1x15 module.
from ADS1115 import ADS1115

class Turbidity(object):

   def __init__(self):
      self._adc = ADS1115()
      self._id = 0
      self._gain = 1

    def getRaw(self):
        return adc.read_adc(self._id, gain=GAIN)

def test():
    tur = Turbidity()
    value = tur.getRaw()
    print "Turbidity", value

if __name__ == "__main__":
    test()

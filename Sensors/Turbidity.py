"""
Test of the Turbidity meter using an ADC
# The Turbidity sensor mapped from 0 to 1023 (0 - 5 volts)
# ADC maps values -32768 to 32767, GND is 0 (-5 - 5 v)
# Voltage conversion is volts = (reading / 32767) * 5
# This may need some calibration adjustment


"""
from __future__ import print_function
# Import the ADS1x15 module.
from ADS1115 import ADS1115


class Turbidity(object):
    """
    Turbidity meter
    """

    def __init__(self):
        """
        initialize the turbidity meter
        """
        self._adc = ADS1115()
        self._id = 0
        self._gain = 1

    def get(self):
        """
        returns the raw values of the turbidity meter
        :return:
        """
        return self._adc.read_adc(self._id, gain=self._gain)


def test():
    turbidity = Turbidity()
    value = turbidity.get()
    print("Turbidity", value)


if __name__ == "__main__":
    test()

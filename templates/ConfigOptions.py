# -*- coding: utf-8 -*-
""" Handlers for holding and passing configuration data between parts of the application"""

from libs.Constants import *

""" Logging setup: """
import logging
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # CRITICAL , ERROR , WARNING , INFO , DEBUG , NOTSET
if not os.path.isdir('{}\\Debug'.format(os.getcwd())) and (logger.level is not logger.disabled):
    os.mkdir('{}\\Debug'.format(os.getcwd()))
FH = logging.FileHandler('{}\\Debug\\debug.log'.format(os.getcwd()))
FMT = logging.Formatter("%(asctime)s - %(name)s -- %(message)s")
FH.setFormatter(FMT)
logger.addHandler(FH)


class ConfigData:
    """Config Data to be shared between modules in the application"""
    def __init__(self):
        super(ConfigData, self).__init__()
        from os import getcwd
        from multiprocessing import Value
        from ctypes import c_bool
        from datetime import datetime as dt
        self.Extension = EXTENSION.TXT
        self.BitOrder = BITORDER.LSB
        self.BitDepth = BITDEPTHS.EIGHT
        self.PacketSize = 8
        self.WriteEnable = Value(c_bool, False)
        self.StreamEnable = Value(c_bool, False)
        self.write_block = Value(c_bool, False)
        self.MaxVoltage = 3.3
        self.MinVoltage = 0.0
        self.StreamType = STREAMTYPE.SERIAL
        self.SerialPort = None
        self.SerialBaud = 9600
        self.MaxDataPts = MAXCHUNKS
        self.SessionDialogInfo = dt.now().strftime("%d-%b-%Y--%H-%M-%f")
        self.SessionPath = getcwd()
        self.WriteNum = 0
        # [BitDepthIndex <int>, MSB / LSBIndex <int>, VoltageIndex <int>, PacketIndex <int>]
        self.BitLayout = [2, 0, 0, 2]
        self.NIPort = None
        self.NumSamples = int(1000000)
        self.TimeEnable = False
        self.combined_axis = False

    # TODO MAKE PROPER
    def get_plot_data(self):
        """returns a tuple of relevant data for plotting purposes"""
        # return self.MaxDataPts
        return CHUNKSIZE, self.MaxDataPts

    def get_stream_enable(self):
        return self.StreamEnable.value

    def get_write_enable(self):
        return self.WriteEnable.value

    def get_stream_data(self):
        """returns a tuple of relevant data for stream creation"""
        return self.StreamType, self.StreamEnable.value, self.BitDepth, self.BitOrder  # , self.PacketSize

    def get_serial_params(self):
        """return a tuple of revelant data for serial configuration"""
        return self.SerialPort, self.SerialBaud

    def get_file_data(self):
        """returns a tuple of relevant data for file writing purposes"""
        return self.Extension, self.SessionDialogInfo, self.SessionPath, self.WriteNum

    def get_file_enable(self):
        """returns a tuple of relevant data for file write enable/disable"""
        return self.WriteEnable.value

    def get_session_data(self):
        """returns a tuple of relevant data for plotting purposes"""
        return self.SessionDialogInfo, self.SessionPath

    def get_bit_data(self):
        """returns a tuple of relevant data for packet arranging and sizing purposes"""
        return self.BitDepth.value, self.BitOrder.value, self.PacketSize

    def get_voltage_data(self):
        """returns a tuple of relevant data for high level conversion purposes"""
        return self.MaxVoltage, self.MinVoltage, (self.MaxVoltage - self.MinVoltage / self.BitDepth.value)

    def set_combined(self, val: bool):
        """Setter for Write_Enable Value"""
        self.combined_axis = val

    def set_serial_port(self, port):
        """takes a string argument for the currently selected serial port"""
        self.SerialPort = port

    def set_session_data(self, _name, _path):
        """sets data for Session Naming purposes"""
        self.SessionDialogInfo, self.SessionPath = _name, _path

    def set_stream_type(self, _type):
        """takes a Constant defined value from Constants.STREAMTYPE for a value that determines operating mode"""
        self.StreamType = _type

    def set_serial_baud(self, baud):
        """takes a positive integer value for the intended serial baudrate"""
        self.SerialBaud = baud

    def set_ext(self, ext):
        """takes a defined streamtype value and sets extension to it."""
        self.Extension = ext

    def set_order(self, ord):
        """takes a defined BITORDER value and sets BitOrder to it."""
        self.BitOrder = ord

    def set_stream_enable(self, val: bool):
        """Setter for Write_Enable Value"""
        self.StreamEnable.value = val

    def set_write_enable(self, val: bool):
        self.WriteEnable.value = val

    def set_bit_data(self, data):
        """ uses a tuple to set plotting/analysis options """
        self.BitDepth = data[0][0]
        if data[0][1] == 'LSB':
            self.BitOrder = BITORDER.LSB
        else:
            self.BitDepth = BITORDER.MSB
        self.MinVoltage, self.MaxVoltage = data[0][2].split(' - ')
        self.MinVoltage, self.MaxVoltage = float(self.MinVoltage), float(self.MaxVoltage)
        self.PacketSize = data[0][3]
        self.BitLayout = data[1]
        logger.info('{} {} {} {}'.format(self.BitDepth, self.BitOrder, self.MinVoltage, self.MaxVoltage))


# Conditional check to start test
if __name__ == '__main__':
    import sys
    from pprint import pprint
    test = ConfigData()
    pprint(vars(test))
    print(test.get_stream_data())
    print(test.Extension)
    print(test.BitOrder)
    sys.exit(0)

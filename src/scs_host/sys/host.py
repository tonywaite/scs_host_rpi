"""
Created on 16 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://raspberrypi.stackexchange.com/questions/2086/how-do-i-get-the-serial-number
"""

import os
import re
import socket
import subprocess

from scs_core.sys.node import Node

from scs_host.sys.mcu_datum import MCUDatum


# --------------------------------------------------------------------------------------------------------------------

class Host(Node):
    """
    Broadcom BCM2837 64bit ARMv7 quad core processor
    """

    I2C_EEPROM =            3
    I2C_SENSORS =           1

    DFE_EEPROM_ADDR =       0x50
    DFE_UID_ADDR =          0x58


    # ----------------------------------------------------------------------------------------------------------------
    # devices...

    __OPC_SPI_BUS =         0                                   # based on spidev
    __OPC_SPI_DEVICE =      0                                   # based on spidev

    __NDIR_SPI_BUS =        0                                   # based on spidev
    __NDIR_SPI_DEVICE =     1                                   # based on spidev

    __NDIR_USB_DEVICE =     "/dev/ttyUSB0"                      # hard-coded path


    # ----------------------------------------------------------------------------------------------------------------
    # directories...

    __DEFAULT_HOME_DIR =    "/home/pi/"                         # hard-coded abs path
    __LOCK_DIR =            "/run/lock/southcoastscience/"      # hard-coded abs path
    __TMP_DIR =             "/tmp/southcoastscience/"           # hard-coded abs path

    __COMMAND_DIR =         "SCS/cmd/"                          # hard-coded rel path

    __CONF_DIR =            "SCS/conf/"                         # hard-coded rel path
    __AWS_DIR =             "SCS/aws/"                          # hard-coded rel path
    __OSIO_DIR =            "SCS/osio/"                         # hard-coded rel path

    __DFE_EEP_IMAGE =       "SCS/dfe_cape.eep"                  # hard-coded rel path


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def serial_number():
        cpuinfo = os.popen("cat /proc/cpuinfo").readlines()
        line = cpuinfo[-1]

        match = re.match('Serial\s*:\s*([0-9A-Fa-f]+)', line)

        if match is None:
            return None

        fields = match.groups()
        serial = fields[0]

        return serial


    @staticmethod
    def power_cycle():
        subprocess.call(['sudo', 'reboot'])


    @staticmethod
    def enable_eeprom_access():
        subprocess.call(['sudo', 'dtoverlay', 'i2c-gpio', 'i2c_gpio_sda=0', 'i2c_gpio_scl=1'])


    @staticmethod
    def mcu_temp():
        message = str(os.popen("vcgencmd measure_temp").readline())

        message = message.replace("temp=", "").replace("'C\n", "")

        temp = float(message)

        return MCUDatum(temp)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def gps_device(cls):
        raise NotImplementedError


    @classmethod
    def ndir_usb_device(cls):
        return cls.__NDIR_USB_DEVICE            # we might have to search for it instead


    @classmethod
    def psu_device(cls):
        raise NotImplementedError


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return socket.gethostname()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def ndir_spi_bus(cls):
        return cls.__NDIR_SPI_BUS


    @classmethod
    def ndir_spi_device(cls):
        return cls.__NDIR_SPI_DEVICE


    @classmethod
    def opc_spi_bus(cls):
        return cls.__OPC_SPI_BUS


    @classmethod
    def opc_spi_device(cls):
        return cls.__OPC_SPI_DEVICE


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def home_dir(cls):
        return os.environ['SCS_ROOT_PATH'] if 'SCS_ROOT_PATH' in os.environ else cls.__DEFAULT_HOME_DIR


    @classmethod
    def lock_dir(cls):
        return cls.__LOCK_DIR


    @classmethod
    def tmp_dir(cls):
        return cls.__TMP_DIR


    @classmethod
    def command_dir(cls):
        return cls.home_dir() + cls.__COMMAND_DIR


    @classmethod
    def conf_dir(cls):
        return cls.home_dir() + cls.__CONF_DIR


    @classmethod
    def aws_dir(cls):
        return cls.home_dir() + cls.__AWS_DIR


    @classmethod
    def osio_dir(cls):
        return cls.home_dir() + cls.__OSIO_DIR


    @classmethod
    def eep_image(cls):
        return cls.home_dir() + cls.__DFE_EEP_IMAGE

# SPDX-FileCopyrightText: 2023 Bernhard Bablok
# SPDX-FileCopyrightText: 2016 Philip R. Moyer for Adafruit Industries
# SPDX-FileCopyrightText: 2016 Radomir Dopieralski for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`pcf85063a` - PCF85063A Real Time Clock module
====================================================

This library supports the use of the PCF85063A-based RTC in CircuitPython.

Functions are included for reading and writing registers and manipulating
datetime objects.

Based on the driver for the PCF8523 RTC from:

Author(s): Philip R. Moyer and Radomir Dopieralski for Adafruit Industries.
Date: November 2016
Affiliation: Adafruit Industries

Implementation Notes
--------------------

**Hardware:**

* Pimoroni Badger 2040 W
* Pimoroni Inky Frame
* CM4 IO-base

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

**Notes:**

#. Milliseconds are not supported by this RTC.
#. Datasheet: https://www.nxp.com/docs/en/data-sheet/PCF85063A.pdf

"""

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_PCF85063A.git"

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register import i2c_bit
from adafruit_register import i2c_bits
from adafruit_register import i2c_bcd_alarm
from adafruit_register import i2c_bcd_datetime
from micropython import const

try:
    import typing  # pylint: disable=unused-import
    from busio import I2C
    from time import struct_time
except ImportError:
    pass


class PCF85063A:
    """Interface to the PCF85063A RTC.

    :param ~busio.I2C i2c_bus: The I2C bus the device is connected to

    **Quickstart: Importing and using the device**

        Here is an example of using the :class:`PCF85063A` class.
        First you will need to import the libraries to use the sensor

        .. code-block:: python

            import time
            import board
            import pcf85063a

        Once this is done you can define your `board.I2C` object and define your sensor object

        .. code-block:: python

            i2c = board.I2C()  # uses board.SCL and board.SDA
            rtc = pcf85063a.PCF85063A(i2c)

        Now you can give the current time to the device.

        .. code-block:: python

            t = time.struct_time((2017, 10, 29, 15, 14, 15, 0, -1, -1))
            rtc.datetime = t

        You can access the current time accessing the :attr:`datetime` attribute.

        .. code-block:: python

            current_time = rtc.datetime

    """

    lost_power = i2c_bit.RWBit(0x04, 7)
    """True if the device has lost power since the time was set."""

    datetime_register = i2c_bcd_datetime.BCDDateTimeRegister(0x04, False, 0)
    """Current date and time."""
    # The False means that day comes before weekday in the registers. The 0 is
    # that the first day of the week is value 0 and not 1.

    clockout_frequency = i2c_bits.RWBits(3, 0x01, 0)
    """Clock output frequencies generated. Default is 32.768kHz.
    Possible values are as shown (selection value - frequency).
    000 - 32.768khz
    001 - 16.384khz
    010 - 8.192kHz
    011 - 4.096kHz
    100 - 2.024kHz
    101 - 1.024kHz
    110 - 0.001kHz (1Hz)
    111 - Disabled
    """

    CLOCKOUT_FREQ_32KHZ = const(0b000)
    """Clock frequency of 32 KHz"""
    CLOCKOUT_FREQ_16KHZ = const(0b001)
    """Clock frequency of 16 KHz"""
    CLOCKOUT_FREQ_8KHZ = const(0b010)
    """Clock frequency of  8 KHz"""
    CLOCKOUT_FREQ_4KHZ = const(0b011)
    """Clock frequency of  4 KHz"""
    CLOCKOUT_FREQ_2KHZ = const(0b100)
    """Clock frequency of  2 KHz"""
    CLOCKOUT_FREQ_1KHZ = const(0b101)
    """Clock frequency of  1 KHz"""
    CLOCKOUT_FREQ_1HZ = const(0b110)
    """Clock frequency of 1 Hz"""
    CLOCKOUT_FREQ_DISABLED = const(0b111)
    """Clock output disabled"""

    alarm = i2c_bcd_alarm.BCDAlarmTimeRegister(
        0x0B, has_seconds=True, weekday_shared=False, weekday_start=0
    )
    """Alarm time for the first alarm."""
    # The False means that day and weekday don't share a register. The 0 is that the
    # first day of the week is value 0 and not 1.

    alarm_interrupt = i2c_bit.RWBit(0x01, 7)
    """True if the interrupt pin will output when alarm is alarming."""

    alarm_status = i2c_bit.RWBit(0x01, 6)
    """True if alarm is alarming. Set to False to reset."""

    timerA_enabled = i2c_bit.RWBit(0x11, 2)
    """True if timer is enabled"""

    timerA_frequency = i2c_bits.RWBits(2, 0x11, 3)
    """TimerA clock frequency. Default is 1/60Hz.
    Possible values are as shown (selection value - frequency).
    00 - 4.096kHz
    01 - 64Hz
    10 -  1Hz
    11 -  1/60Hz
    """

    TIMER_FREQ_4KHZ = const(0b00)
    """Timer frequency of 4 KHz"""
    TIMER_FREQ_64HZ = const(0b01)
    """Timer frequency of 64 Hz"""
    TIMER_FREQ_1HZ = const(0b10)
    """Timer frequency of 1 Hz"""
    TIMER_FREQ_1_60HZ = const(0b11)
    """Timer frequency of 1/60 Hz"""

    timerA_value = i2c_bits.RWBits(8, 0x10, 0)
    """ TimerA value (0-255). The default is undefined.
    The total countdown duration is calcuated by
    timerA_value/timerA_frequency. For a higher precision, use higher values
    and frequencies, e.g. for a one minute timer you could use
    value=1, frequency=1/60Hz or value=60, frequency=1Hz. The
    latter will give better results. See the PCF85x3 User's Manual
    for details."""

    timerA_interrupt = i2c_bit.RWBit(0x11, 1)
    """True if the interrupt pin will assert when timerA has elapsed.
    Defaults to False."""

    timerA_status = i2c_bit.RWBit(0x01, 3)
    """True if timerA has elapsed. Set to False to reset."""

    timerA_pulsed = i2c_bit.RWBit(0x11, 0)
    """True if timerA asserts INT as a pulse. The default
    value False asserts INT permanently."""

    high_capacitance = i2c_bit.RWBit(0x00, 0)
    """True for high oscillator capacitance (12.5pF), otherwise lower (7pF)"""

    calibration_schedule_per_minute = i2c_bit.RWBit(0x02, 7)
    """False to apply the calibration offset every 2 hours (1 LSB = 4.340ppm);
    True to offset every four minutes (1 LSB = 4.069ppm).  The default, False,
    consumes less power.  See datasheet figures 28-31 for details."""

    calibration = i2c_bits.RWBits(  # pylint: disable=unexpected-keyword-arg
        7, 0x02, 0, signed=True
    )
    """Calibration offset to apply, from -64 to +63.  See the PCF85063A datasheet
    table 13 for values and figure 11 for the offset calibration calculation workflow."""

    ram_byte = i2c_bits.RWBits(8,0x03,0)
    """free to use single byte of RAM. The value is zero on POR"""

    def __init__(self, i2c_bus: I2C):
        self.i2c_device = I2CDevice(i2c_bus, 0x51)

    @property
    def datetime(self) -> struct_time:
        """Gets the current date and time or sets the current date and time then starts the
        clock."""
        return self.datetime_register

    @datetime.setter
    def datetime(self, value: struct_time):
        self.lost_power = False
        self.datetime_register = value

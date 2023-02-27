
Introduction to the PCF85063A Real Time Clock (RTC) Library
===========================================================

This is a super-small real time clock (RTC) that allows your
microcontroller project to keep track of time even if it is reprogrammed,
or if the power is lost. Perfect for datalogging, clock-building, time
stamping, timers and alarms, etc.

The PCF85063A is simple and inexpensive but not a high precision device.
It may lose or gain up to two seconds a day. For a high-precision,
temperature compensated alternative, please check out the
`DS3231 precision RTC. <https://www.adafruit.com/products/3013>`_
If you need a DS1307 for compatibility reasons, check out our
`DS1307 RTC breakout <https://www.adafruit.com/products/3296>`_.

The PCF85063A is used in various Pimoroni boards, e.g. the Badger2040W or InkyFrame.
It is also used in the CM4IO-board.


Dependencies
============

This driver depends on the `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_
and `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
libraries. Please ensure they are also available on the CircuitPython filesystem.
This is easily achieved by downloading
`a library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.


Installing from PyPI
====================

*Note: currently, the package is not yet available from PyPI*.

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-pcf85063a/>`_. To install for current user:

.. code-block:: shell

    pip3 install circuitpython-pcf85063a

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-pcf85063a

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install circuitpython-pcf85063a


Usage Notes
===========

Basics
------

Of course, you must import the library to use it:

.. code:: python3

    import time
    import pcf85063a

All the RTC libraries take an instantiated and active I2C object
(from the `board` library) as an argument to their constructor. The way to
create an I2C object depends on the board you are using. For boards with labeled
SCL and SDA pins, you can:

.. code:: python3

    import board

Now, to initialize the I2C bus:

.. code:: python3

    i2c = board.I2C()

Once you have created the I2C interface object, you can use it to instantiate
the RTC object:

.. code:: python3

    rtc = pcf85063a.PCF85063A(i2c)

Date and time
-------------

To set the time, you need to set datetime` to a `time.struct_time` object:

.. code:: python3

    rtc.datetime = time.struct_time((2017,1,9,15,6,0,0,9,-1))

After the RTC is set, you retrieve the time by reading the `datetime`
attribute and access the standard attributes of a struct_time such as ``tm_year``,
``tm_hour`` and ``tm_min``.

.. code:: python3

    t = rtc.datetime
    print(t)
    print(t.tm_hour, t.tm_min)

Alarm
-----

To set the time, you need to set `alarm` to a tuple with a `time.struct_time`
object and string representing the frequency such as "hourly":

.. code:: python3

    rtc.alarm = (time.struct_time((2017,1,9,15,6,0,0,9,-1)), "daily")

After the RTC is set, you retrieve the alarm status by reading the
`alarm_status` attribute. Once True, set it back to False to reset.

.. code:: python3

    if rtc.alarm_status:
        print("wake up!")
        rtc.alarm_status = False


Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.


Contributing
============

Contributions are welcome! This project follows Adafruit's `Code of Conduct
<https://github.com/bablokb/circuitpython_pcf85063a/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

LEDCube
=======

Introduction
------------
A Simple LED Cube controller program. I built a 3x3 LED cube that uses 2 MCP23008 8-bit I2C GPIO
expanders. There are several posts on building an LED Cube but essentially it takes two many pins to
control each LED individually. Instead a multiplexing technique is used. To address a particular LED, 
the "column" is set to +5V and the entire "level" is sunk to ground.

This is provided mostly for education purposes. I don't really intended to build this class out more
or anything like that. It was really done for fun. I hope someone can find this useful.

This library requires the Adafruit's Raspberry-Pi Python Code Library located at
https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.

Classes
-------
The LedCube.py Python file contains three classes:
* LedCube: This class turns LEDs on a off by specifying the level and column of the LED.
* LedCubeLoader: This class parses JSON files and runs "programs" that are displayed on the 
LED cube.
* LedCubePov: Because each LED is not individually addressable, you can't turn on certain combinations
of multiple LEDs at the same time. For example if you tried to turn on LED at address level 0,
column 0 as well as level 1,column 1 the not only will those LEDs be enabled but also level 0,
column 1 and level 1,column 0 will also be turned on. The way to accomplish this is to cycle 
indiviually through the LEDs that need to be enabled very quickly. This is created a persistence 
of vision (PoV).

JSON Programs
-------------
The LedCubeLoader class loads "programs" from JSON files. While the LedCube class can be used
to interact with the cube programmatically, JSON files can be used as well.
* lightcheck.json: blinks each light in succession for 1/2 a second
* reset.json: turns all the lights off
* rowLooper.json: Cycles throw the bottom rows the jumps up to the top row cycles back.

Each of these files load a cube definition file. The example here is cube.json. It defines
the I2C address and SMB bus of the MCP23008/MCP23017 GPIO expander and the pins for each ground wire
for each level of the cube and the pins for each column.

License
-------
This source is release under GPL v3. The license can be viewed at http://www.gnu.org/licenses/gpl.html.

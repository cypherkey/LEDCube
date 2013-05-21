import sys
from time import sleep
from datetime import datetime,timedelta
import json
from Adafruit_MCP230xx import Adafruit_MCP230XX

class LEDCube:
    def __init__(self):
        self.level = []
        self.col = []

    def __setPin(self, ledType, index, val):
        if index >= len(ledType):
            raise ValueError("out of ranage")
        ledType[index][0].output(ledType[index][1], val)

    def addLevel(self, expander, pin):
        self.level.append([expander,pin])
        expander.config(pin, Adafruit_MCP230XX.OUTPUT)
        expander.output(pin, 0)

    def addCol(self, expander, pin):
        self.col.append([expander,pin])
        expander.config(pin, Adafruit_MCP230XX.OUTPUT)
        expander.output(pin, 0)

    def setLed(self, level, col, val):
        self.__setPin(self.level, level, val)
        self.__setPin(self.col, col, val)

    def reset(self):
        for i in range(0,len(self.level)):
            self.__setPin(self.level, level, 0)
        for i in range(0,len(self.col)):
            self.__setPin(self.col, col, 0)

    def levels(self):
        return len(self.level)

    def cols(self):
        return len(self.col)
 
class LedCubeLoader:
    @staticmethod
    def generateCube(filename):
        fp = open(filename,"r")
        cubeData = json.load(fp)
        fp.close()

        if not "expanders" in cubeData:
            raise Exception("missing expander definition")

        expanders = {}
        for expander in cubeData["expanders"]:
            expanders[expander["id"]] = \
                Adafruit_MCP230XX(busnum = expander["bus"], address = expander["address"], num_gpios = expander["gpio"])

        if not "cube" in cubeData:
            raise Exception("missing cube data")
        cube = LEDCube()
        if not "levels" in cubeData["cube"]:
            raise Exception("levels data missing for cube")

        for level in cubeData["cube"]["levels"]:
            cube.addLevel(expanders[level["expander"]],level["pin"])
        
        if not "columns" in cubeData["cube"]:
            raise Exception("column data missing for cube")

        for col in cubeData["cube"]["columns"]:
            cube.addCol(expanders[col["expander"]],col["pin"])

        return cube

    @staticmethod
    def runProgram(filename):
        fp = open(filename,"r")
        prog = json.load(fp)
        fp.close()

        if not "cube" in prog:
            raise Exception("cube not defined in program file")

        cube = LedCubeLoader.generateCube(prog["cube"])
        repeat=False
        if "repeat" in prog:
            repeat = prog["repeat"]

        if not "prog" in prog:
            raise Exception("program (prog) not defined in program file")

        pov = LedCubePov(cube)
        while(True):
            for line in prog["prog"]:
                pov.clear()
                if "level" in line and "column" in line:
                    pov.addLed(line["level"], line["column"])
                elif "leds" in line:
                    for led in line["leds"]:
                        pov.addLed(led["level"], led["column"])
                pov.run(line["duration"])
            if not repeat:
                break

class LedCubePov:
    def __init__(self, cube):
        self.cube = cube
        self.leds = []
        self.refresh = 0.005

    def addLed(self, level, col):
        self.leds.append([level,col])

    def run(self, duration):
        dt = datetime.now() + timedelta(milliseconds=duration)
        while dt > datetime.now():
            for leds in self.leds:
                self.cube.setLed(leds[0],leds[1], 1)
                sleep(self.refresh)
                self.cube.setLed(leds[0],leds[1], 0)

    def clear(self):
        self.leds = []

if __name__=="__main__":
    if len(sys.argv) == 2:
        LedCubeLoader.runProgram(sys.argv[1])

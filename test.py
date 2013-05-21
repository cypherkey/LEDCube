mcp0 = Adafruit_MCP230XX(busnum = 0, address = 0x20, num_gpios = 8)
mcp1 = Adafruit_MCP230XX(busnum = 0, address = 0x21, num_gpios = 8)
cube = LEDCube()
cube.addLevel(mcp0,1)
cube.addLevel(mcp1,5)
cube.addCol(mcp0,6)
cube.addCol(mcp0,2)
cube.addCol(mcp0,4)
cube.addCol(mcp0,0)
cube.addCol(mcp1,6)
cube.addCol(mcp1,7)
cube.addCol(mcp1,3)
cube.addCol(mcp1,0)
cube.addCol(mcp1,1)

def lightCheck():
    for level in range(0,cube.levels()):
        for col in range(0,cube.cols()):
            cube.setLed(level,col,1)
            sleep(0.5)
            cube.setLed(level,col,0)

def povTest():
    pov = LedCubePov(cube)
    pov.addLed(0,0)
    pov.addLed(1,1)
    pov.run(1000)
    cube.reset
    
def prog1():
    while(True):
        for level in [0,1]:
            if level:
                direction = [2,1,0]
            else:
                direction = [0,1,2]
    
            for col in direction:
                cube.setLed(level,col,1)
                cube.setLed(level,col+3,1)
                cube.setLed(level,col+6,1)
                sleep(.25)
                cube.setLed(level,col,0)
                cube.setLed(level,col+3,0)
                cube.setLed(level,col+6,0)

# lightCheck()
# prog1()
# povTest()

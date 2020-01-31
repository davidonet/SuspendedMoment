import board
import time
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)

class Stepper:
    def __init__(self,dir_pin,en_pin,step_pin):
        self._sleep = mcp.get_pin(0)
        self._sleep.switch_to_output(value=True)
        self._rst = mcp.get_pin(1)
        self._rst.switch_to_output(value=True)
        self.ms1 = mcp.get_pin(2)
        self.ms1.switch_to_output(value=False)
        self.ms2 = mcp.get_pin(3)
        self.ms2.switch_to_output(value=False)
        self.ms3 = mcp.get_pin(4)
        self.ms3.switch_to_output(value=False)
        self.dir = mcp.get_pin(dir_pin)
        self.dir.switch_to_output(value=False)
        self._en = digitalio.DigitalInOut(en_pin)
        self._en.direction = digitalio.Direction.OUTPUT
        self.step = digitalio.DigitalInOut(step_pin)
        self.step.direction = digitalio.Direction.OUTPUT

    def step_loop(self,steps,sec):
        self._en.value = False
        for i in range(steps):
            self.step.value = True
            time.sleep((2*sec)/steps)
            self.step.value = False
            time.sleep((2*sec)/steps)
        self._en.value = True

    def push(self,steps,sec):
        self.dir.value = False
        self.step_loop(steps,sec)

    def pull(self,steps,sec):
        self.dir.value = True
        self.step_loop(steps,sec)


# stepper0 = stepper.Stepper(5,board.D19,board.D13)
# stepper1 = stepper.Stepper(6,board.D26,board.D12)

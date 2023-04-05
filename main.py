#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
claw = Motor(Port.A)
vertical_axis = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
horizontal_axis = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

vertical_axis.control.limits(speed=60, acceleration=120)
horizontal_axis.control.limits(speed=60, acceleration=120)

# Write your program here.
def pick_up():
    """Function that makes the claw grip and move upward (picking up)"""
    for i in range(1, 10):
        claw.run(10)
        


    for i in range(1, 10):
        vertical_axis.run(10)
        vertical_axis.reset_angle(0)


def main():
    pick_up()


if __name__ == "__main__":
    main()

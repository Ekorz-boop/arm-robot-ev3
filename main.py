#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
claw = Motor(Port.A)
vertical_axis = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
horizontal_axis = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])
left_button = Button.LEFT_DOWN


vertical_axis.control.limits(speed=60, acceleration=120)
horizontal_axis.control.limits(speed=60, acceleration=120)

claw.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
claw.reset_angle(0)
claw.run_target(200, -90)
vertical_axis.run_until_stalled(-20, then=Stop.COAST, duty_limit=50)
vertical_axis.reset_angle(0)

color_sensor = ColorSensor(Port.S2)

zone_dict = {}

# Write your program here.
def pick_up():
    """Function that makes the claw grip and move upward (picking up)"""
    claw.run_until_stalled(-100, then=Stop.HOLD, duty_limit=50)
    vertical_axis.run_target(20, 120, then=Stop.HOLD)


def drop():
    """Function that gently puts the item down and drops it"""
    vertical_axis.run_target(20, 70, then=Stop.HOLD)
    claw.run_target(20, -90)
    vertical_axis.run_target(40, 80, then=Stop.HOLD)


def check_location():
    """Cheks if an item is at precent at a given locations and returns true"""
    claw.run_until_stalled(20, then=Stop.HOLD, duty_limit=50)
    if (claw.angle() > -10):
        print("No Item")
        return False
    else:
        print("Item")
        return True

def free_control():
    """Function for controlling the arm free form"""
    pressed = ev3.buttons.pressed()
    if Button.LEFT in pressed:
        horizontal_axis.run(-45)
    elif Button.RIGHT in pressed:
        horizontal_axis.run(45)
    else:
        horizontal_axis.run(0)
        
def create_zone():
    """Function for creating zones at a designated position and saving it in the zone dictionary"""
    pressed = ev3.buttons.pressed()
    current_zone_num = 0
    if Button.BEACON in pressed:
        current_angle = horizontal_axis.angle()
        current_zone_num += 1
        zone_dict[f"zone {current_zone_num}"] = current_angle
        if current_zone_num >= 4:
            current_zone_num = 0

        
def color_check():
    """function tells the color"""
    vertical_axis.run_target(40, 95, then=Stop.HOLD)
    print(color_sensor.color())

def main():
    item = False
    item = check_location()
    if check_location():
        pick_up()
        drop()
    while True:
        free_control()


if __name__ == "__main__":
    main()

#hrj
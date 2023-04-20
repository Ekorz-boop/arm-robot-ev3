#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor
import os


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
current_zone_num = 0

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

def free_control(pressed):
    """Function for controlling the arm free form"""
    if Button.LEFT in pressed:
        horizontal_axis.run(-45)
    elif Button.RIGHT in pressed:
        horizontal_axis.run(45)
    elif Button.UP in pressed:
        vertical_axis.run(45)
    elif Button.DOWN in pressed:
        vertical_axis.run(-45)
    else:
        horizontal_axis.stop()
        vertical_axis.stop()
        
        

def create_zone():
    """Function for creating zones at a designated position and saving it in the zone dictionary"""
    global current_zone_num
    current_h_angle = horizontal_axis.angle()
    current_v_angle = vertical_axis.angle()
    current_zone_num += 1
    angle_tuple = (current_h_angle, current_v_angle)
    zone_dict[str(current_zone_num)] = angle_tuple
    if current_zone_num >= 4:
        current_zone_num = 0
    wait(200)
        
            
def go_to_zone(zone):
    """Function that turns the arm to the desigated zone"""
    horizontal_axis.run_target(zone_dict.get(zone[0]), 70, then=Stop.COAST)
    vertical_axis.run_target(zone_dict.get(zone[1]), 70, then=Stop.COAST)
        

def color_check():
    """function tells the color"""
    vertical_axis.run_target(40, 95, then=Stop.HOLD)
    color = color_sensor.color()
    print(color)
    return color


def drop_of_color_calibrate():
    global drop_of_color_1
    global drop_of_color_2
    global drop_of_color_3
    if drop_of_color_1 == None:
        drop_of_color_1 = color_check()
        wait(200)
    elif (drop_of_color_1 != None and drop_of_color_2 == None and drop_of_color_3 == None):
        drop_of_color_2 = color_check()
        wait(200)
    elif(drop_of_color_1 != None and drop_of_color_2 != None and drop_of_color_3 == None):
        drop_of_color_3 = color_check()
        wait(200)
    else:
        print("All colors calibratet")


def movement_menu():
    menu_movement = """
    L. Left
    U. Up
    R. Right
    D. Down
    """
    run = True
    while run:
        print(menu_movement)
        pressed = ev3.buttons.pressed()
        free_control(pressed)
        
        if Button.CENTER in pressed:
            run = False
            
def zone_menu():
    menu_zone = """
    L. 
    U. Create Zone
    R. 
    D. Go to zone
    """
    menu_zone_choice = """
    L. Zone 1
    U. Zone 2
    R. Zone 3
    D. Zone 4
    """
    zone = "1"
    run = True
    while run:
        pressed = ev3.buttons.pressed()
        print(menu_zone)
        if Button.UP in pressed:
            create_zone()
        elif Button.DOWN in pressed:
            print(menu_zone_choice)
            if Button.LEFT in pressed:
                zone = "1"
                go_to_zone(zone)
                
            elif Button.UP in pressed:
                zone = "2"
                go_to_zone(zone)
                
            elif Button.RIGHT in pressed:
                zone = "3"
                go_to_zone(zone)
                
            elif Button.DOWN in pressed:
                zone = "4"
                go_to_zone(zone)
        
        if Button.CENTER in pressed:
            run = False
        

def color_menu():
    menu_color = """
    L. Left
    U. Up
    R. Right
    D. Down
    """
    run = True
    while run:
        print(menu_color)
        pressed = ev3.buttons.pressed()
        if Button.CENTER in pressed:
            run = False


def interface():
    menu_1 = """
    L. Zone Menu
    U. Color Menu
    R. Movement
    D. Bad functions
    """
    run = True
    while run:
        print(menu_1)
        pressed = ev3.buttons.pressed()
        
        if Button.LEFT in pressed:
            zone_menu()
            
        elif Button.RIGHT in pressed:
            movement_menu()
            
        elif Button.UP in pressed:
            color_menu()
            
        elif Button.DOWN in pressed:
            pass
        
        
        
        
                
def main():
    """Main function"""
    # item = False
    # item = check_location()
    # if check_location():
    #     pick_up()
    #     drop()
    #interface()
    pass


if __name__ == "__main__":
    interface()

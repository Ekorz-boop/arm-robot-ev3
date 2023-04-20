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
        drop_of_color_calibrate()
    else:
        horizontal_axis.stop()
        

def create_zone(pressed):
    """Function for creating zones at a designated position and saving it in the zone dictionary"""
    global current_zone_num
    if Button.UP in pressed:
        current_h_angle = horizontal_axis.angle()
        current_v_angle = vertical_axis.angle()
        current_zone_num += 1
        angle_tuple = (current_h_angle, current_v_angle)
        zone_dict[current_zone_num] = angle_tuple
        if current_zone_num >= 4:
            current_zone_num = 0
        wait(200)
        
            
def go_to_zone(zone):
    """Function that turns the arnm to the desigated zone"""
    horizontal_axis.run_target(zone_dict.get(zone[0]), 70, then=Stop.COAST)
    vertical_axis.run_target(zone_dict.get(zone[1]), 70, then=Stop.COAST)
        

def color_check():
    """function tells the color"""
    vertical_axis.run_target(40, 95, then=Stop.HOLD)
    color = color_sensor.color()
    return color


def drop_of_color_calibrate():
    global drop_of_color_1
    global drop_of_color_2
    global drop_of_color_3
    if drop_of_color_1 == None:
        drop_of_color_1 = color_check()
        print("color1",drop_of_color_1)
        wait(200)
    elif (drop_of_color_1 != None and drop_of_color_2 == None and drop_of_color_3 == None):
        drop_of_color_2 = color_check()
        print("color2",drop_of_color_2)
        wait(200)
    elif(drop_of_color_1 != None and drop_of_color_2 != None and drop_of_color_3 == None):
        drop_of_color_3 = color_check()
        print("color3",drop_of_color_3)
        wait(200)
    else:
        print("All colors calibratet")

def interface():
    menu_layer_1 = """
    L. Zone Menu
    U. Color Menu
    R. 
    D.
    """
    menu_zone = """
    L. Move Left
    U. Create Zone
    R. Move Right
    D. Go to Zone
    """
    menu_color = """
    L.
    U.
    R.
    D.
    """
    menu_zones = """
    Choose which zone to go to
    L. Zone 1
    U. Zone 2
    R. Zone 3
    D. Zone 4
    """
    current_menu = menu_layer_1
    run = True
    while run:
        pressed = ev3.buttons.pressed()
        #print(current_menu)
        if current_menu == menu_layer_1:
            if Button.LEFT in pressed:
                current_menu = menu_zone
                
            elif Button.UP in pressed:
                current_menu = menu_color
                
        
        elif current_menu == menu_zone:
            zone = 1
            if Button.LEFT in pressed:
                print(pressed)
                free_control(pressed)
                
                
            elif Button.UP in pressed:
                create_zone(pressed)
                
                
            elif Button.RIGHT in pressed:
                print(pressed)
                free_control(pressed)
                
                
            elif Button.DOWN in pressed:
                print(menu_zones)
                
                if Button.LEFT in pressed:
                    zone = 1
                    go_to_zone(zone)
                    
                
                elif Button.UP in pressed:
                    zone = 2
                    go_to_zone(zone)
                    
                    
                elif Button.RIGHT in pressed:
                    zone = 3
                    go_to_zone(zone)
                    
                    
                elif Button.DOWN in pressed:
                    zone = 4
                    go_to_zone(zone)
                    
            
            
        elif current_menu == menu_color:
            if Button.LEFT in pressed:
                pass
            elif Button.UP in pressed:
                pass
            elif Button.RIGHT in pressed:
                pass
            elif Button.DOWN in pressed:
                pass
            
        elif Button.CENTER in pressed:
            current_menu = menu_layer_1
            wait(150)
        
                
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

#hrj
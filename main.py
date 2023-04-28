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
import math

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
claw = Motor(Port.A)
vertical_axis = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
horizontal_axis = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])
left_button = Button.LEFT_DOWN


vertical_axis.control.limits(speed=60, acceleration=60)
horizontal_axis.control.limits(speed=60, acceleration=60)

claw.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
claw.reset_angle(0)
claw.run_target(200, -90)
vertical_axis.run_until_stalled(-20, then=Stop.COAST, duty_limit=50)
vertical_axis.reset_angle(0)

color_sensor = ColorSensor(Port.S2)

zone_dict = {} #Handles which zone have which angle coordinates
color_dict = {} #Handles which color have which zone
start = None
current_zone_num = 0

drop_of_color_1 = None
drop_of_color_2 = None
drop_of_color_3 = None
c_blue = Color.rgb(Color.BLUE)
c_red = Color.rgb(Color.RED)
c_yellow = Color.rgb(Color.YELLOW)
c_green = Color.rgb(Color.GREEN)
all_colors = [c_blue, c_red, c_yellow, c_green]

# Write your program here.
def pick_up():
    """Function that makes the claw grip and move upward (picking up)"""
    claw.run_until_stalled(-100, then=Stop.HOLD, duty_limit=50)
    vertical_axis.run_target(20, 120, then=Stop.HOLD)


def drop():
    """Function that gently puts the item down and drops it"""
    vertical_axis.run_until_stalled(-100, then=Stop.HOLD, duty_limit=50)
    claw.run_target(20, -90)
    vertical_axis.run_target(40, 80, then=Stop.HOLD)


def check_location():
    """Checks if an item is at precent at a given locations and returns true"""
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
    
    
def assign_color(color, zone):
    """Assigns a zone to a color and saves it in a dictionary"""
    color_dict[str(color)] = zone
    wait(200)


def get_h_angle(zone):
    """Gives the horizontal angle of target zone in the zone dictionary"""
    for key in zone_dict:
        if key == zone:
            cord_tuple = zone_dict[zone]
            return cord_tuple[0]


def get_v_angle(zone):
    """Gives the vertical angle of target zone in the zone dictionary"""
    for key in zone_dict:
        if key == zone:
            cord_tuple = zone_dict[zone]
            return cord_tuple[1]

     
def go_to_zone(zone):
    """Function that turns the arm to the desigated zone"""
    print(zone_dict)
    vertical_axis.run_target(-120, 70, then=Stop.HOLD) 
    speed = 70
    if get_h_angle(zone) <= 0:
        speed = speed * -1
    elif get_h_angle(zone) > 0 and speed == -70:
        speed = speed * -1
    horizontal_axis.run_target(get_h_angle(zone), speed, then=Stop.COAST)
    vertical_axis.run_target(get_v_angle(zone), 70, then=Stop.HOLD) 

def set_pickup_zone(zone):
    """Sets the pickup zone to the start position"""
    global start
    start = zone

def pickup_from_start():
    """Pick up block from the starting position"""
    global start
    zone = start
    go_to_zone(zone)
    check_location()
    pick_up()


def color_check():
    """Function that tells the color"""
    vertical_axis.run_target(40, 95, then=Stop.HOLD)
    color = determine_color(color_sensor.rgb())
    print(color)
    return color


def euclidean_distance(test_color, color):
    """Return the distance from chosen color and predetermined color"""
    r1, g1, b1 = test_color
    r2, g2, b2 = color
    distance = math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
    return distance


def determine_color(test_color):
    """Returns the color closest matching the input color"""
    closest_match = (0, 0, 0)
    for color in all_colors:
        if euclidean_distance(test_color, color) < euclidean_distance(closest_match, color):
            closest_match = color
    
    return closest_match


def drop_of_color_calibrate():
    """Checks and saves colors (up to 3 colors)"""
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
    """Handles the movement menu"""
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
    """Handles the zone menu"""
    menu_zone = """
    L. 
    U. Create Zone
    R. 
    D. Go to zone
    """
    run = True
    while run:
        pressed = ev3.buttons.pressed()
        print(menu_zone)
        if Button.UP in pressed:
            create_zone()
            wait(500)
        elif Button.DOWN in pressed:
            wait(500)
            go_to_zone_menu()
            
        
        if Button.CENTER in pressed:
            run = False
        

def go_to_zone_menu():
    """Handles the go to zone choice menu"""
    menu_zone_choice = """
    L. Zone 1
    U. Zone 2
    R. Zone 3
    D. Zone 4
    """
    
    run = True
    while run:
        pressed = ev3.buttons.pressed()
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
    """Handles the color menu"""
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
            

def color_zone_menu():
    """Handles the color zones menu"""
    menu_color_zone = """
    L. 
    U. Assign color to zone
    R. 
    D. 
    """
    run = True
    while run:
        print(menu_color_zone)
        pressed = ev3.buttons.pressed()
        if Button.UP in pressed:
            color_match_menu()
        
        if Button.CENTER in pressed:
            run = False
            

def color_match_menu():
    """Handles the color match menu"""
    menu_color_match = """
    Choose which color you want to assign to a zone
    L. Color 1 {drop_of_color_1}
    U. Color 2 {drop_of_color_2}
    R. Color 3 {drop_of_color_3}
    D.
    """.format(drop_of_color_1=drop_of_color_1, drop_of_color_2=drop_of_color_2, drop_of_color_3=drop_of_color_3)
    chosen_color = drop_of_color_1
    run = True
    while run:
        print(menu_color_match)
        pressed = ev3.buttons.pressed()
        
        if Button.LEFT in pressed:
            color_match_menu_2(chosen_color)
            
        elif Button.UP in pressed:
            chosen_color = drop_of_color_2
            color_match_menu_2(chosen_color)
            
        elif Button.RIGHT in pressed:
            chosen_color = drop_of_color_3
            color_match_menu_2(chosen_color)
            
        elif Button.DOWN in pressed:
            chosen_color = drop_of_color_1
            color_match_menu_2(chosen_color)
        
        if Button.CENTER in pressed:
            run = False


def color_match_menu_2(chosen_color):
    """Handles the second phase of the color match menu"""
    menu_color_match_2 = """
    Choose which zone to assign chosen color to
    L. Zone 1
    U. Zone 2
    R. Zone 3
    D. Zone 4
    """
    run = True
    while run:
        print(menu_color_match_2)
        pressed = ev3.buttons.pressed()
        
        if Button.LEFT in pressed:
            assign_color(chosen_color, "1")
            
        elif Button.UP in pressed:
            assign_color(chosen_color, "2")
            
        elif Button.RIGHT in pressed:
            assign_color(chosen_color, "3")
            
        elif Button.DOWN in pressed:
            assign_color(chosen_color, "4")
        
        if Button.CENTER in pressed:
            run = False


def interface():
    """Handles the interface"""
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
            color_zone_menu()
            
        
def main():
    """Main function"""
    # item = False
    # item = check_location()
    # if check_location():
    #     pick_up()
    #     drop()
    #interface()
    interface()


if __name__ == "__main__":
    main()

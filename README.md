## Introduction
This project is a University project where a lego mindstorms robot (ev3) is supposed to be programmed with different user stories in mind. 
The main objective/feature of the project is to enable the robot arm to sort lego bricks according to different criterias. 


## Getting started
* Clone the project folder to your computer using git bash ("git clone https://github.com/Ekorz-boop/arm-robot-ev3") in a destination of your choice

* Make sure you have ev3dev-browser, Lego Mindstorms EV3 Microython, Python and Flake8 (optional but recommended) installed. You can install these in the extensions
tab in visual studio code. 

* Open the folder in visual studio code and sync your instance to the repository using ("git pull") in the folder via git bash or via the source control tab in visual studio code.

* Now you have the latest version and can make changes, commit and push via the visual studio code source control tab for convenience.


## Building and running

To run the program you first need a ev3 mindstorms robot and all dependencies installed. Then follow these steps:

* Connect to the robot via the explorer tab in visual studio code, and then under the ev3dev device browser drop down menu (click connect to device and choose the robot you want to connect to)

* Transfer the code you want to run to the robot via the ev3dev device browser menu

* Right click on the file (server_main.py file if you want to run that robot as a server, or the client_main.py if you want the robot to run as a client) and then press "run".

* The code will now run, and you can use the buttons on the hub of the robot to control the menu system. You will need to stay connected to the robot via usb to read the output in visual studio code, which will grant you a view of the menu system and which buttons does what. 

* Create all zones, remember that zone 1 is the pickup zone and should not be overwritten with a new zone. Zone 1 is also the position in which the arm is in when the robot starts, so keep that in mind.

* Assign colors to all the zones (remember to not assign anything to zone 1)

* Run sorting mode in the menu


## Features
- [x] US_1:  As a customer, I want the robot to pick up items
- [x] US_1B: As a customer, I want the robot to pick up items from a designated position
- [x] US_2: As a customer, I want the robot to drop off items
- [x] US_2B: As a customer, I want the robot to drop items off at a designated position.
- [x] US_3: As a customer, I want the robot to be able to determine if an item is present at a given location.
- [x] US_4: As a customer, I want the robot to tell me the color of an item.
- [x] US_5: As a customer, I want the robot to drop items off at different locations based on the color of the item.
- [x] US_6: As a customer, I want the robot to be able to pick up items from elevated positions
- [x] US_8: As a customer, I want to be able to calibrate maximum of three different colors and assign them to specific drop-off zones.
- [x] US_8B: As a customer, I want to be able to calibrate items with three different colors and drop the items off at specific drop-off zones based on color
- [x] US_9: As a customer, I want the robot to check the pickup location periodically to see if a new item has arrived.
- [x] US_10: As a customer, I want the robots to sort items at a specific time. 
- [ ] US_11: As a customer, I want two robots to communicate and work together on items sorting without colliding with each other.
- [x] US_12: As a customer, I want to be able to manually set the locations and heights of one pick-up zone and two drop-off zones. (Implemented either by manually dragging the arm to a position or using buttons).



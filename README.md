AutoDoor
========
This is the repository for an automatically unlocking door. This allows a door to automatically unlock once a one of the permissioned users get near the door. 

**Raspberry Pi**
  1. Continually checks every device loccated in the authorized client list if the device is connected to the local network or not.
  2. If a device connects to the network and is not already in the connected list the door will unlock automatically.
  3. The door will automatically locks once the door is shut after unlocking. If the door had not been opened with in 20 seconds of the unlock it will automattically lock again.
  4. Allows direct override of locking and unlocking of the door using commands from the Android app.
  5. Determines if the door is locked or unlocked, and if the door is open or closed.
  6. Manages all socket connections made by the Android app and verifying users credidentials.
  7. Will email the list of admins when a user has logged in or failed to log in via the Android app.
  8. Monitors information recived from the Arduino
**Android App**
  1. Requires an authorized username and pin.
  2. Will remember username but after exiting the app the pin must be entered again.
  3. Display the current state of the door (Locked, Unlocked, Open, Closed)
  4. Allow locking and unlocking from anywhere.
**Arduino**
  1. Initiate servo moter to lock/unlock the door.
  2. When requested by the PI send a signal to the PI telling if the door is unlocked/locked
  3. Manage the information from the proximity sensor to automatically unlock the door when leaving from the inside.

**Parts**
  1. Raspberry Pi
     1. Wireless dongle - Optional
     2. Power cable
  2. Arduino
     1. Usb cable - For power and serial comunication
     2. Brototyping wires - To connect to the auxilarary components
  3. Servo motor
  4. Proximity sensor
  5. Magnetic door sensor

**Installation Proccess**
=========================
*0. Pre-install*
This tutorial is based on a Raspberry-PI running Raspbian.
If need to install Raspbian you can get it here http://www.raspbian.org/FrontPage

All devices must have static ip addressing for the door to automaticaly unlock when they connect to the internet.
Google your router for specific instructions on setting static IPs. Usally this setting is under Nat or DHCP settings.

*1. Installing*
sudo apt-get update; sudo apt-get upgrade; sudo apt-get install git pyhton-mysqldb mysql-server tmux

git clone https://github.com/quinnsam/Autodoor.git

sudo ./installer

*Arduino Setup*
Frist you will need to get the ide for the Arduino
    http://arduino.cc/en/Main/Software

Next you wil need to install the Autodoor sketch to the Arduino you will find the sketch in the 
Serial_Prox folder named "Serial_Prox.ino"

    D13 --> +Vcc LED                    Connected to digital pin 13
    D9  --> +Vcc Servo                  Digital pin to control the servo
    A0  --> Servo Potentiometer 		Analog pin used to connect the potentiometer
    D2  --> Door Switch                 Digital pin for door switch

Proximity Sensor

    Red   --> +5V
    White --> I2C SDA (pin-A4)
    Black --> GND
    Grey  --> ISC SCL (pin-A5)

Set Dip switches on the proximity
    1 --> OFF
    2 --> OFF



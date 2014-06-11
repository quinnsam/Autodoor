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
**Coming Soon**

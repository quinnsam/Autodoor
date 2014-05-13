AutoDoor
========
This is the repository for an automatically unlocking door. This allows a door to automatically unlock once a one of the permissioned users get near the door. 

**Raspberry Pi**
  1. Detects how many users are currently in the house.
  2. Auto locks the door when no one is in the house.
  3. Automatically locks the door (if not already) after 20:00
  4. Allows direct override of locking and unlocking of the door using a command.
  5. Determines if the door is locked or unlocked.
  6. Allow permissioned users to be added remotely.
  7. Relocks the door after 10 minutes of unlocked | OR | When specified users are home alone.
  8. Lock Down mode, where it returns to matic functionality.
  9. [POSSIBLE ADDITION] Takes a picture of whoever enters the door matically or automatically. Using one of these http://www.google.com/url?q=http%3A%2F%2Fwww.securitysurveillanceplus.com%2FDoor-Eye-Hole%2F&sa=D&sntz=1&usg=AFQjCNEqIjUrdfbWMzXDiYqKlvx-fe9TNA

**Arduino**
  1. Initiate servo moter to lock/unlock the door.
  2. Send a signal to the PI telling if the door is unlocked/locked

**Parts**
  1. Raspberry Pi
    a. Wireless dongle
    b. Power cable
  2. Servo Motor
    a. Control and Position wires
    b. Motor control IC
  3. Arduino
    a. Raspberry Pi connect

**Chris’s Thoughts**: I would imagine the way to do communication should be through serial, have the pi run a python script or something that reads and write serial data and arduino can do the same in c. Every # seconds you could send the data back and forth in a string via serial that could easily be parsed in python. Or you could have it only send on input from the PI as well. depending on the state of the arduino is when motors would move. But any information would be
conveyed back to the pi and then could be displayed perhaps on a website through the pi. In conjunction with a database you could then also have an app for manual control and remote additions to people allowed in.  By requiring a username and password for that kind of connection people could be allowed in without being given access to the entire system as well.


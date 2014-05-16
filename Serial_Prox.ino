/******************************************************************************
* This program automates a door for keyless unlocking                         *
* Developed by: Sam Quinn, Chauncey Yan, Ashley Greenacre, and Chris Harper.  *
* 05/13/2014                                                                  *
******************************************************************************/

#include <Wire.h>
#include <Servo.h>


// Possible sensor addresses (suffix correspond to DIP switch positions)
#define SENSOR_ADDR_OFF_OFF  (0x26)
#define SENSOR_ADDR_OFF_ON   (0x22)
#define SENSOR_ADDR_ON_OFF   (0x24)
#define SENSOR_ADDR_ON_ON    (0x20)

#define LOCK        40
#define UNLOCK      120

//Prototypes
int lock(int);

// Set the sensor address here
const uint8_t sensorAddr = SENSOR_ADDR_OFF_OFF;
int led_pin = 13;       // LED connected to digital pin 13
int servo_pin = 9;      //Digital pin to control the servo
int const pot_pin = A0; // analog pin used to connect the potentiometer
int pot_val = -1;            // variable to read the value from the analog pin 
int input;

// Servo Object
Servo door;

// One-time setup
void setup()
{
    // Start the serial port for output
    Serial.begin(9600);

    // Pin to connet to the pi
    pinMode(led_pin, OUTPUT);      // sets the digital pin as output

    // Join the I2C bus as master
    Wire.begin();

    //Adrress for the proximity sensor 
    WriteByte(sensorAddr, 0x3, 0xFE);
}

// Main program loop
void loop() {
    //Beginig Serial monitoring
    if (Serial.available() > 0) {
        input = Serial.read();
        if (input == 49 || input == 48){
            if( input == 49) {
                if (lock(1) != 1) {
                    Serial.println("ERROR: Could not execute command LOCK");
                }
            } else {
                if (lock(0) != 0) {
                    Serial.println("ERROR: Could not execute command UNLOCK");
                }
            }
        } else {
            Serial.print("ERROR: Unreconnized command: ");
            Serial.println(input, DEC);
        }
    }

    //Begin proximity monitoring
    // Varible to store proximity data in
    uint8_t val;

    // Get the value from the sensor
    if (ReadByte(sensorAddr, 0x0, &val) == 0) {
        /* The second LSB indicates if something was not detected, i.e.,
           LO = object detected, HI = nothing detected */
        if (val & 0x2) {
            Serial.println("Nothing detected");
            digitalWrite(led_pin, LOW);    // sets the LED off
            delay(2);
        } else {
            Serial.println("Object detected");
            digitalWrite(led_pin, HIGH);   // sets the LED on
            delay(2);
        }
    } else {
        Serial.println("Failed to read from sensor");
    }

    // Run again in 1 s (1000 ms)
    delay(1000);
}

// Read a byte on the i2c interface
int ReadByte(uint8_t addr, uint8_t reg, uint8_t *data)
{
    // Do an i2c write to set the register that we want to read from
    Wire.beginTransmission(addr);
    Wire.write(reg);
    Wire.endTransmission();

    // Read a byte from the device
    Wire.requestFrom(addr, (uint8_t)1);
    if (Wire.available()) {
        *data = Wire.read();
    } else {
        // Read nothing back
        return -1;
    }

    return 0;
}

// Write a byte on the i2c interface
void WriteByte(uint8_t addr, uint8_t reg, byte data) {
    // Begin the write sequence
    Wire.beginTransmission(addr);

    // First byte is to set the register pointer
    Wire.write(reg);

    // Write the data byte
    Wire.write(data);

    // End the write sequence; bytes are actually transmitted now
    Wire.endTransmission();
}

/******************************************************************************
* Determines the current state of the door
*
* Tasks:
* 1.)   Read analog data from the servos internal potentiometer
* 2.)   Map the potentiometer data to an angle
* 3.)   If angle is close to the defined LOCK value return 1
* 4.)   If angle is close to the defined UNLOCK value return 0
* 5.)   If the lock is in an indeterminate state then return -1
*
******************************************************************************/
int lock_status() {
    int angle; // variable to read the value from the analog pin
    pot_val = analogRead(pot_pin); // read the value of the potentiometer
    angle = map(pot_val, 0, 1023, 0, 179);

    print_info();

    if(angle > (LOCK -20) && angle < (LOCK + 20)){
        return 1;
    } else if(angle > (UNLOCK -20) && angle < (UNLOCK + 20)) {
        return 0;
    } else {
        return -1;
    }

}

/******************************************************************************
* Print the current state of the servo motor
*
* Tasks:
* 1.)   Read analog input from the potentiometer of the servo
* 2.)   Map the potentiometer data to angles
* 3.)   Check current lock status
* 4.)   Print all data out through serial
*
******************************************************************************/
void print_info() {
    int curr_angle, status; 
    pot_val = analogRead(pot_pin); // read the value of the potentiometer
    cur_angle = map(pot_val, 0, 1023, 0, 179);
    status = lock_status();

    //print out the value to the serial monitor
    Serial.print("Lock Status: ");
    Serial.println(status);
    Serial.print("Potent: ");
    Serial.println(pot_val);
    Serial.print("Angle: ");
    Serial.println(curr_angle);
}

/******************************************************************************
* Will either lock or unlock the door 
* 
* Tasks:
* 1.)   Attach to the Servo motor
* 2.)   Read the curent position of the lock
* 3.)   If the door is already in its desired location do nothing
* 4.)   If the door is not in the desired location then set the servo angle
* 5.)   Move the servo to the desired location
* 6.)   Detach the servo to allow manual locking and unlocking.
*
******************************************************************************/
int lock(int lock_pos) {
    door.attach(9);
    int status, angle;
    if (lock_pos == 1) {
        Serial.println("Now Locking");
    } else {
        Serial.println("Now Unlocking");
    }

    // Read the position of the lock currently
    status = lock_status();

    if (status == lock_pos) {
        Serial.println("ALREADY ins desired state.");
        return 0;
    } else {
        print_info();
        if (lock_pos == 1) {
            angle = LOCK;
        } else if (lock_pos == 0) {
            angle = UNLOCK;
        }
    }


    // set the servo position  
    Serial.print("Moving Servo to [");
    Serial.print(angle);
    Serial.println("] now.");

    door.write(angle);
    delay(2000);

    // Detach servo so manual override of the door can take place
    door.detach();

    return lock_status();
}



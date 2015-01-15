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

// Lock angle definitions
#define LOCK        180
#define UNLOCK      30

// Time Definitions
#define PRX_WAIT 	10000		// Time to wait before locking after proximity trigger
#define SYS_WAIT	2			// Short pasue to allow system to catch up	
#define RUN_WAIT	50			// Time to wait before starting loop again
#define CAL_WAIT	1500		// Time to wait for the calibrator
#define ADJ_WAIT	1000		// Time to wait for the Servo to adjust
#define DSR_WAIT	500			// Delay before locking after the door sensor is triggered
#define AFT_WAIT	1500		// Time to wait to allow door to complete its task

// Functions declarations
extern int ReadByte(uint8_t addr, uint8_t reg, uint8_t *data);
extern void WriteByte(uint8_t addr, uint8_t reg, byte data);
extern int lock_status();
extern int lock(int lock_pos);
extern void print_info();
extern void calibrate();
extern int door_position();


//Prototypes
//int lock(int);

// Set the sensor address here
const uint8_t sensorAddr = SENSOR_ADDR_OFF_OFF;
int led_pin = 11;       // LED connected to digital pin 13
int servo_pin = 9;      //Digital pin to control the servo
int pot_pin = A0; 		// analog pin used to connect the potentiometer
int pot_val = -1;       // variable to read the value from the analog pin 
int pot_lock = 0;
int pot_unlock = 0;
int input;
int door_pin = 2;
int lockdown = 0;
//global counter
int gc = 0;
int lockdown_counter = 0;

int led_cool[2] = {255, 0};
int door_sensor = -1;

// Servo Object
Servo door;

// One-time setup
void setup()
{
    // Start the serial port for output
    Serial.begin(9600);

    // Pin to connet to the pi
    pinMode(led_pin, OUTPUT);      // sets the digital pin as output

    // Set door sensor as an input
    pinMode(door_pin, INPUT);

    // Join the I2C bus as master
    Wire.begin();

    // Adrress for the proximity sensor 
    WriteByte(sensorAddr, 0x3, 0xFE);

	// Calibrates the definitions of the potentiometer values
    calibrate();

}

// Main program loop
void loop() {
    int stat;

    //Beginig Serial monitoring
    if (Serial.available() > 0) {
        input = Serial.read();
        if (input == '0' || input == '1' || input == '2' || input == '3' || input == '9'){
            if( input == '1') {
                if (lock(1) != 1) {
                    Serial.println("ERROR: Could not execute command LOCK");
                }
            } else if ( input == '0') {
                if (lock(0) != 0) {
                    Serial.println("ERROR: Could not execute command UNLOCK");
                }
            } else if ( input == '2' ){
                stat = lock_status();
                if (stat == 1) {
                    Serial.println("LOCKED");
                } else if (stat == 0){
                    Serial.println("UNLOCKED");
                } else {
                    Serial.println("ERROR");
                }
            } else if ( input == '9' ) {
                lockdown = !lockdown;
                if ( lockdown ) {
                    Serial.println("ATTN: LOCKDOWN ENABLED");
                } else {
                    Serial.println("ATTN: LOCKDOWN DISABLED");
                }

            } else {
                calibrate();
            }
        } else {
            Serial.print("ERROR: Unreconnized command: ");
            char out = input;
            Serial.print("(");
            Serial.print(out);
            Serial.print(")");
        }
    }

    //Begin proximity monitoring
    // 1. Connect one end of the cable into either Molex connectors on the sensor
    //Connect the other end of the cable to the Arduino board:
    //RED: 5V
    //WHITE:  I2C SDA (pin A4 on Uno; pin 20 on Mega)
    //BLACK: GND
    //GREY: I2C SCL (pin A5 on Uno; pin 21 on Mega)
    //Set the DIP switch on the sensor to set the sensor address (check back of sensor for possible addresses)
    // Varible to store proximity data in
    uint8_t val;

    // Get the value from the sensor
    if (ReadByte(sensorAddr, 0x0, &val) == 0) {
        /* The second LSB indicates if something was not detected, i.e.,
           LO = object detected, HI = nothing detected */
        if (val & 0x2) {
            //Serial.println("Nothing detected");
            delay(SYS_WAIT);
        } else {
            Serial.println("Proximity Sensor: Object detected");

            if (lock(0) != 0) {
                Serial.println("ERROR: Could not execute command UNLOCK");
            }
            delay(PRX_WAIT);
            if (lock(1) != 1) {
                Serial.println("ERROR: Could not execute command LOCK");
            }

            delay(SYS_WAIT);
        }
    } else {
        Serial.println("Failed to read from sensor");
    }

    // check if the door is unlocked. 
    // lock it after about 20 (0*0.05) seconds 
    // if no more interaction detected.
    if (lock_status() != 1){
        if ( lockdown ) {
            lockdown_counter++;
            if (lockdown_counter == 1)
                Serial.println("UNLOCKED");
        }
        if ( gc >= 1200 ){
            lock(1);
        } else {
            gc++;
        }
    } else {
      gc = 0;
      lockdown_counter = 0;
    }

    // Check wheater the door is open or closed using the Magetic door sensor.
    door_position();

    // Run again in 0.5 s (500 ms)
    delay(RUN_WAIT);
}

// Read a byte on the i2c interface
int ReadByte(uint8_t addr, uint8_t reg, uint8_t *data) {
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

// Returns the position of the door.
int door_position() {
    return digitalRead(door_pin);
    //return 1; //If no door switch
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

void calibrate () {
    //unlock the door to read the potvalue 
    door.attach(9);
    door.write(UNLOCK);
    delay(CAL_WAIT);
    door.detach();
    delay(ADJ_WAIT);
    // read the value of the potentiometer
    pot_unlock = analogRead(pot_pin); 
    // print out the value to the serial monitor
    Serial.print("Defined unlock: ");
    Serial.println(pot_unlock);

    //lock the door to read the potvalue 
    door.attach(9);
    door.write(LOCK);
    delay(CAL_WAIT);
    // read the value of the potentiometer
    door.detach();
    delay(ADJ_WAIT);
    pot_lock = analogRead(pot_pin); 
    // print out the value to the serial monitor
    Serial.print("Defined lock: ");
    Serial.println(pot_lock);
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
    int rv = -1;

	pot_val = analogRead(pot_pin); // read the value of the potentiometer

    //print_info();

    if(pot_val > (pot_lock -15) && pot_val < (pot_lock + 15)){
		
        rv = 1;
    } else if(pot_val > (pot_unlock -15) && pot_val < (pot_unlock + 15)) {
        rv = 0;
    } else {
        rv = -1;
    }
	
	// Turns on the door led light when the door is unlocked
    if (rv == 0) {
        //digitalWrite(led_pin, HIGH);   // sets the LED on
		analogWrite(led_pin,led_cool[0]);
		if(led_cool[1]){
			led_cool[0] = led_cool[0] + 5;  
			if (led_cool[0] >= 255) {
				led_cool[1] = 0;
				led_cool[0] = 255;
			}
		} else {
			led_cool[0] = led_cool[0] - 5;
			if (led_cool[0] <= 0) {
				led_cool[1] = 1;
				led_cool[0] = 0;
			}
		}

    } else {
        //digitalWrite(led_pin, LOW);    // sets the LED off
		analogWrite(led_pin, 0);    // sets the LED off
		led_cool[0] = 255;
    }

	return rv;
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

    pot_val = analogRead(pot_pin); // read the value of the potentiometer

    //print out the value to the serial monitor

    Serial.print("Potent: ");
    Serial.println(pot_val);

}

/******************************************************************************
 * Will either lock (1) or unlock (0) the door 
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

    int l_status = lock_status();
    int angle;
    int door_open = 1;
    if (lock_pos == 1) {
        Serial.println("----LOCKING----");
    } else if (lock_pos == 0) {
        Serial.println("----UNLOCKING----");
    } else {
        Serial.print("Unreconized command for lock():");
        Serial.println(lock_pos);
    }

    // Read the position of the lock currently
    if (l_status == lock_pos) {
        Serial.println("ALREADY ins desired state.");
        return lock_pos;
    } else {
        //print_info();
        if (lock_pos == 1) {
            angle = LOCK;
        } else if (lock_pos == 0) {
            angle = UNLOCK;
        }
    }


    // set the servo position  
    if (angle == LOCK) {
        // Waits till the door is closed before locking.
		while (door_open == 1) {
            if (door_position() == 1) {
                delay(DSR_WAIT);
                door.attach(9);
                door.write(LOCK);
                door_open = 0;
            } else {
                continue;
            }
        }
	// No need to wait for the door to close to unlock
    } else {
        door.attach(9);
        door.write(UNLOCK);
    }
	delay(AFT_WAIT);
    // Detach servo so manual override of the door can take place
    door.detach();

	delay(ADJ_WAIT);

    return lock_status();
}


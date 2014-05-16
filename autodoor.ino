/*
  Servo control for Autodoor.
 */

// include the servo library
#include <Servo.h>
#define LOCK        123
#define UNLOCK      321

Servo door;  // create a servo object 

int const potPin = A0; // analog pin used to connect the potentiometer

void setup() {
  door.attach(9); // attaches the servo on pin 9 to the servo object 
  Serial.begin(9600); // open a serial connection to your computer
  door.write(91); // Stops the servo from moving.
  delay(1500);
}

int lock_status() {
    int pos; // variable to read the value from the analog pin
    pos = analogRead(potPin); // read the value of the potentiometer
    if(pos == LOCK){
        return 1;
    } else if(pos == UNLOCK) {
        return 0;
    } else {
        return -1;
    }
}

int lock(int lock_pos) {
    int status, angle;
    if (lock_pos == 1) {
        Serial.print("Now Locking");
    } else {
        Serial.print("Now Unlocking");
    }
    
    // Read the position of the lock currently
    status = lock_status();
    
    if (status == lock_pos) {
        return 0;
    } else {
        if (lock_pos == 1) {
            angle = LOCK;
        } else if (lock_pos == 0) {
            angle = UNLOCK;
        }
    }
    
    //print out the value to the serial monitor
    Serial.print("Lock Status: ");
    Serial.print(status);
    
    Serial.print(", angle: ");
    Serial.println(angle); 
    
    // set the servo position  
    door.write(angle); // Stops the servo from moving.
    delay(15);
    
    if (lock_status() == lock_pos) {
        return 0;
    } else {
        return -1;
    }
}

void loop() {
    int input;
    //angle = map(potVal, 0, 1023, 0, 179);

    if (Serial.available() > 0) {
        input = Serial.read();
        if (input == 1 || input == 0){
            if (lock(input) != 0) {
                Serial.print("ERROR: Could not execute command");
                Serial.println(input, DEC);
            }
        } else {
            Serial.print("ERROR: Unreconnized command: ");
            Serial.println(input, DEC);
        }
    }
}

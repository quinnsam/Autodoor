/******************************************************************************
 * This program automates a door for keyless unlocking                         *
 * Developed by: Sam Quinn, Chauncey Yan, Ashley Greenacre, and Chris Harper.  *
 * 05/13/2014                                                                  *
 ******************************************************************************/
#include <Wire.h>
#include <Servo.h>
#include "pitches.h"
#include <SoftwareSerial.h>

SoftwareSerial XBee(2, 3); // RX, TX
// Lock angle definitions
#define LOCK            100
#define UNLOCK          0

// Time Definitions
#define SYS_WAIT	1000			// Short pasue to allow system to catch up	
#define RUN_WAIT	400			// Time to wait before starting loop again
#define CAL_WAIT	1500		        // Time to wait for the calibrator
#define DSR_WAIT	500			// Delay before locking after the door sensor is triggered
#define AFT_WAIT	1000		        // Time to wait to allow doorlock to complete its task
#define ERR_WAIT	1000		        // Time to wait to redo after ERROR
#define STAT_WAIT	100		        // Time to wait to redo befro read the pot in lock_status()

// Functions declarations

extern int lock_status();
extern int lock(int lock_pos);
extern void print_info();
extern void calibrate();
extern void calibrate_unlock();
extern void calibrate_lock();
//extern int door_position();
extern void melodyTone();

// Varial declearation

int input = 1;            // input variable from serial
int stat;                 // Variable for lock status
int led_pin = 10;         // LED connected to digital pin 10 (PWM)
int servo_pin = 9;        // Digital pin to control the servo
int pot_pin = A0; 	      // analog pin used to connect the potentiometer
int pot_val = -1;         // variable to read the value from the analog pin 
int pot_mid = 190;        // pot variable for calibrate bidirectional
int pot_lock = 250;       // pot value for lock
int pot_unlock = 0;       // pot value for unlock
int pot_tole = 100;       // pot variable for pot tolerance
int trigPin = 12;         // Ultrasonic sensor trig singal out 
int echoPin = 11;         // ultrasonic sensor echo singal in 
int xbeeIn = 6;           // xbee input pin       
int duration, distance;   // Ultrasonic unlock sensor
int Buzzer = 8;           // buzzer pin
int BuzzerGnd = 7;        // buzzer GND
int door_pin = 13;        // door detector pin
int door_sensor = -1;     // door detector value
int gc = 30;              // global counter

int led_cool[2] = {255, 0}; 

// Servo Object
Servo door;

// One-time setup
void setup()
{
    // Start the serial port for output
    Serial.begin(9600);
    XBee.begin(9600);
    
    // Pin to connet to the pi
    pinMode(led_pin, OUTPUT);      // sets the digital pin as output

    // Set door sensor as an input
    pinMode(door_pin, INPUT);

    // Join the I2C bus as master
    Wire.begin();
    
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    pinMode(Buzzer, OUTPUT);
    pinMode(BuzzerGnd, OUTPUT);
    pinMode(xbeeIn, INPUT);
    digitalWrite(BuzzerGnd, LOW);
    
    melodyTone();
    
    // Calibrates the definitions of the potentiometer values
    calibrate();
    //if (pot_unlock > 475)
    //  calibrate();
      
    delay(SYS_WAIT);

}

// Main program loop
void loop() {
  //Beginig Serial monitoring
  if (XBee.available() > 0) {
      input = XBee.read();
      // If data comes in from serial monitor, send it out to XBee
      if (input == '0' || input == '1' || input == '2' || input == '3'){
          if( input == '1') {
              if (lock(1) != 1) {
                  XBee.println("ERROR: Could not execute command LOCK");
                  errorTone();
                  delay(ERR_WAIT);
                  if (lock(1) != 1) {
                  XBee.println("ERROR: Could not execute command LOCK");
                  errorTone();
                  }
              }
          } else if ( input == '0') {
              if (lock(0) != 0) {
                  XBee.println("ERROR: Could not execute command UNLOCK.");
                  errorTone();
                  delay(ERR_WAIT);
                  if (lock(0) != 0) {
                  XBee.println("ERROR: Could not execute command UNLOCK twice.");
                  errorTone();
                  }
              }
          } else if ( input == '2' ){
              stat = lock_status();
              if (stat == 1) {
                  XBee.println("LOCKED");
              } else if (stat == 0){
                  XBee.println("UNLOCKED");
              } else {
                  XBee.println("ERROR");
              }
          } else {
              calibrate();
         }
      } else if (byte(input) == 13){
          //XBee.println("s/e");
      } else {
          XBee.print("ERROR: Unreconnized command: ");
          byte out = input;
          XBee.print("(");
          XBee.print(out);
          XBee.print(")");
      }
  }

  
  // Get the distance value from the ultrasonic sensor
  // issue : the first value will be really small
  digitalWrite(trigPin, HIGH);         // transmit sound wave out
  delayMicroseconds(10);             	 // transmit last 10 uS
  digitalWrite(trigPin, LOW);          // stop transmit
  duration = pulseIn(echoPin, HIGH);   // read from echo pin for travel duration
  distance = (duration/2) / 29.1;      // calculate distance
  // trying to solve the issue above
  
  if ( gc == 30 )
    distance = 15;
  //Serial.print("Dis1 ");
  //Serial.println(distance);

  if (distance >= 15 || distance <= 0){
    //Serial.println("no object detected");
    digitalWrite(Buzzer, LOW);         // do nothing 
  }else {
    XBee.println("Object detected");      // unlock the door
    
    // make sure there is a solid object;
    digitalWrite(trigPin, HIGH);         // transmit sound wave out
    delayMicroseconds(10);                // transmit last 10 uS
    digitalWrite(trigPin, LOW);          // stop transmit
    duration = pulseIn(echoPin, HIGH);   // read from echo pin for travel duration
    distance = (duration/2) / 29.1;      // calculate distance
    
    //Serial.print("Dis2 ");
    //Serial.println(distance);

    if (distance >= 15 || distance <= 0){
      //Serial.println("no object detected");
      digitalWrite(Buzzer, LOW);         // do nothing 
    }else {
      XBee.println("Solid object detected");      // unlock the door
      if (lock(0) != 0) {
        XBee.println("ERROR: Could not execute command UNLOCK");
        errorTone();
        delay(ERR_WAIT);
        if (lock(0) != 0) {
          XBee.println("ERROR: Could not execute command UNLOCK");
          errorTone();
        }
      }
      delay(AFT_WAIT);
    }
  }

  // check if the door is unlocked. 

  if (lock_status() != 1){
    
    // Check wheater the door is open or closed using the Magetic door sensor.
    // Waits till the door is closed before locking.
    while (door_position() == 1){
      gc = 20;
    }
    
    
    // lock it after about 12 (30*0.4) seconds 
    // if no more interaction detected.
    if ( gc >= 30 ){
      lock(1);
    } else {
      gc++;
    }
  } else {
    gc = 0;
  }

//  if (digitalRead(xbeeIn) == 0){
//    if (lock(1) != 1) {
//      Serial.println("ERROR: Could not execute command LOCK");
//      errorTone();
//      delay(ERR_WAIT);
//    }
//  }else if (digitalRead(xbeeIn) == 1){
//    if (lock(0) != 0) {
//      Serial.println("ERROR: Could not execute command UNLOCK");
//      errorTone();
//      delay(ERR_WAIT);
//    }
//  }
 
  // Run again in 0.4 s (400 ms)
  delay(RUN_WAIT);
}

// Returns the position of the door.
int door_position() {
    return digitalRead(door_pin);
}

void calibrate() {
  if (analogRead(pot_pin) < pot_mid) {
    calibrate_unlock();
    calibrate_lock();
  } else {
    calibrate_lock();
    calibrate_unlock();
    calibrate_lock();
  }
}

void calibrate_unlock () {
    //unlock the door to read the potvalue 
    door.attach(9);
    door.write(UNLOCK);
    delay(CAL_WAIT);
    door.detach();
    // read the value of the potentiometer
    pot_unlock = analogRead(pot_pin); 
    // print out the value to the serial monitor
    XBee.print("Defined unlock: ");
    XBee.println(pot_unlock);
}

void calibrate_lock () {
    //lock the door to read the potvalue 
    door.attach(9);
    door.write(LOCK);
    delay(CAL_WAIT);
    door.detach();
    // read the value of the potentiometer
    pot_lock = analogRead(pot_pin); 
    // print out the value to the serial monitor
    XBee.print("Defined lock: ");
    XBee.println(pot_lock);
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
    
    delay(STAT_WAIT);              // prevent it from reading bad value
    pot_val = analogRead(pot_pin); // read the value of the potentiometer

    //print_info();
    
    if(pot_val > 200 && pot_val < (pot_lock + pot_tole)){
	rv = 1;
    } else if(pot_val > (pot_unlock - pot_tole) && pot_val < (pot_unlock + pot_tole)) {
        rv = 0;
    } else {
        rv = -1;
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

    XBee.print("pot_val: ");
    XBee.println(pot_val);
    XBee.print("pot_unlock: ");
    XBee.println(pot_unlock);
    XBee.print("pot_lock: ");
    XBee.println(pot_lock);

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
    
    if (lock_pos == 1) {
        XBee.println("----LOCKING----");
    } else if (lock_pos == 0) {
        XBee.println("----UNLOCKING----");
    } else {
        XBee.print("Unreconized command for lock():");
        XBee.println(lock_pos);
    }
    // Read the position of the lock currently
    if (l_status == lock_pos) {
        XBee.println("ALREADY ins desired state.");
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
        door.attach(9);
        door.write(LOCK);
        locktone();
    } else {
        door.attach(9);
        door.write(UNLOCK);
        unlocktone();
    }
    delay(AFT_WAIT);
    // Detach servo so manual override of the door can take place
    door.detach();

    return lock_status();
}


void melodyTone() {
  // notes in the melody:
  int melody[] = {
  NOTE_C4, NOTE_G3,NOTE_G3, NOTE_A3, NOTE_G3,0, NOTE_B3, NOTE_C4};

  // note durations: 4 = quarter note, 8 = eighth note, etc.:
  int noteDurations[] = { 4, 8, 8, 4,4,4,4,4 };
  
  // iterate over the notes of the melody:
  for (int thisNote = 0; thisNote < 8; thisNote++) {
    
    // to calculate the note duration, take one second 
    // divided by the note type.
    //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
    int noteDuration = 800/noteDurations[thisNote];
    tone(8, melody[thisNote],noteDuration);

    // to distinguish the notes, set a minimum time between them.
    // the note's duration + 30% seems to work well:
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    
    // stop the tone playing:
    noTone(8);
  }
}

void unlocktone(){ // keep these two funtion under 1000 ms
    tone(Buzzer, 800);          // play 400 Hz tone for 500 ms
    delay(250);
    tone(Buzzer, 600);          // play 800Hz tone for 500ms
    delay(250);
    tone(Buzzer, 800);          // play 400 Hz tone for 500 ms
    delay(250);
    //tone(Buzzer, 400);          // play 800Hz tone for 500ms
    //delay(250);
    noTone(Buzzer);
}
void locktone(){ // keep these two funtion under 1000 ms
    tone(Buzzer, 600);          // play 400 Hz tone for 500 ms
    delay(250);
    tone(Buzzer, 800);          // play 800Hz tone for 500ms
    delay(250);
    tone(Buzzer, 600);          // play 400 Hz tone for 500 ms
    delay(250);
    //tone(Buzzer, 400);          // play 800Hz tone for 500ms
    //delay(250);
    noTone(Buzzer);
}
void errorTone(){ 
   tone(Buzzer, 1000);
   delay(100);
   tone(Buzzer, 600);
   delay(100);
   noTone(Buzzer); 
}

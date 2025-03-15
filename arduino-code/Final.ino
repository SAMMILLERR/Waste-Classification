#include <cvzone.h>
#include <Servo.h>

SerialData serialData(1, 1);
Servo sl;
int v[1];

void setup() {
  serialData.begin(9600);
  sl.attach(9);
  
  pinMode(12, OUTPUT);
}

void loop() {
  // Read data from the sensor or input source
  serialData.Get(v);

  int angleOffset = 0;
  digitalWrite(12, HIGH);

  if (v[0] == 2) {
    // Non Plastic detected
    angleOffset = 45;
    sl.write(90 + angleOffset);
    
    delay(1000);
    sl.write(90);
    
    delay(1000);
  }

  if (v[0] == 1) {
    // Plastic detected
    angleOffset = -45;
    sl.write(90 + angleOffset);
    digitalWrite(12, LOW);
    delay(1000);
    sl.write(90);
    digitalWrite(12, HIGH);
    delay(1000);
  }
}

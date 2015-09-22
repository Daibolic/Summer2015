int pirPin = 7;
int ledPin = 8;
int sensorPin = A0;
bool printOn = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(pirPin, LOW);
  
  //PIR sensor calibration
  Serial.print("Calibrating PIR sensor ");
  for (int i = 0; i<3; i++){
    Serial.print(".");
    delay(1000);
  }
  Serial.println(" done");
  Serial.println(" PIR sensor ACTIVE");

}

void loop() {
  // put your main code here, to run repeatedly:
  int reading= analogRead(sensorPin);
  
  float voltage = (reading*5.0)/1024.0;
  float tempC = voltage*100;
  float tempF = (tempC * 9.0/5.0) + 32.0;
  
  if (digitalRead(pirPin) == HIGH) {
    digitalWrite(ledPin, HIGH);
    if (!printOn) {
      Serial.println("Motion detected, temperature is ");
      Serial.print(tempC);
      Serial.print(" degrees C and ");
      Serial.print(tempF);
      Serial.println(" degrees F");
      printOn = true;
    }
  }
  
  
  if (digitalRead(pirPin) == LOW) {
    digitalWrite(ledPin, LOW);
    printOn = false;
  }

}

int sensorPin = A0;
int ledPin = 13;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  int reading = analogRead(sensorPin);
  
  float voltage = reading*5.0;
  voltage /= 1024.0;
  
  //Serial.print(voltage);
  //Serial.println(" volts");
  
  float tempC = (voltage)*100;
  
  //Serial.print(tempC);
  //Serial.println(" degrees C");
  
  //float tempF = (tempC * 9.0/5.0) + 32.0;
  
  //Serial.print(tempF);
  //Serial.println(" degrees F");
  
  if (tempC >= 27) {
    Serial.print("Hot and temp is ");
    Serial.println(tempC);
  } else if (tempC < 26) {
    Serial.print("Cold and temp is ");
    Serial.println(tempC);
  } else {
    Serial.print("Temperature is ");
    Serial.println(tempC);
  }
  delay(3000);

}

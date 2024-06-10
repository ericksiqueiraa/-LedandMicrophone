#include <Arduino.h>
#define led 3

void setup()
{
  Serial.begin(9600);
  pinMode(led, OUTPUT);
}

void loop()
{
  while (Serial.available())
  {
    char command = Serial.read();

    if (command == '1')
    {
      digitalWrite(led, HIGH);
    }
    else if (command == '0')
    {
      digitalWrite(led, LOW);
    }
  }
}

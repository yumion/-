/*
 * Test turn on LED on for one second,then off for one second
 */

int led = 13;

void setup() {
  // put your setup code here, to run once:
  pinMode(led,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
digitalWrite(13,HIGH);//13番pinを1へ
delay(2000);
digitalWrite(13,LOW);//13番pinを0へ
delay(1000);
}

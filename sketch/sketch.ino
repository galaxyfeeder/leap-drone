const int MAX_DC_33 = 169;
const int PIN_THROTTLE = 3;
const int PIN_YAW = 6;
const int PIN_PITCH = 9;
const int PIN_ROLL = 5;


void setup() {
  Serial.begin(9600);
  analogWrite(PIN_THROTTLE, 0);
  analogWrite(PIN_YAW, 100);
  analogWrite(PIN_PITCH, 100);
  analogWrite(PIN_ROLL, 100);
  delay(5000);
}

void loop() {
  int a = Serial.read();
  int b = Serial.read();
  int c = Serial.read();
  if(a != -1){
    a -= 48;
    analogWrite(PIN_THROTTLE, a*20);
  }
  if(b != -1){
    b -= 48;
    analogWrite(PIN_PITCH, b*20);
  }
  if(c != -1){
    c -= 48;
    analogWrite(PIN_ROLL, 1*20);
  }
}

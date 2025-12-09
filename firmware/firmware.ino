#include <Servo.h>

Servo pan;
Servo tilt;

const int min = 20;
const int max = 175;

float x = 90.0;
float y = (float)max;

String read(unsigned long timeout = 1000) {
  String buffer = "";

  unsigned long start = millis();
  while (true) {
    while (Serial.available() > 0) {
      char character = (char)Serial.read();
      if (character == '\r') continue;
      if (character == '\n') {
        return buffer;
      } else {
        buffer += character;
        if (buffer.length() > 200) {
          buffer = buffer.substring(buffer.length() - 200);
        }
      }
    }

    if (timeout > 0 && (millis() - start) > timeout) {
      return "";
    }
  }
}

void move(String command) {
  command.trim();
  int sep = command.indexOf(';');

  if (sep == -1) {
    Serial.println("ERROR: invalid format. e.g: 10;20");
    return 0;
  }

  String sx = command.substring(0, sep);
  String sy = command.substring(sep + 1);

  sx.trim();
  sy.trim();

  float dx = sx.toFloat();
  float dy = sy.toFloat();

  x += dx;
  y += dy;

  if (y > max) {
    y = max;
  }
  if (y < min) {
    y = min;
  }
  tilt.write((int)y);

  if (x > max) {
    x = 180;
  } 
  if (x < 0) {
    x = 0;
  }
  pan.write((int)x);
}

void setup() {
  Serial.begin(9600);

  pan.attach(6);
  tilt.attach(3);

  pan.write(x);
  tilt.write(y);
}

void loop() {
  String command = read();
  if (command.length() > 0) {
    move(command);
  }
}
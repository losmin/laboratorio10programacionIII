#include <Servo.h>

Servo servoMotor;

void setup() {
  servoMotor.attach(9); // Conecta el servo al pin 9
  Serial.begin(9600);   // Inicia comunicación serial a 9600 bps
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();
    switch (comando) {
      case '1':
        girar(180); // Gira a la derecha
        break;
      case '2':
        girar(0); // Gira a la izquierda
        break;
      case '3':
        girar(90); // Gira 90 grados
        break;
      case '4':
        girar(180); // Gira 180 grados
        break;
      case '5':
        girar(270); // Gira 270 grados
        break;
      case '6':
        girar(0); // Gira 360 grados (vuelve a posición inicial)
        break;
    }
  }
}

void girar(int angulo) {
  servoMotor.write(angulo);
  delay(500); // Espera 0.5 segundos
}

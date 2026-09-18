# Como funciona un motor
En la sesión 4 el tema abarcado fue acerca de como sirve un motor y un servo motor mediante un codigo en arduino y para esta practica se necesito la pagina web que ayuda a simular circuitos y programarlos.
llamada **Tinkercad**.
## 1. Motor en tinkercad
Lo primero que se debe de hacer es poner los componentes que se van a usar y en este caso son :
- un motor
- un arduino 
- una pila de 9 v
- jumpers 
- puente-h

Posteriormente el circuito queda armado de la siguiente manera :

![Circuito1](../recursos/imgs/Tremendous%20Blorr%20(1).png)

El codigo que se ejecuto para que se pudiera mover el motor fue el siguiente :
```
void adelante(){
  digitalWrite(3,HIGH);
  digitalWrite(4,LOW);
}

void setup()
  //MOTOR 1
{
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  
  digitalWrite(5,HIGH);
}

void loop()
{
 adelante();
 delay(1000); 
}
```

Posteriormente se conecta un segundo motor y para eso el circuito quedaria de la siguiente manera :
![Circuito2](../recursos/imgs/Tremendous%20Blorr%20(2).png)

Y lo unico que cambia en el codigo es lo siguiente:
```
void adelante(){
  digitalWrite(3,HIGH);
  digitalWrite(4,LOW);
  
  digitalWrite(7,HIGH);
  digitalWrite(8,LOW);
  
}

void atras(){
  digitalWrite(4,HIGH);
  digitalWrite(3,LOW);
  
  digitalWrite(8,HIGH);
  digitalWrite(7,LOW);
}

void setup()
  //MOTOR 1
{
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  
  //Motor2
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  
  
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  
  digitalWrite(5,HIGH);
  digitalWrite(6,HIGH);
}

void loop()
{
 adelante();
 delay(1000); 
  
}
```
Solo se agrega en que pines estan conectados las terminales del motor.
# 2. Servomotor con motores

El circuito quedaria armado de la siguiente manera :

![Circuito con servomotor](../recursos/imgs/Tremendous%20Blorr%20(3).png)

En donde el codigo quedaria de la misma manera solo que se agrega la libreria `` # include <Servo.h>`` :

```
# include <Servo.h>
Servo Minitur_motor;


void adelante(){
  digitalWrite(3,HIGH);
  digitalWrite(4,LOW);
  
  digitalWrite(7,HIGH);
  digitalWrite(8,LOW);
  
}

void atras(){
  digitalWrite(4,HIGH);
  digitalWrite(3,LOW);
  
  digitalWrite(8,HIGH);
  digitalWrite(7,LOW);
}

void setup()
  //MOTOR 1
{
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  
  //Motor2
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  
  // Servo Minitur
  Minitur_motor.attach(11);
  
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  
  digitalWrite(5,HIGH);
  digitalWrite(6,HIGH);
}

void loop()
{
  
 Minitur_motor.write(0);
 delay(1000);
 Minitur_motor.write(90);
 delay(1000); 
 Minitur_motor.write(180);
 delay(1000);
  
 adelante();
 delay(1000); 
  
}
```

Y eso fue todo lo que se vio en la clase #4.

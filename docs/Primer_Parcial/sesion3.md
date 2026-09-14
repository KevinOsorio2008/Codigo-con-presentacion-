# Conociendo como es un control remoto

## 1. Programando un led
Como primer paso que se realizo antes de hacer el control remoto fue hacer un circuito basico para encender un led con ayuda de un **DOIT ESP32 DEVKIT V1**  . Algo basico y sencillo de hacer y a cotinuación se muestra el [video del circuito ](https://youtube.com/shorts/7GQBfP9BR-s).
Este circuito abarca el siguiente codigo en **Arduino**

```
void setup(){
    pinMode(25,OUTPUT);
} 

void loop(){
    digitalWrite(25,HIGH);
    delay(1000);
    digitalWrite(25,LOW);
    delay(1000);
}
```
## 2. Prendiendo un led y apagando otro led 
Despues de haber ejecutado el codigo posteriormente se realizó un nuevo codigo para dos led's que pudieran prenderse y apagarse y este fue el [Resultado](https://youtube.com/shorts/mQbgPaAtfeI). Y para este nuevo circuito se desarrolló el siguiente codigo :
```
void setup(){
    pinMode(25,OUTPUT);
    pinMode(26,OUTPUT);
} 

void loop(){
    digitalWrite(25,HIGH);
    digitalWrite(26,LOW);
    delay(1000);
    digitalWrite(25,LOW);
    digitalWrite(26,HIGH);
    delay(1000);
}
```

## 3.Circuito con un boton
Posteriormente se hizo el mismo circuito y lo que se cambió fue un led por un boton para que pueda recibir información de cuando se presiona y así pueda mandar señal a la terminal de arduino y cambie lo que se este ejecutando. [video](https://youtube.com/shorts/0A6uvm1gV4k)

El codigo fue el siguiente :
 ```
 void setup() {
    Serial.begin(9600);
    pinMode(32,INPUT);
 }

 void loop (){
    if(digitalRead(32)==HIGH){
        Serial.println("PRESIONADO");
    }else{
        Serial.println("NO PRESIONADO")
    }
    delay(1000);

 }
 ```
## Control remoto

A partir de este circuito es cuando se hace el control remoto , ya que se agrega la libreria de `#include "BluetoothSerial.h"` y a partir de ahi se desarrolla el codigo el cual quedo de la siguiente manera :
```
#include "BluetoothSerial.h"

BluetoothSerial Mi_cel;
void setup(){
    Mi_cel.begin("ControlRemoto");
    Mi_cel.setTimeout(20);
    Serial.begin(9600);
    pinMode(32,INPUT);
}

void loop(){
    if(digitalRead(32)==HIGH){
        Mi_cel.println("SI");
    }else{
        Mi_cel.println("NO");
    }
    delay(1000);
}
```
Lo que ocurre en este codigo es que al momento en el que se agrega la libreria y la variable de como se llama en este caso `Mi_cel.begin("ControlRemoto")` se le asigna el nombre de **ControlRemoto** y este aparecera al momento de conectarse por bluetooth,
posteriormente lo que se indica bajo este programa es que cuando se presiona el boton , este mandara una señal al dispositivo al que este conectado y aparecera `SI` cuando este presionado el boton y cuando no lo este aparecera `NO ` y este fue el [resultado](https://youtube.com/shorts/vAfb1LFuVSU) 
## 4. Control remoto prendiendo un led

Finalmente lo que se realizó fue un codigo el cual hiciera que prendiera un led mediante un mensaje desde el dispositivo al que estuviera conectado.
```
#include "BluetoothSerial.h"

BluetoothSerial Mi_cel;
void setup(){
    Mi_cel.begin("ControlRemoto");
    Mi_cel.setTimeout(20);
    Serial.begin(9600);
    pinMode(32,OUTPUT);
}

void loop(){
    if(Mi_cel.available ()){
        String texto = Mi_cel.readStringUntil('\n');
        texto.trim();
        if(texto == "ON"){
            digitalWrite(32,HIGH);
        }
        if(texto == "OFF"){
            digitalWrite(32,LOW);
        }

    }
    
}
```
Lo que sucede en este codigo es casi lo mismo del codigo anterior pero lo que cambia es que trata de encontrar si hay datos entrantes por bluetooth de manera constante y al momento de recibir un texto el cual termine en salto de linea `(\n)` remueve espacios centrales y si el mensaje o texto es `ON` el led prendera y si es `OFF` se apaga y asi es como quedo el resultado del [circuito](https://youtube.com/shorts/xfyCgblwXQM) 

Finalmente este circuito fue el que nos ayudó a entender como funciona un control remoto por bluetooth.
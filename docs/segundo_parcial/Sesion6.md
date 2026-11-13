# Vision por computadora 

En esta sesion se introdujo el tema de pixeles , y vision por computadora el cual se basa por imagenes.

```cpp
# 01 - Estructura base: abrir la cámara y mostrar el video en vivo
import cv2
 
cap = cv2.VideoCapture(0)  # prueba 0/1/2 si tienes varias cámaras
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")
 
# Opcional: fija resolución (si la cámara lo permite)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
 
while True:
    ok, frame = cap.read()
    if not ok:
        break
 
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # presiona 'q' para salir
        break
 
cap.release()
cv2.destroyAllWindows()
```
---
### Codigo numero 2
```cpp
# 02 - Recolor: cambiar el espacio de color del video (BGR -> GRAY / RGB / HSV)
import cv2
 
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")
 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
 
while True:
    ok, frame = cap.read()
    if not ok:
        break
    # OG frame
 
    # Cambia la constante para probar otros espacios de color:
    #   cv2.COLOR_BGR2GRAY  -> escala de grises (1 canal)
    #   cv2.COLOR_BGR2RGB   -> invierte el orden de los canales
    #   cv2.COLOR_BGR2HSV   -> Matiz, Saturación, Valor
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    cv2.imshow("Ventana", frame)  # Muestra la foto original
    cv2.imshow("Gris", gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # presiona 'q' para salir
        # Imprime un pedacito de la imagen para ver cómo se guardan los números
        print(frame[0:3, 0:3])
        break
 
cap.release()
cv2.destroyAllWindows()
```
---
### codigo numero 3
```cpp
# 03 - Quitar un canal de color (poner una capa en 0)
# OpenCV guarda la imagen como [alto][ancho][canal] en orden BGR:
#   BLUE 0 | GREEN 1 | RED 2
import cv2
 
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")
 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
 
while True:
    ok, frame = cap.read()
    if not ok:
        break
    # OG frame
 
    no_color = frame.copy()
    no_color[:, :, 2] = 0   # quita el rojo (prueba con 0 o 1)
 
    # También se puede hacer solo en una zona (filas 0-360, toda la anchura):
    # no_color[0:360, :, 2] = 0
 
    cv2.imshow("Ventana", frame)  # Muestra la foto
    cv2.imshow("Sin rojo", no_color)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # presiona 'q' para salir
        break
 
cap.release()
cv2.destroyAllWindows()
```
## Codigo numero 4
```cpp
# 04 - Dividir la imagen (1280x720) en 4 cuadrantes y dejar un color en cada uno
#   BLUE 0 | GREEN 1 | RED 2
import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ok, frame = cap.read()
    if not ok:
        break
    # OG frame

    no_color = frame.copy()
    # Arriba-izquierda: solo AZUL (quita rojo y verde)
    no_color[0:360, 0:640, 2] = 0
    no_color[0:360, 0:640, 1] = 0

    # Abajo-izquierda: solo ROJO (quita azul y verde)
    no_color[360:720, 0:640, 0] = 0
    no_color[360:720, 0:640, 1] = 0

    # Arriba-derecha: solo VERDE (quita rojo y azul)
    no_color[0:360, 640:1280, 2] = 0
    no_color[0:360, 640:1280, 0] = 0

    # Abajo-derecha: NEGRO (quita los tres canales)
    no_color[360:720, 640:1280, 2] = 0
    no_color[360:720, 640:1280, 0] = 0
    no_color[360:720, 640:1280, 1] = 0

    # Variante vista en clase (cian / magenta / amarillo):
    # quitar SOLO un canal por cuadrante, p. ej.
    # no_color[0:360, 0:640, 2] = 0       -> cian
    # no_color[360:720, 0:640, 1] = 0     -> magenta
    # no_color[0:360, 640:1280, 0] = 0    -> amarillo

    cv2.imshow("Cuadrantes", no_color)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # presiona 'q' para salir
        break

cap.release()
cv2.destroyAllWindows()

```
## Codigo numero 5
```cpp
# 05 - Segmentación por color en HSV (máscara)
# En OpenCV: H (matiz) va de 0-179, S y V van de 0-255.
import cv2
import numpy as np
 
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")
 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
 
while True:
    ok, frame = cap.read()
    if not ok:
        break
    # OG frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # Rango de VERDE (ajusta según tu iluminación)
    low  = np.array([35,  60,  60], dtype=np.uint8)
    high = np.array([85, 255, 255], dtype=np.uint8)
    # Para AZUL se probó: low=[100, 60, 60], high=[130, 255, 255]
 
    filtro = cv2.inRange(hsv, low, high)                       # máscara blanco/negro
    filtrada = cv2.bitwise_and(frame, frame, mask=filtro)      # solo el color elegido
 
    cv2.imshow("mask", filtro)
    cv2.imshow("Original", frame)  # Muestra la foto
    cv2.imshow("HSV", filtrada)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # presiona 'q' para salir
        break
 
cap.release()
cv2.destroyAllWindows()
 
```
## Codigo numero 6 
```cpp
# 06 - Limpieza morfológica de la máscara (erosión y dilatación)
import cv2
import numpy as np
 
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")
 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # "pincel" de 5x5
 
while True:
    ok, frame = cap.read()
    if not ok:
        break
    # OG frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    low  = np.array([35,  60,  60], dtype=np.uint8)
    high = np.array([85, 255, 255], dtype=np.uint8)
    filtro = cv2.inRange(hsv, low, high)
 
    # En clase se probó primero erode(iterations=10) y dilate(iterations=100)
    # para ver el efecto exagerado. Versión final (dilatar y luego erosionar = cierre):
    erosion = cv2.dilate(filtro, kernel, iterations=2)
    erosion = cv2.erode(erosion, kernel, iterations=2)
 
    filtrada = cv2.bitwise_and(frame, frame, mask=erosion)
    cv2.imshow("mask", filtro)
    cv2.imshow("Erosion", erosion)
    cv2.imshow("HSV", filtrada)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # presiona 'q' para salir
        break
 
cap.release()
cv2.destroyAllWindows()
 
```
### Codigo numero 6 
```cpp
# 07 - Dibujar figuras y texto sobre el video
import cv2
 
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")
 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
 
while True:
    ok, frame = cap.read()
    if not ok:
        break
 
    #cv2.line(imagen, punto1, punto2, color, grosor, tipo de linea)
    cv2.line(frame, (0, 0), (280, 80), (0, 255, 0), thickness=3, lineType=cv2.LINE_AA)
    #cv2.circle(imagen, centro, radio, color, grosor (-1 es lleno), tipo de linea)
    cv2.circle(frame, (230, 180), 20, (0, 0, 255), thickness=5, lineType=cv2.LINE_AA)
    #cv2.ellipse(imagen, centro, (ancho, alto), angulo, inicio, fin, color, grosor, tipo de linea)
    cv2.ellipse(frame, (290, 315), (80, 35), 0, 0, 360, (255, 0, 0), thickness=3, lineType=cv2.LINE_AA)
    #cv2.rectangle(imagen, punto1, punto2, color, grosor, tipo de linea)
    cv2.rectangle(frame, (310, 160), (380, 200), (255, 0, 255), thickness=5, lineType=cv2.LINE_8)
    #cv2.putText(imagen, texto, punto, fuente, escala, color, grosor, tipo de linea)
    cv2.putText(frame, "Hola Mundo!", (20, 450), cv2.FONT_HERSHEY_COMPLEX, 1.5, (250, 255, 255), 2, cv2.LINE_AA)
 
    '''
    cv2.LINE_8: Conectividad de 8, predeterminado, conexión diagonal y ortogonal.
    cv2.LINE_4: Conectividad de 4, solo conexión ortogonal.
    cv2.LINE_AA: Línea suavizada (anti-aliasing), líneas más suaves y estéticas.
    '''
 
    cv2.imshow("Original", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # presiona 'q' para salir
        break
 
cap.release()
cv2.destroyAllWindows()
 
```
### Codigo ocho
```cpp
# 08 - Programa final de la clase: color -> limpieza -> contornos -> centro
import cv2  # Importar libreria de vision OPENCV
import time
import numpy as np
 
cap = cv2.VideoCapture(0)  # prueba 0/1/2 si tienes varias cámaras
 
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")
 
# Opcional: fija resolución (si la cámara lo permite)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
 
while True:
    ok, frame = cap.read()
    if not ok:
        break
    # OG frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #BLUE 0
    #GREEN 1
    #RED 2
    low  = np.array([35,  60,  60], dtype=np.uint8)
    high = np.array([85, 255, 255], dtype=np.uint8)
    filtro = cv2.inRange(hsv, low, high)
    erosion = cv2.dilate(filtro, kernel, iterations=2)
    erosion = cv2.erode(erosion, kernel, iterations=2)
    filtrada = cv2.bitwise_and(frame, frame, mask=erosion)
    contours, _ = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area < 200:  # filtra ruido muy pequeño
            continue
 
        # Dibujo del contorno:
        cv2.drawContours(filtrada, [c], -1, (0, 255, 0), 2)
 
        # Rectángulo axis-aligned:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(filtrada, (x, y), (x + w, y + h), (255, 0, 0), 2)
 
        # Círculo mínimo envolvente:
        (cx, cy), rad = cv2.minEnclosingCircle(c)
        cv2.circle(filtrada, (int(cx), int(cy)), int(rad), (0, 255, 255), 2)
 
        # Centroides con momentos:
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx_m = int(M["m10"] / M["m00"])
            cy_m = int(M["m01"] / M["m00"])
            cv2.circle(filtrada, (cx_m, cy_m), 4, (0, 0, 255), -1)
            cv2.putText(filtrada, f"({cx_m},{cy_m})", (cx_m + 6, cy_m - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
 
    cv2.imshow("mask", filtro)
    cv2.imshow("Erosion", erosion)
    # Muestra la foto
    cv2.imshow("HSV", filtrada)
    cv2.imshow("Original", frame)
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
```
### Codigo numero 9
```cpp
# Detección de color azul con la cámara
# Pasos: desenfoque -> HSV -> máscara -> limpiar ruido -> contornos -> centro
import cv2
import numpy as np
 
camara = cv2.VideoCapture(0)
if not camara.isOpened():
    raise RuntimeError("No se pudo abrir la cámara")
 
# Rango del color azul en HSV (en OpenCV H va de 0 a 179)
azul_min = np.array([95, 80, 50], dtype=np.uint8)
azul_max = np.array([130, 255, 255], dtype=np.uint8)
 
# Filtro para quitar manchitas y rellenar huecos
filtro = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
 
# Área mínima para ignorar objetos muy chiquitos
area_minima = 1000
 
while True:
    ret, imagen = camara.read()
    if not ret:
        break
 
    # Quito ruido y paso a HSV
    suave = cv2.medianBlur(imagen, 9)
    hsv = cv2.cvtColor(suave, cv2.COLOR_BGR2HSV)
 
    # Dejo solo lo que sea azul
    mascara = cv2.inRange(hsv, azul_min, azul_max)
 
    # Abrir quita puntitos de ruido, cerrar rellena huecos
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, filtro, iterations=1)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, filtro, iterations=2)
 
    # Imagen donde solo se ve lo azul
    resultado = cv2.bitwise_and(imagen, imagen, mask=mascara)
 
    # Busco los contornos de lo que quedó
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    for cont in contornos:
        if cv2.contourArea(cont) < area_minima:
            continue
 
        # Dibujo el contorno
        cv2.drawContours(resultado, [cont], -1, (0, 255, 0), 2)
 
        # Rectángulo que rodea el objeto
        x, y, ancho, alto = cv2.boundingRect(cont)
        cv2.rectangle(resultado, (x, y), (x + ancho, y + alto), (0, 0, 255), 2)
 
        # Centro del objeto con momentos
        m = cv2.moments(cont)
        if m["m00"] != 0:
            centro_x = int(m["m10"] / m["m00"])
            centro_y = int(m["m01"] / m["m00"])
            cv2.circle(resultado, (centro_x, centro_y), 8, (255, 255, 0), -1)
            print("Centro:", centro_x, centro_y)
 
    cv2.imshow("Camara", imagen)
    cv2.imshow("Color azul detectado", resultado)
 
    # Con la tecla q se cierra
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
camara.release()
cv2.destroyAllWindows()
```
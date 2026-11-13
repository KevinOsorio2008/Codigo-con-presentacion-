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

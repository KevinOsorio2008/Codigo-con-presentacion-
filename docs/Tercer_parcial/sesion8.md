# VISION POR COMPUTADORA PT.2

```
#ERROR APARTIR DEL CENTRO

import cv2
import numpy as np
import time
import math
import serial   



actual=time.time()
#Formula Error
'''
Error = meta-donde estoy
'''
mx=320
my=240
error_x=0
error_y=0
error_x_ant=0
error_y_ant=0
Kp=2
Kd=1
Ki=0.5
anterior=time.time()
integral_x=0
integral_y=0
L=15
r=5


PORT="COM8"
#
qr_detector = cv2.QRCodeDetector()
aruco_dict = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_50
)
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict)
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    bt=serial.Serial(PORT, 115200, timeout=0.1, write_timeout=0.1)
    if not ret:
        if bt is not None:
            bt.close()
        break
    
    # --- QR Code Detection ---
    data, points, _ = qr_detector.detectAndDecode(frame)
    if points is not None:
        pts = points.reshape(4, 2)
        cx, cy = np.mean(pts, axis=0).astype(int)
        cv2.polylines(frame, [pts.astype(int)], True,
                      (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        cv2.putText(frame, f"QR: ({cx}, {cy})",
                    (cx + 10, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 0), 2)
    # --- ArUco Detection ---
    corners, ids, _ = aruco_detector.detectMarkers(frame)
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        for marker_id, corner in zip(ids.flatten(), corners):
            pts = corner.reshape(4, 2)
#Centro de mi ARUCO
            cx, cy = np.mean(pts, axis=0).astype(int)

            frente_x, frente_y = (pts[1]+pts[2])/2
            theta_actual = math.atan2((cy-frente_y),(cx-frente_x))
            cv2.line(frame, (int(frente_x),int(frente_y)),(cx,cy),(127,127,127), thickness=2, lineType=cv2.LINE_AA)
            cv2.putText(frame, f"theta ({theta_actual})",
                                    (0,80),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 0, 0), 2)



            #ERROR CON RESPECTO A EL CENTRO DE MI PANTALLA (MX,MY)
            error_x=mx-cx
            error_y=my-cy
            actual=time.time()
            dif_tiempo = actual - anterior
            anterior=actual


            #SACA EL TIEMPO TRANSCURRIDO
            derivada_x =(error_x - error_x_ant)/dif_tiempo
            derivada_y =(error_y - error_y_ant)/dif_tiempo
            error_y_ant= error_y
            error_x_ant= error_x


            #CALCULA LA INTEGRAL DEL ERROR
            integral_x= integral_x + error_x*dif_tiempo
            integral_y= integral_y + error_y*dif_tiempo


            #CALCULA LA VELOCIDAD LINEAL PARA MOVERME
            Vx=error_x*Kp + Kd * derivada_x + Ki * integral_x
            Vy=error_y*Kp + Kd * derivada_y + Ki * integral_y
            print(f"Vx: {Vx}, Vy: {Vy}")

            cv2.circle(frame, (cx, cy), 5,
                       (0, 0, 255), -1)
            cv2.line(frame, (mx,my),(cx,cy),(127,127,127), thickness=2, lineType=cv2.LINE_AA)
            cv2.putText(frame, f"ID {marker_id}: ({cx}, {cy})",
                        (cx + 10, cy + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 0, 0), 2)
            cv2.circle(frame, (mx, my), 5,
                                   (255, 255, 0), -1)

        cv2.putText(frame,f"E_x: {error_x},E_y: {error_y}",
                    (0,15), cv2.FONT_HERSHEY_SIMPLEX,1.0,(255, 255, 0), -2)

    cv2.imshow("QR + ArUco Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



#convertir a velocidad robot 
theta_deseado= math.atan2(Vy,Vx) 
dif_theta= theta_deseado - theta_actual
#pasar por un P
Kp_theta=1
V= math.hypot(Vx, Vy) #unidades de pixeles por segundo
w=Kp_theta*dif_theta 

wheel_left=(V -L*w)/r
wheel_right=(V +L*w)/r

if bt is not None:
    #crear mensaje
    mensaje = f"{wheel_left},{wheel_right}\n"
    bt.write(mensaje.encode("ascii"))



cv2.circle(frame, (mx, my), 5,
                       (0, 0, 255), -1)

cap.release()
bt.close()
cv2.destroyAllWindows()

```
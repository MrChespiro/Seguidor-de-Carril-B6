import cv2 as cv
from gpiozero import AngularServo
import numpy as np
from simple_pid import PID

servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)
cap = cv.VideoCapture(0)
from gpiozero import PWMLED
led = PWMLED(12)
kp = 1.4
ki =0.005
kd =0.002
pid = PID(kp, ki, kd, setpoint=0,output_limits=(-25, 25))

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv.resize(frame, (240, 180), fx = 0, fy = 0,
                         interpolation = cv.INTER_CUBIC)

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Otsu's thresholding
    ret2,th2 = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
   
    cv.line(frame,(120,0),(120,180),(0,255,0),1)
    cv.line(frame,(15,110),(15,110),(0,255,0),1)
    cv.line(frame,(0,110),(240,110),(0,255,0),1)
   
    x1=120
    x2=120
    x3=120
    x4=120
    x5=120
    x6=120
   
    while x1>0: #coordenada izquierda centro
        img=int(th2[140][x1]/255)
        if img==0:
            break
        x1=x1-1
       
    while x2<240: #coordenada derecha centro
        img=int(th2[140][x2]/255)
        if img==0:
            break
        x2=x2+1
       
    while x3>0: #coordenada izquierda bajo
        img=int(th2[102][x3]/255)
        if img==0:
            break
        x3=x3-1
       
    while x4<240: #coordenada derecha bajo
        img=int(th2[102][x4]/255)
        if img==0:
            break
        x4=x4+1

    """while x5>0: #coordenada izquierda arriba
        img=int(th2[0][x5]/255)
        if img==0:
            break
        x5=x5-1
       
    while x6<240: #coordenada derecha arriba
        img=int(th2[0][x6]/255)
        if img==0:
            break
        x6=x6+1"""

       
    angle2=-(((x4+x3)/2)-120)*1.4 #angulo abajo
    pidout=pid(angle2)
    pidout = pidout* -1
    servo= pidout

    if -70<=servo<=70:
        servo.angle = (servo)
    if -47<servo<-26:
        led.value=0.9
    elif servo.angle<-47:
        led.value=0.85
    else:
        led.value=0.36
   
    print("angulo: ",servo.angle, " value: ", led.value)

    cv.imshow('Otsus Thresh', th2)
    # Display the resulting frame
    cv.imshow('Frame', frame)
    # define q as the exit button
    if cv.waitKey(25) & 0xFF == ord('q'):
        break
       
led.value=0
# release the video capture object
cap.release()
# Closes all the windows currently opened.
cv.destroyAllWindows()

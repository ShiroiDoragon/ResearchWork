import cv2
import numpy as np
from array import *

if __name__ == '__main__':
    def callback(*arg):
        print (arg)

cv2.namedWindow( "result" )
#1.3, 1.5, 0.5, 0.5
fps=10
CountFrame = 0
LongDiod = 1.3
LongDark = 1.5
ShortDiod = 0.5
ShortDark = 0.5
CountLongDiod = int(fps*LongDiod)
CountLongDark = int(fps*LongDark)
CountShortDiod = int(fps*ShortDiod)
CountShortDark = int(fps*ShortDark)
x1 = 0
y1 = 0
cap = cv2.VideoCapture('2.mp4')
# HSV фильтр для синих объектов
#0, 0, 250
#255, 85, 255
CodeSequence = array('i', [])
for i in range(CountLongDiod):
    CodeSequence.append(1)
for i in range(CountLongDark):
    CodeSequence.append(0)
for i in range(CountShortDiod):
    CodeSequence.append(1)
for i in range(CountShortDark):
    CodeSequence.append(0)
for i in range(CountShortDiod):
    CodeSequence.append(1)
for i in range(CountShortDark):
    CodeSequence.append(0)
for i in range(CountShortDiod):
    CodeSequence.append(1)
print(CodeSequence)
print("\n")
print(len(CodeSequence))
flug = True
while True:
    flag, img = cap.read()
    img = cv2.resize(img , (800, 600)) 
    #crop_img = img[10:200, 300:500]
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB )
    
    hsv_min = np.array((0, 0, 250), np.uint8)
    hsv_max = np.array((255, 85, 255), np.uint8)
    # применяем цветовой фильтр
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)
    # вычисляем моменты изображения
    moments = cv2.moments(thresh, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']
    # будем реагировать только на те моменты,
    # которые содержать больше 100 пикселей
    
    if dArea > 5:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        x1 = x
        y1 = y
        cv2.rectangle(img, (x-15, y-15), (x+15, y+15), (0,0,255), 2)
    if flug: 
        print(CountFrame)        
        if dArea > 5:
            if CodeSequence[CountFrame] == 1:
                CountFrame += 1
            else:
                CountFrame = 0
        else:
            if CodeSequence[CountFrame] == 0:
                CountFrame += 1
            else:
                CountFrame = 0     
        if CountFrame==len(CodeSequence):
            flug = False         
    else:
        
        cv2.rectangle(img, (x1-15, y1-15), (x1+15, y1+15), (0,255,0), 2)
        if CountFrame != 70:
            CountFrame +=1
        else:
            CountFrame = 0
            flug = True

    
    cv2.imshow('result', img) 
    cv2.imshow('obj', thresh) 
 
    ch = cv2.waitKey(50)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()
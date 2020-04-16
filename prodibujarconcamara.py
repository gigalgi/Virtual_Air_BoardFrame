#funcionamiento aqui ---> https://www.youtube.com/watch?v=t2WfPNoBO6Y

import cv2
import numpy as np


def nothing(x):
    pass
def dibujar(x,y,drawest,B,G,R,size):#funcion que permite hacer el traso en el tablero virtual
    
    draw=drawest
    x=abs(x-640)
    if draw == True:
        cv2.circle(board,(x,y),size,(B,G,R),-1)    

captura = cv2.VideoCapture(0)#captura de video
board = np.ones((480,640,3), np.uint8)*255 #tamano del tablero
conf = np.zeros((640,480,3), np.uint8) # tamano del panel de configuracion

#valores de inicio prederterminados para color del lapiz,tamanao del lapiz y borrador
cv2.namedWindow('Tablero',cv2.WINDOW_NORMAL)
cv2.namedWindow('Configuracion',cv2.WINDOW_NORMAL)
cv2.createTrackbar('R','Configuracion',0,255,nothing)
cv2.createTrackbar('G','Configuracion',0,255,nothing)
cv2.createTrackbar('B','Configuracion',0,255,nothing)
cv2.createTrackbar('Lapiz','Configuracion',5,100,nothing)
cv2.createTrackbar('Borrador','Configuracion',20,100,nothing)

tb,tl=20,5#tamano del lapiz y borrador predeterminado

while True:
    #Capturamos una imagen y la convertimos de RGB -> HSV
    _, imagen = captura.read()
    captura.set(3,640)
    captura.set(4,480) 
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    #filtro Bilateral
    hsvblur = cv2.bilateralFilter(hsv,9,50,75)
    #Establecemos el rango de colores que vamos a detectar
    #Verde para escrbir Azul para borrar
    #En este caso de verde oscuro a verde-azulado claro
    verde_bajos = np.array([49,50,50], dtype=np.uint8)
    verde_altos = np.array([80, 255, 255], dtype=np.uint8)

    #En este caso de azul oscuro a azulado claro claro
    azul_bajos = np.array([100,65,75], dtype=np.uint8)
    azul_altos = np.array([130, 255, 255], dtype=np.uint8)
 
    #Crear una mascara con solo los pixeles dentro del rango de verdes
    mascara_verde = cv2.inRange(hsvblur, verde_bajos, verde_altos)
    mascara_azul = cv2.inRange(hsvblur, azul_bajos, azul_altos)
    #Filtrar el ruido con un CLOSE seguido de un OPEN
    kernel = np.ones((5,5),np.uint8)
    mascara_verde = cv2.morphologyEx(mascara_verde, cv2.MORPH_CLOSE, kernel)
    mascara_verde = cv2.morphologyEx(mascara_verde, cv2.MORPH_OPEN, kernel)
    
    mascara_azul = cv2.morphologyEx(mascara_azul, cv2.MORPH_CLOSE, kernel)
    mascara_azul = cv2.morphologyEx(mascara_azul, cv2.MORPH_OPEN, kernel)
    #Encontrar el area de los objetos que detecta la camara
    moments = cv2.moments(mascara_verde)
    area = moments['m00']
    moments2 = cv2.moments(mascara_azul)
    area2 = moments2['m00']
    #print area
    
    if(area > 40000):#para el color verde
        #Buscamos el centro x, y del objeto
        x = int(moments['m10']/moments['m00'])
        y = int(moments['m01']/moments['m00'])
        dibujar(x,y,True,b,g,r,tl)
        #Mostramos sus coordenadas por pantalla
        #print "x = ", x,"y = ", y
        #Dibujamos una marca en el centro del objeto
        cv2.circle(imagen, (x, y), 5,(0,255,0), 3)
        cv2.line ( imagen, ( x, 0 ), ( x, 720 ), ( 0, 0, 255 ),2 )
        cv2.line ( imagen, ( 0, y ), ( 640, y ), ( 0, 0, 255 ),2 )
        
    
    elif(area2 > 40000):#para el color azul
        x2 = int(moments2['m10']/moments2['m00'])
        y2 = int(moments2['m01']/moments2['m00'])
        dibujar(x2,y2,True,255,255,255,tb)
        cv2.circle(imagen, (x2, y2), 5,(255,0,0), 3)
        cv2.line ( imagen, ( x2, 0 ), ( x2, 720 ), ( 0, 0, 255 ),2 )
        cv2.line ( imagen, ( 0, y2 ), ( 640, y2 ), ( 0, 0, 255 ),2 )
        
        
    mascara = cv2.add(mascara_verde, mascara_azul)   
    #Mostramos la imagen original con la marca del centro y la mascara
    mascara=cv2.flip(mascara,1)
    imagen=cv2.flip(imagen,1)
    cv2.imshow('Tablero',board)
    cv2.imshow('Filtrado',mascara)
    cv2.imshow('Camara',imagen)
    cv2.imshow('Configuracion',conf)
    #selecconamos los valored para el color del lapiz, el tamano del lapiz y del borrador
    r = cv2.getTrackbarPos('R','Configuracion')
    g = cv2.getTrackbarPos('G','Configuracion')
    b = cv2.getTrackbarPos('B','Configuracion')
    tl = cv2.getTrackbarPos('Lapiz','Configuracion')
    tb = cv2.getTrackbarPos('Borrador','Configuracion')
    conf[:] = [b,g,r]
        
    tecla = cv2.waitKey(5) & 0xFF # salimos del programa con la tecla esc o q
    if tecla == 27:
        captura.release()
        break
cv2.destroyAllWindows()
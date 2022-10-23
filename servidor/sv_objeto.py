"""Lo que hacemos aca es definir la clase de nuestro robot RRR. La cual contendra los
metodos y atributos de nuestro robot. Mediante "pyserial" (modulo llamado "serial")
tomaremos los datos y los enviaremos a nuestra placa arduino mediante el puerto serie
"""

import serial
import time


#Inicio de definicion de clase RobotRRR

class RobotRRR:
    
    Arduino=serial.Serial("/dev/ttyUSB1",115200,timeout=0) #timeout es el tiempo de respuesta en segundos
    Arduino.close() #Para que por defecto se encuentre cerrado
    #Definimos los metodos del robot

    #Para abrir el puerto serie para la conexion con Arduino por puerto serie
    def turnSVON(self):
        
        self.Arduino.open()
        #Aca tambien vamos a hacer el homing del robot
        self.Arduino.write(b"G28") #Ponemos la b porque el metodo solo acepta como param. tipos de dato "bytes"
        time.sleep(2) #Colocamos un tiempo de 2s para que demos tiempo al robot a reaccionar y enviarnos info
        """
        El metodo in_wating() me entrega el numero de bytes esperando en el puerto serie para ser recibidos
        por nosotros. Si es mayor a cero (hay mensajes esperando para entrar), le decimos al metodo que retorne
        lo que lee
        """
        while(self.Arduino.in_waiting()>0): 
            return self.Arduino.readline()


    #Para abrir el puerto serie para la conexion con Arduino por puerto serie
    def turnSVOFF(self):

        self.Arduino.close()

    #Para abrir o cerrar la pinza (gripper)
   # def setPinza(self,estado):
        
        #if (estado==True):
            

        

    


    










"""
flag=True
while(flag):
    time.sleep(2)
    while(Arduino.inWaiting()>0):
        print(Arduino.readline())




    mensaje=input("Ingrese comando a enviar a puerto serie: ")
    Arduino.write(bytes(mensaje+"\r\n",encoding='utf-8'))
    
    if(mensaje=="exit"):
        flag=False
"""






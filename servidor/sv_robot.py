"""Lo que hacemos aca es definir la clase de nuestro robot RRR. La cual contendra los
metodos y atributos de nuestro robot. Mediante "pyserial" (modulo llamado "serial")
tomaremos los datos y los enviaremos a nuestra placa arduino mediante el puerto serie
"""

import serial
import time



#Inicio de definicion de clase RobotRRR

class RobotRRR:



    #Para abrir el puerto serie para la conexion con Arduino por puerto serie
    def turnONPort(self):
        #Con esta excepcion, si no se puede abrir el puerto serie, se intenta cambiar el num del USB, si no se avisa que no se pudo abrir el puerto 
        try:
            self.Arduino=serial.Serial("/dev/ttyUSB0",115200,timeout=1) #timeout es el tiempo de respuesta en segundos
            time.sleep(2)
            while(self.Arduino.in_waiting>0): 
                return self.Arduino.readlines()
        except FileNotFoundError as e:
            if e.errno == 2:
                self.Arduino=serial.Serial("/dev/ttyUSB1",115200,timeout=1)
                
            else:
                print("ERROR: Conecte Arduino nuevamente")
                raise #Con raise terminamos el codigo ahi

        
        

    #Para abrir el puerto serie para la conexion con Arduino por puerto serie
    def turnOFFPort(self):

        self.Arduino.close()
        time.sleep(2)
        return "INFO: ROBOT OFFLINE"

    #Para abrir o cerrar la pinza (gripper)
    def setPinza(self,estado=False): #Falso por defecto
        
        if (estado==True):
            self.Arduino.write(b"M3")
        else:
            self.Arduino.write(b"M5")
        time.sleep(2)

        if(self.Arduino.in_waiting>0): 
            return self.Arduino.readlines()
    
    def movLineal(self,coordX,coordY,coordZ,velocidad):
        
        self.Arduino.write(bytes("g1x"+str(coordX)+"y"+str(coordY)+"z"+str(coordZ)+"e"+str(velocidad),encoding='utf-8'))
        time.sleep(2)
        while(self.Arduino.in_waiting()>0): 
            return self.Arduino.readline()
    
    def movReset(self):
        #Primero establecemos modo de coordenadas absolutas por las dudas
        self.Arduino.write(b"G90")
        #Ahora lo llevamos a la posicion de origen
        self.Arduino.write(b"g1x0y0z0e10") #Por defecto le asignamos una velocidad de 10mm/s
        

        

        

    


    










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






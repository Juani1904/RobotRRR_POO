"""Lo que hacemos aca es definir la clase de nuestro robot RRR. La cual contendra los
metodos y atributos de nuestro robot. Mediante "pyserial" (modulo llamado "serial")
tomaremos los datos y los enviaremos a nuestra placa arduino mediante el puerto serie
"""

import serial
import time
import os
#Inicio de definicion de clase RobotRRR

class RobotRRR:

    modo="" 
    file=None
    nombreArchivo=""

    def modoManual(self):
        print("¿Quiere ingresar en modo aprendizaje? Ingrese S para Si, N para NO: ")
        submodo=input().upper()
        if (submodo=="S"):
            self.modo="aprendizaje"
            self.turnONPort()
            print("Ingrese NOMBRE del archivo .txt a crear con los comandos: ", end="")
            self.nombreArchivo=input()+".txt"
            self.file=open(self.nombreArchivo,"w")
        elif (submodo=="N"):
            self.modo="manual"
        return "INFO: MODO MANUAL ACTIVADO"

    def modoAutomatico(self):
        #El modo automatico solo sera valido cuando el archivo de comandos exista, y cuando no este vacio
        #Si no se entrara directamente a modo manual
        print("Ingrese NOMBRE del archivo .txt que contiene los comandos: ", end="")
        self.nombreArchivo=input()+".txt"
        try:
            #Leemos el archivo y colocamos cada linea como elemento de una lista "listadelectura"
            archivolectura=open(self.nombreArchivo,"r")
            listadelectura=archivolectura.readlines()
            archivolectura.close() #Cerramos el archivo.Importante, si no el programa tira error
            #Primero abrimos el puerto del Arduino
            self.turnONPort()
            #Ahora mandamos al Arduino cada elemento de lista
            for comando in listadelectura:
                self.Arduino.write(bytes(comando,encoding='UTF-8'))
                time.sleep(2)
            #Cerramos el puerto serie
            self.turnOFFPort()
            #Luego volvemos al loop del CLI sv
            print("Actividad automatica finalizada. Entrando a modo manual...") #Para el CLI del servidor
            self.modoManual()
        except FileNotFoundError as e:
            if e.errno==2:
                print("Archivo no encontrado.Entra a modo manual")
                self.modoManual()
        except os.stat(self.nombreArchivo).st_size==0:
            print("Archivo vacio. Entra a modo manual")
            self.modoManual()

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
    
    #Activacion/Desactivacion de motores del robot
    def setMotores(self,estado): #Falso por defecto
        if estado=="on":
            self.Arduino.write(b"M17\r\n")
            #Para escribir el comando en el modo manual
            if self.modo=="aprendizaje" and self.file!=None:
                self.file.write("M17\r\n")
            time.sleep(2)
            return "INFO: STEPPERS ENABLED"
        elif estado=="off":
            self.Arduino.write(b"M18\r\n")
            #Para escribir el comando en el modo manual
            if self.modo=="aprendizaje" and self.file!=None:
                self.file.write("M18\r\n")
            time.sleep(2)
            return "INFO: STEPPERS DISABLED"
        
    #Para abrir o cerrar la pinza (gripper) [Actividad del efector final]
    def setPinza(self,estado="off"): #Falso por defecto
        if (estado=="on"):
            self.Arduino.write(b"M3\r\n")
            #Para escribir el comando en el modo manual
            if self.modo=="aprendizaje" and self.file!=None:
                self.file.write("M3\r\n")
        elif (estado=="off"):
            self.Arduino.write(b"M5\r\n")
            #Para escribir el comando en el modo manual
            if self.modo=="aprendizaje" and self.file!=None:
                self.file.write("M5\r\n")
        time.sleep(2)

        if(self.Arduino.in_waiting>0): 
            return self.Arduino.readlines()

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






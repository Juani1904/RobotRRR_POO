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

    #Creamos el constructor de RobotRRR.No acepta parametros, solo instancia el objeto del puerto serie

    def __init__(self):
        try:
            self.Arduino=serial.Serial("/dev/ttyUSB1",115200,timeout=1) #timeout es el tiempo de respuesta en segundos
            self.Arduino.close() #Cerramos el puerto serie para que inicie por defecto cerrado
        except serial.serialutil.SerialException as e:
            if e.errno==16: #Puerto ocupado
                print("El puerto serie se encuentra ocupado. Cierre el programa que lo esta usando")
                return "El puerto serie no se encuentra disponible. Cierre el programa que lo esta usando"
            elif e.errno==2: #Mal definicion de puerto. Puede estar en el USB0 o USB1
                self.Arduino=serial.Serial("/dev/ttyUSB0",115200,timeout=1)
                self.Arduino.close()
            
    #Metodos para activar el modo manual (aprendizaje o no) y el modo automatico

    def modoManual(self,nombreexterno=None):
        #Si el nombre externo es distinto de None, significa que se esta llamando desde el Cliente
        #Si el nombre externo es None, significa que se esta llamando desde el servidor

        #Caso cliente. Si o si entraria en modo aprendizaje, porque si no llamaria a las funciones por otro lado.
        if nombreexterno!=None:
            self.nombreArchivo=nombreexterno+".txt"
        #Caso servidor
        elif nombreexterno==None:
            print("Ingrese NOMBRE del archivo .txt a crear con los comandos: ", end="")
            self.nombreArchivo=input()+".txt"
        #Luego
        self.modo="aprendizaje"
        self.file=open(self.nombreArchivo,"w")
        return "INFO: MODO MANUAL(APRENDIZAJE) ACTIVADO"

    def modoAutomatico(self,nombreexterno=None):
        #El modo automatico solo sera valido cuando el archivo de comandos exista, y cuando no este vacio
        #Si no se entrara directamente a modo manual
        if nombreexterno!=None:
            self.nombreArchivo=nombreexterno+".txt"
        elif nombreexterno==None:
            print("Ingrese NOMBRE del archivo .txt que contiene los comandos: ", end="")
            self.nombreArchivo=input()+".txt"
        try:
            self.modo="automatico"
            #Leemos el archivo y colocamos cada linea como elemento de una lista "listadelectura"
            archivolectura=open(self.nombreArchivo,"r")
            listadelectura=archivolectura.readlines()
            archivolectura.close() #Cerramos el archivo.Importante, si no el programa tira error
            #Primero abrimos el puerto del Arduino, si no se encontrara abierto
            if self.Arduino.isOpen()==False:
                self.turnONPort()
            #Ahora mandamos al Arduino cada elemento de lista
            for comando in listadelectura:
                self.Arduino.write(bytes(comando,encoding='UTF-8').strip()) #Con strip me aseguro de eliminar los \t
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


    #Metodos de control del puerto serie y robot

    #Para abrir el puerto serie para la conexion con Arduino por puerto serie
    def turnONPort(self):
        #Con esta excepcion, si no se puede abrir el puerto serie, se intenta cambiar el num del USB, si no se avisa que no se pudo abrir el puerto 
        self.Arduino.open()
        time.sleep(2)
        while(self.Arduino.in_waiting>0): 
            return self.Arduino.readlines()
        return "INFO: ROBOT ONLINE"
        
            


    #Para abrir el puerto serie para la conexion con Arduino por puerto serie
    def turnOFFPort(self):
        self.Arduino.close()
        time.sleep(2)
        return "INFO: ROBOT OFFLINE"
    
    #Activacion/Desactivacion de motores del robot
    def setMotores(self,estado): #Falso por defecto
        
        if (estado=="on"):
            self.Arduino.write(b"M17\r\n")
            #Para escribir el comando en el modo manual
            if self.modo=="aprendizaje" and self.file!=None:
                self.file.write("M17\r\n")
            time.sleep(2)
            return "INFO: STEPPERS ENABLED"
        elif (estado=="off"):
            self.Arduino.write(b"M18\r\n")
            #Para escribir el comando en el modo manual
            if self.modo=="aprendizaje" and self.file!=None:
                self.file.write("M18\r\n")
            time.sleep(2)
            return "INFO: STEPPERS DISABLED"

        else: 
            return Exception

    #Movimiento lineal del robot
    def setPosicionLineal(self,coordX,coordY,coordZ,velocidad):
        
        self.Arduino.write(bytes("G1X"+coordX+"Y"+coordY+"Z"+coordZ+"E"+velocidad+"\r\n",encoding='utf-8'))
        if self.modo=="aprendizaje" and self.file!=None:
            self.file.write("G1\tX"+coordX+"\tY"+coordY+"\tZ"+coordZ+"\tE"+velocidad+"\r\n")
        time.sleep(2)
        while(self.Arduino.in_waiting>0): 
            return self.Arduino.readlines()
        
    #Movimiento angular del robot
    def setAngularMotor1(self,velocidad:float,sentido:str,angulo:float):
        
        #Este metodo simplemente entrega un mensaje
        return f"INFO: Valores seteados. Velocidad: {velocidad} mm/s, Sentido: {sentido}, Angulo: {angulo} grados"
    
    def setAngularMotor2(self,velocidad:float,sentido:str,angulo:float):
        
        #Este metodo simplemente entrega un mensaje
        return f"INFO: Valores seteados. Velocidad: {velocidad} mm/s, Sentido: {sentido}, Angulo: {angulo} grados"
    
    def setAngularMotor3(self,velocidad:float,sentido:str,angulo:float):
        
        #Este metodo simplemente entrega un mensaje
        return f"INFO: Valores seteados. Velocidad: {velocidad} mm/s, Sentido: {sentido}, Angulo: {angulo} grados"

    #Para abrir o cerrar la pinza (gripper) [Actividad del efector final]
    def setPinza(self,estado): #Falso por defecto
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
        while(self.Arduino.in_waiting>0): 
            return self.Arduino.readlines()
        

    def Reset(self): #Tambien llamado Homing. Sirve para que el brazo vuelva a su posicion de origen/descanso

        self.Arduino.write(b"G28\r\n")
        if self.modo=="aprendizaje" and self.file!=None:
            self.file.write("G28\r\n")
        time.sleep(2)
        while(self.Arduino.in_waiting>0): 
            return self.Arduino.readlines()
        






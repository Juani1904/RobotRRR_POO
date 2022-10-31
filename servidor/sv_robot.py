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
    fileExterno=None
    fileInterno=None

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

    def modoManual(self,nombreexterno=""):
        #Si el nombre externo es distinto de None, significa que se esta llamando desde el Cliente
        #Si el nombre externo es None, significa que se esta llamando desde el servidor
        #Caso cliente. Si o si entraria en modo aprendizaje, porque si no llamaria a las funciones por otro lado.
        #Caso cliente
        if (nombreexterno != ""):
            nombreArchivoExterno=nombreexterno+".txt"
            self.modo="aprendizaje"
            self.fileExterno=open(nombreArchivoExterno,"w")
            return "INFO: MODO MANUAL(APRENDIZAJE) ACTIVADO"
        #Caso servidor
        elif (nombreexterno==""):
            print("Ingrese NOMBRE del archivo .txt a crear con los comandos: ", end="")
            nombreArchivoInterno=input()+".txt"
            self.modo="aprendizaje"
            self.fileInterno=open(nombreArchivoInterno,"w")
            return "INFO: MODO MANUAL(APRENDIZAJE) ACTIVADO"
        

    def modoAutomatico(self,nombreexterno=""):
        #Primero, si el archivo de modo manual sigue abierto lo cerramos
        if (self.fileExterno!=None):

            self.cerrarArchivoExterno()

        if (self.fileInterno!=None):

            self.cerrarArchivoInterno()
        #El modo automatico solo sera valido cuando el archivo de comandos exista, y cuando no este vacio
        #Si no se entrara directamente a modo manual
        
        try:
            #+++++++++++++++++++LADO CLIENTE++++++++++++++++++++++
            if (nombreexterno!=""):
                self.modo="automatico"
                nombreArchivoExterno=nombreexterno+".txt"
                #Leemos el archivo y colocamos cada linea como elemento de una lista "listadelectura"
                archivolectura=open(nombreArchivoExterno,"r")
                listadelectura=archivolectura.readlines()
                archivolectura.close() #Cerramos el archivo.Importante, si no el programa tira error
                #Primero abrimos el puerto del Arduino, si no se encontrara abierto
                if self.Arduino.isOpen()==False:
                    self.turnONPort()
                #Antes de iniciar hay que verificar que no este el servidor mandando nada al Arduino
                while(self.Arduino.in_waiting>0):
                    continue #Se queda en loop hasta que no haya nada en el buffer de entrada

                #Ahora mandamos al Arduino cada elemento de lista
                listacmd=""
                for comando in listadelectura:
                    self.Arduino.write(bytes(comando,encoding='UTF-8').strip()) #Con strip me aseguro de eliminar los \t
                    time.sleep(2)
                #Cerramos el puerto serie
                self.turnOFFPort()
                #Retornamos un mensaje al cliente
                return "INFO: SECUENCIA AUTOMATICA FINALIZADA"
            #++++++++++++++++LADO SERVIDOR++++++++++++++++++++++++++++++++
            elif (nombreexterno==""):
                self.modo="automatico"
                print("Ingrese NOMBRE del archivo .txt que contiene los comandos: ", end="")
                nombreArchivoInterno=input()+".txt"
                #Leemos el archivo y colocamos cada linea como elemento de una lista "listadelectura"
                archivolectura=open(nombreArchivoInterno,"r")
                listadelectura=archivolectura.readlines()
                archivolectura.close() #Cerramos el archivo.Importante, si no el programa tira error
                #Primero abrimos el puerto del Arduino, si no se encontrara abierto
                if self.Arduino.isOpen()==False:
                    self.turnONPort()

                #Antes de iniciar hay que verificar que no este el servidor mandando nada al Arduino
                while(self.Arduino.in_waiting>0):
                    continue #Se queda en loop hasta que no haya nada en el buffer de entrada
                
                #Ahora mandamos al Arduino cada elemento de lista
                for comando in listadelectura:
                    self.Arduino.write(bytes(comando,encoding='UTF-8').strip()) #Con strip me aseguro de eliminar los \t
                    time.sleep(2)
                #Cerramos el puerto serie
                self.turnOFFPort()
                #Retornamos un mensaje al cliente
                return "INFO: SECUENCIA AUTOMATICA FINALIZADA"
                    
        except FileNotFoundError as e:
            if e.errno==2:
                print("Archivo no encontrado.")
                return "Archivo no encontrado."
                
        except os.stat(nombreArchivoExterno).st_size==0:
            return "Archivo vacio."
        
        except os.stat(nombreArchivoInterno).st_size==0:
            print("Archivo vacio.")


    #Metodos de control del puerto serie y robot

    #Para abrir el puerto serie para la conexion con Arduino por puerto serie
    def turnONPort(self):
        #Con esta excepcion, si no se puede abrir el puerto serie, se intenta cambiar el num del USB, si no se avisa que no se pudo abrir el puerto 
        self.Arduino.open()
        time.sleep(2)
        while(self.Arduino.in_waiting>0): 
            return self.Arduino.readlines()
        
            


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
            if self.modo=="aprendizaje" and self.fileExterno!=None:
                self.fileExterno.write("M17\r\n")
            if self.modo=="aprendizaje" and self.fileInterno!=None:
                self.fileInterno.write("M17\r\n")
            time.sleep(2)
            return "INFO: STEPPERS ENABLED"
        elif (estado=="off"):
            self.Arduino.write(b"M18\r\n")
            #Para escribir el comando en el modo manual
            if self.modo=="aprendizaje" and self.fileExterno!=None:
                self.fileExterno.write("M18\r\n")
            if self.modo=="aprendizaje" and self.fileInterno!=None:
                self.fileInterno.write("M18\r\n")
            time.sleep(2)
            return "INFO: STEPPERS DISABLED"

        else: 
            return Exception

    #Movimiento lineal del robot
    def setPosicionLineal(self,coordX,coordY,coordZ,velocidad):
        
        self.Arduino.write(bytes("G1X"+coordX+"Y"+coordY+"Z"+coordZ+"E"+velocidad+"\r\n",encoding='utf-8'))
        if self.modo=="aprendizaje" and self.fileExterno!=None:
            self.fileExterno.write("G1\tX"+coordX+"\tY"+coordY+"\tZ"+coordZ+"\tE"+velocidad+"\r\n")
        if self.modo=="aprendizaje" and self.fileInterno!=None:
            self.fileInterno.write("G1\tX"+coordX+"\tY"+coordY+"\tZ"+coordZ+"\tE"+velocidad+"\r\n")
        time.sleep(2)
        while(self.Arduino.in_waiting>0): 
            return self.Arduino.readlines()
        
    #Movimiento angular del robot
    def setAngularMotor1(self,velocidad:float,sentido:str,angulo:float):
        #Este metodo simplemente entrega un mensaje
        if self.Arduino.isOpen()==True:
            return f"INFO: Valores seteados. Velocidad: {velocidad} mm/s, Sentido: {sentido}, Angulo: {angulo} grados"
        if self.Arduino.isOpen()==False:
            print("El puerto serie no se encuentra abierto.Ejecute TURNONPORT")
            return "El puerto serie no se encuentra abierto.Ejecute TURNONPORT"
        
        
        
    
    def setAngularMotor2(self,velocidad:float,sentido:str,angulo:float):
        #Este metodo simplemente entrega un mensaje
        if self.Arduino.isOpen()==True:
            return f"INFO: Valores seteados. Velocidad: {velocidad} mm/s, Sentido: {sentido}, Angulo: {angulo} grados"
        if self.Arduino.isOpen()==False:
            print("El puerto serie no se encuentra abierto.Ejecute TURNONPORT")
            return "El puerto serie no se encuentra abierto.Ejecute TURNONPORT"
        

    def setAngularMotor3(self,velocidad:float,sentido:str,angulo:float):
        #Este metodo simplemente entrega un mensaje
        if self.Arduino.isOpen()==True:
            return f"INFO: Valores seteados. Velocidad: {velocidad} mm/s, Sentido: {sentido}, Angulo: {angulo} grados"
        if self.Arduino.isOpen()==False:
            print("El puerto serie no se encuentra abierto.Ejecute TURNONPORT")
            return "El puerto serie no se encuentra abierto.Ejecute TURNONPORT"
        

    #Para abrir o cerrar la pinza (gripper) [Actividad del efector final]
    def setPinza(self,estado): #Falso por defecto
        if (estado=="on"):
            self.Arduino.write(b"M3\r\n")
            #Para escribir el comando en el modo manual
            if self.modo=="aprendizaje" and self.fileExterno!=None:
                self.fileExterno.write("M3\r\n")
            if self.modo=="aprendizaje" and self.fileInterno!=None:
                self.fileInterno.write("M3\r\n")    
        elif (estado=="off"):
            self.Arduino.write(b"M5\r\n")
            #Para escribir el comando en el modo manual
            if self.modo=="aprendizaje" and self.fileExterno!=None:
                self.fileExterno.write("M5\r\n")
            if self.modo=="aprendizaje" and self.fileInterno!=None:
                self.fileInterno.write("M5\r\n")
        time.sleep(2)
        while(self.Arduino.in_waiting>0): 
            return self.Arduino.readlines()
        
    #Para realizar el HOMING del robot    
    def Reset(self): #Tambien llamado Homing. Sirve para que el brazo vuelva a su posicion de origen/descanso

        self.Arduino.write(b"G28\r\n")
        if self.modo=="aprendizaje" and self.fileExterno!=None:
            self.fileExterno.write("G28\r\n")
        if self.modo=="aprendizaje" and self.fileInterno!=None:
            self.fileInterno.write("G28\r\n")
        time.sleep(2)
        while(self.Arduino.in_waiting>0): 
            return self.Arduino.readlines()
    
    #Este metodo lo implementamos para que el cliente cuando cierre su CLI pueda cerrar el archivo para ejecutarlo
    def cerrarArchivoExterno(self):
        if self.fileExterno!=None:
            self.fileExterno.close()
            self.fileExterno=None
    
    def cerrarArchivoInterno(self):
        if self.fileInterno!=None:
            self.fileInterno.close()
            self.fileInterno=None






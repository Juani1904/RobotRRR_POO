from cmd import Cmd
import os
from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer
import time
import sys
class Consola(Cmd): #Creamos una clase Consola que hereda de la clase Cmd
    #Los "atributos" que vamos a setear aca son realmente metodos de la clase Cmd (ejemplo Cmd.intro(string))
    intro=""
    prompt="V>>"
    file=None #Atributo para guardar el archivo de comandos
    doc_header= "Ingrese help <comando> para obtener ayuda sobre el ingreso de dicho comando"

    def __init__(self,controlRobot):
        super().__init__()
        self.controlRobot=controlRobot

    #Creamos un metodo para que desde sv_main podamos meter al objeto servidor instanciado en el main
    #De esta forma ahora la consola conoce al servidor, y asi podremos habilitar o deshabilitar el sv
    def agregarSV(self,servidor):
        self.servidor=servidor
    
    
    def do_svstatus_switch(self,estado):
        'Abrir o Cerrar el servidor: svstatus_switch on/off'
        if estado =="on":
            # Se lanza el servidor en un hilo de control mediante Thread
            #Instanciamos el objeto thread
            self.servidor.thread=Thread(target=self.servidor.run_server)
            self.servidor.thread.start() #Utilizamos atributo start() del objeto thread
            print("Servidor RPC iniciado en el puerto [%s]" % str(self.servidor.server.server_address))
        elif estado =="off":
            self.servidor.shutdown()
            print("Servidor RPC en el puerto [%s] fue cerrado" % str(self.servidor.server.server_address))
    
    
    def do_turnonport(self,arg=None):
        'Activar el puerto serie: TURNONPORT'
        mensaje=""
        listamensaje=self.controlRobot.turnONPort()
        for elemento in listamensaje:
            mensaje_decoded=elemento.decode('UTF-8')
            mensaje+=mensaje_decoded
        return mensaje

    def do_turnoffport(self,arg=None):
        'Deshabilita puerto serie: TURNOFFPORT'
        mensaje=self.controlRobot.turnOFFPort()
        return mensaje
    
    def do_setmotores(self,estado):
        "Activacion/Desactivacion de los motores del robot: SETMOTORES ON/OFF"
        mensaje=self.controlRobot.setMotores(estado)
        
        return mensaje

    
    
    

    def do_setpinza(self,estado):
        'Habilitacion de pinza/gripper: estadopinza on/off'
        mensaje=""
        listamensaje=self.controlRobot.setPinza(estado)
        for elemento in listamensaje:
            mensaje_decoded=elemento.decode('UTF-8')
            mensaje+=mensaje_decoded
        return mensaje
        

    def do_posicion(self,arg):
        'Establece las nuevas coordenadas absolutas del controlRobot: posicion 1 2 3 10'
        return self.controlRobot.movLineal(arg)
    
    def do_reset(self,arg):
        'Resetea al RobotRRR a su posicion inicial: reset'
        return self.controlRobot.movReset()

    def do_exit(self,arg):
        'Salir de la consola: EXIT'
        self.cerrarArchivo() #Cerramos archivo de modo manual
        print("Saliendo de la consola...")
        time.sleep(1)
        sys.exit()



    #Metodos para la construccion y apertura de archivos de comandos
    def modoManual(self, archivo):
        self.file = open(archivo, 'w')

    def modoAutomatico(self, archivo):
        #El modo automatico solo sera valido cuando el archivo de comandos exista, y cuando no este vacio
        #Si no se entrara directamente a modo manual
        try:
            with open(archivo) as f:
                self.cmdqueue.extend(f.read().splitlines())
        except FileNotFoundError as e:
            if e.errno==2:
                print("Archivo no encontrado.Entra a modo manual")
                print("Ingrese NOMBRE del archivo .txt que contiene los comandos: ", end="")
                archivonuevo=input()+".txt"
                self.modoManual(archivonuevo)
        except os.stat(archivo).st_size==0:
            print("Archivo vacio. Entra a modo manual")
            print("Ingrese NOMBRE del archivo .txt que contiene los comandos: ", end="")
            archivonuevo=input()+".txt"
            self.modoManual(archivonuevo)
    
    def cerrarArchivo(self):
        if self.file: #Si el archivo existe, entrega un valor booleano True, si no tira False
            self.file.close()
            self.file = None



    #Metodos para el manejo de la consola

    #Este precmd me convierte los comandos ingresados a minusculas para que no haya problemas con mayusculas
    def precmd(self, line):
        line=line.lower()
        if self.file and 'modoAutomatico' not in line:
            print(line, file=self.file)
        return line

    #Este postcmd me permite que funciones do_.. que tengan un return no me lleven a un loop infinito en la consola IU Server
    def postcmd(self, stop, line):
        return False
    
    #Este default me permite que si se ingresa un comando que no existe, me entrege un mensaje personalizado
    def default(self, args):
        print("Comando no reconocido. Ingrese help para ver los comandos disponibles")
        
    #Creamos un preloop que llame a la funcion do_help para que se muestren los comandos disponibles apenas inicie la consola
    def preloop(self):
        #Creamos una pequeña animacion para el servidor antes de que se inicie

         #HABILITAR AL TERMINAR CODIGO
        print("Iniciando...")
        time.sleep(1)
        for i in range(0,101):
            time.sleep(0.05)
            print("Cargando consola IU Server...[%d%%]" % i, end="\r")
        print("Cargando consola IU Server...[100%]")
        time.sleep(0.5)
        
        print("\n\n**********Bienvenido a Veneris Server ®**********\n")
        time.sleep(0.5)
        print("Ingrese el modo de trabajo: Manual o Automatico(M/A): ", end="")
        modo=input()
        if modo=="M":
            print("Ingrese NOMBRE del archivo .txt a crear con los comandos: ", end="")
            archivo=input()+".txt"
            self.modoManual(archivo)
            pass
        elif modo=="A":
            print("Ingrese NOMBRE del archivo .txt que contiene los comandos: ", end="")
            archivo=input()+".txt"
            self.modoAutomatico(archivo)
            pass
        print("Lista de comandos disponibles:")
        time.sleep(0.5)
        self.do_help(None)
    
    

    
   

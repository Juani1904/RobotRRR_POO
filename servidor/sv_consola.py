from cmd import Cmd
"""
A tener en cuenta al usar el modulo Cmd. Cuando declaramos las funciones do_XXX, estas deben
tener como parametro obligatorio self y SIEMPRE tener un argumento, al que podemos llamar arg o args
(o de cualquier forma). Esto es asi porque el modulo Cmd, cuando llama a las funciones do_XXX, interpreta
al comando en si mismo (por ejemplo turnonport) como un argumento en si mismo.
"""
from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer
import time
import sys
class Consola(Cmd): #Creamos una clase Consola que hereda de la clase Cmd
    #Los "atributos" que vamos a setear aca son realmente metodos de la clase Cmd (ejemplo Cmd.intro(string))
    intro=""
    prompt="V>>"
    file=None
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

    def do_estadopinza(self,arg):
        'Habilitacion de pinza/gripper: estadopinza True/False'
        return self.controlRobot.setPinza(arg)

    def do_posicion(self,arg):
        'Establece las nuevas coordenadas absolutas del controlRobot: posicion 1 2 3 10'
        return self.controlRobot.movLineal(arg)
    
    def do_reset(self,arg):
        'Resetea al RobotRRR a su posicion inicial: reset'
        return self.controlRobot.movReset()

    def do_exit(self,arg):
        'Salir de la consola: EXIT'
        print("Saliendo de la consola...")
        time.sleep(1)
        sys.exit()
    #Funciones para el manejo de la consola

    #Este precmd me convierte los comandos ingresados a minusculas para que no haya problemas con mayusculas
    def precmd(self, line):
        return line.lower()

    #Este postcmd me permite que funciones do_.. que tengan un return no me lleven a un loop infinito en la consola IU Server
    def postcmd(self, stop, line):
        return False
    
    #Este default me permite que si se ingresa un comando que no existe, me entrege un mensaje personalizado
    def default(self, args):
        print("Comando no reconocido. Ingrese help para ver los comandos disponibles")
        
    #Creamos un preloop que llame a la funcion do_help para que se muestren los comandos disponibles apenas inicie la consola
    def preloop(self):
        #Creamos una pequeña animacion para el servidor antes de que se inicie

        """ HABILITAR AL TERMINAR CODIGO
        print("Iniciando...")
        time.sleep(1)
        for i in range(0,101):
            time.sleep(0.05)
            print("Cargando consola IU Server...[%d%%]" % i, end="\r")
        print("Cargando consola IU Server...[100%]")
        time.sleep(0.5)
        """
        print("\n\n**********Bienvenido a Veneris Server ®**********\n")
        time.sleep(0.5)
        print("Lista de comandos disponibles:")
        time.sleep(0.5)
        self.do_help(None)
    
    

    
   

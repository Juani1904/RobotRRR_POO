from cmd import Cmd
from sv_robot import RobotRRR
from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer
class Consola(Cmd): #Creamos una clase Consola que hereda de la clase Cmd
    controlRobot=RobotRRR()
    #Los "atributos" que vamos a setear aca son realmente metodos de la clase Cmd (ejemplo Cmd.intro(string))
    intro= "Bienvenido a Veneris Server ® . Ingresa help para ver la lista de comandos disponibles:"
    prompt="V>>"
    file=None
    doc_header= "Guia de comandos documentados (ingrese help <comando> para obtener ayuda sobre el ingreso de dicho comando)"


    #Ahora ingresamos todas las funciones que queremos que tenga
    def agregarSV(self,servidor):
        self.servidor=servidor
    
    

    def do_svstatus_switch(self,estado):
        if estado =="on":
            self.servidor.thread = Thread(target=self.servidor.run_server) #Instanciamos el objeto thead
            self.servidor.thread.start() #Utilizamos atributo start() del objeto thread
            print("Servidor RPC iniciado en el puerto [%s]" % str(self.servidor.server.server_address))
        elif estado =="off" and self.servidor is not None:
            self.servidor.shutdown()
            print("Servidor RPC en el puerto [%s] fue cerrado" % str(self.servidor.server.server_address))
    
    def run_server(self):
        
        self.servidor.serve_forever()

    def shutdown(self):
        
        self.servidor.shutdown()
        self.thread.join()
        

    def do_turnonport(self,arg=None):
        'Activar el puerto serie: turnonport'
        mensaje=""
        listamensaje=self.controlRobot.turnONPort()
        for elemento in listamensaje:
            mensaje_decoded=elemento.decode('UTF-8')
            mensaje+=mensaje_decoded
        return mensaje

    def do_turnoffport(self,arg=None):
        'Deshabilita puerto serie: turnoffport'
        mensaje=self.controlRobot.turnOFFPort()
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


    #Este postcmd me permite que funciones do_.. que tengan un return no me lleven a un loop infinito en la consola IU Server
    def postcmd(self, stop, line):
        return False
    

    
   

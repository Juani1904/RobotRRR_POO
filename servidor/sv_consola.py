from cmd import Cmd
from sv_robot import RobotRRR
class Consola(Cmd): #Creamos una clase Consola que hereda de la clase Cmd
    controlRobot=RobotRRR()
    #Los "atributos" que vamos a setear aca son realmente metodos de la clase Cmd (ejemplo Cmd.intro(string))
    intro= "Bienvenido a Veneris Server ® . Ingresa help para ver la lista de comandos disponibles:"
    prompt="V>>"
    file=None
    doc_header= "Guia de comandos documentados (ingrese help <comando> para obtener ayuda sobre el ingreso de dicho comando)"

    #Ahora ingresamos todas las funciones que queremos que tenga
    
    def do_svstatus(self,estado=False): #Falso por defecto
        'Activar el servidor: svstatus on/off'
        if (estado=="on"):
            return True
        elif (estado=="off"):
            return False

        

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
    

    
   

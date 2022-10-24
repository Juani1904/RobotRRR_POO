from cmd import Cmd
from sv_robot import RobotRRR

class Consola(Cmd): #Creamos una clase Consola que hereda de la clase Cmd
    Robot=RobotRRR()
    #Los "atributos" que vamos a setear aca son realmente metodos de la clase Cmd (ejemplo Cmd.intro(string))
    intro= "Bienvenido a Veneris ® . Ingresa help para ver la lista de comandos disponibles:"
    prompt="V>>"
    file=None
    doc_header= "Guia de comandos documentados (ingrese help <comando> para obtener ayuda sobre el ingreso de dicho comando)"

    #Ahora ingresamos todas las funciones que queremos que tenga
    def do_puertoserie_on(self,arg):
        'Habilita puerto serie: puertoserie_on'
        return self.Robot.turnSVON()

    def do_puertoserie_off(self,arg):
        'Deshabilita puerto serie: puertoserie_off'
        return self.Robot.turnSVOFF()

    def do_estadopinza(self,arg):
        'Habilitacion de pinza/gripper: estadopinza True/False'
        return self.Robot.setPinza(arg)

    def do_posicion(self,arg):
        'Establece las nuevas coordenadas absolutas del robot: posicion 1 2 3 10'
        return self.Robot.movLineal(arg)
    
    def do_reset(self,arg):
        'Resetea al RobotRRR a su posicion inicial: reset'
        return self.Robot.movReset()
    
    def precmd(self,args):
        args=args.lower()
        return(args)


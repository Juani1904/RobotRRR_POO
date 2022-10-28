#Este es el modulo de lanzamiento del servidor.

#!/usr/bin/python
# _*_ coding: utf-8 _*_

from Servidor import Servidor
from sv_robot import RobotRRR
from sv_consola import Consola


#Aca lo que vamos a hacer es instanciar o constuir el objeto objeto_vinculado, y se lo pasaremos como
#parametro a la instanciacion del objeto servidor. De esta forma mediante este modulo de lanzamiento
#establezco el vinculo entre el servidor y el servicio, que en nuestro caso particular sera el robot
if __name__=="__main__":

    objeto_vinculado=RobotRRR()
    consola=Consola(objeto_vinculado)
    servidor =Servidor(consola)
    consola.agregarSV(servidor)
    consola.cmdloop()
    



    
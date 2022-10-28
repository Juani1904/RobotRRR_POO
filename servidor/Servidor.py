from xmlrpc.server import SimpleXMLRPCServer
# El modulo xmlrpc.server y la clase SimpleXMLRPCServer me permiten establecer un servidor con protocolo XMLRPC
from threading import Thread
# Con este modulo y Thread podemos instanciar un objeto Thread o hilo que es el que va a mantener la ejecucion del sv y comunicaciones
# Basicamente es el que va a estar bloqueandose o esperando (en estado de escucha) a que un objeto se conecte
import socket
# El socket me va a permitir establecer el cinculo entre la aplicacion cliente (C++) y la aplicacion servidora (Python)
# La clase que vamos a definir ahora hace de interfaz entre el cliente y el servicio (en nuestro caso cliente y framework de Arduino)

class Servidor(object):
    server = None
    """
    Como servidor no se ha especificado a ninguno en particular, porque en el lanzamiento (instanciacion
    de self.server) le pasaremos todo
    """
    puertoRPC = 8891  # Definimos un puerto. Puede ser cualquiera, simpre y cuando este libre en el host
    
    # Definimos el constructor
    def __init__(self,Consola, port=puertoRPC): #Por defecto se establece puerto 
        # Con self.objeto_vinculado establecemnos la relacion entre la interfaz y el servicio. En este caso el framework de Arduino
        self.puerto = port
        self.consola=Consola
        while True:
            try:
                """Creacion del servidor indicando el puerto deseado. Es importante esta instanciacion
                del objeto self.server, debido a que es la que me crea el vinculo entre mi clase
                interfaz XmlRpcEjemploserver con el servidor propiamente dicho (clase servidor SimpleXMLRPCServer)
                """
                self.server = SimpleXMLRPCServer(("localhost", self.puerto), allow_none=True)
                if self.puerto != port:
                    print("Servidor RPC ubicado en puerto no estandar [%d]" % self.puerto)
                break
            #En el caso de que el puerto usado este ocupado (error 98), pasamos al siguiente, si no indicamos que no puede iniciarse el servidor
            except socket.error as e:

                if e.errno == 98:
                    self.puerto += 1
                    continue
                else:
                    print("El servidor RPC no puede ser iniciado")
                    raise
        
        #Aca, dentro del mismo constructor, registramos las funciones a ser llamadas por el cliente
        self.server.register_function(self.do_modoManual, "modomanual")
        self.server.register_function(self.do_modoAutomatico, "modoautomatico")
        self.server.register_function(self.do_turnONPort,"turnonport")
        self.server.register_function(self.do_turnOFFPort,"turnoffport")
        self.server.register_function(self.do_setMotores,"setmotores")
        self.server.register_function(self.do_setPosicionLineal,"setposicionlineal")
        self.server.register_function(self.do_setAngularMotor1,"setangularmotor1")
        self.server.register_function(self.do_setAngularMotor2,"setangularmotor2")
        self.server.register_function(self.do_setAngularMotor3,"setangularmotor3")
        self.server.register_function(self.do_setPinza,"setpinza")
        self.server.register_function(self.do_Reset,"reset")
        self.server.register_function(self.getnumOrdenes,"getnumordenes")
        self.server.register_function(self.cerrarArchivoExterno,"cerrararchivoexterno")
        self.server.register_function(self.getComandos,"getcomandos")
        self.server.register_function(self.getlistaOrdenes,"getlistaordenes")
        
    #Funciones para el iniciar y cerrar el servidor

    def run_server(self):
        
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        self.thread.join()

    #Funcion para iniciar el modo manual o de aprendizaje
  
    def do_modoManual(self,textoexterno):

        return self.consola.do_modomanual(textoexterno)

    #Funcion para iniciar el modo automatico

    def do_modoAutomatico(self,textoexterno):

        return self.consola.do_modoautomatico(textoexterno)
    
    #Funcion para abrir el puerto serie
    def do_turnONPort(self):
         
        return self.consola.do_turnonport()
    
    #Funcion para cerrar el puerto serie
    
    def do_turnOFFPort(self):
        
        return self.consola.do_turnoffport()
    
    #Funcion para habilitar o deshabilitar los motores del robot

    def do_setMotores(self,estado):

        return self.consola.do_setmotores(estado)
    
    #Funcion para mover el brazo a un punto determinado linealmente
    
    def do_setPosicionLineal(self,coordX,coordY,coordZ,velocidad):
        parametros=str(coordX)+" "+str(coordY)+" "+str(coordZ)+" "+str(velocidad)
        return self.consola.do_setposicionlineal(parametros)
    
    #Funcion para controlar de manera angular el Motor1 del robot

    def do_setAngularMotor1(self,velocidad,sentido,angulo):
        parametros=str(velocidad)+" "+str(sentido)+" "+str(angulo)
        return self.consola.do_setangularmotor1(parametros)
    
    #Funcion para controlar de manera angular el Motor2 del robot
    def do_setAngularMotor2(self,velocidad,sentido,angulo):
        parametros=str(velocidad)+" "+str(sentido)+" "+str(angulo)
        return self.consola.do_setangularmotor2(parametros)
    
    #Funcion para controlar de manera angular el Motor3 del robot
    
    def do_setAngularMotor3(self,velocidad,sentido,angulo):
        parametros=str(velocidad)+" "+str(sentido)+" "+str(angulo)
        return self.consola.do_setangularmotor3(parametros)
    
    #Funcion para controlar la apertura y cierre de la pinza del robot
    
    def do_setPinza(self,estado):

        return self.consola.do_setpinza(estado)
    
    #Funcion para resetear el robot (hacer HOMING)

    def do_Reset(self):

        return self.consola.do_reset()
    
    #Definimos los getters solo accesibles mediante el servidor
    def getnumOrdenes(self):
        return self.consola.getnumOrdenes()
    
    def getlistaOrdenes(self):
        return self.consola.getlistaOrdenes()
    
    #Metodo para cerrar el archivo de modo manual, para que el cliente lo pueda cerrar remotamente
    def cerrarArchivoExterno(self):
        self.consola.controlRobot.cerrarArchivoExterno()
        return 0
    
    def getComandos(self):
        listacomandos=["modomanual","modoautomatico","turnonport","turnoffport","setmotores","setposicionlineal","setangularmotor1","setangularmotor2","setangularmotor3","setpinza","reset"]
        return listacomandos
    

    
    

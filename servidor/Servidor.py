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
    def __init__(self, Robot,Consola, port=puertoRPC): #Por defecto se establece puerto 
        # Con self.objeto_vinculado establecemnos la relacion entre la interfaz y el servicio. En este caso el framework de Arduino
        self.Robot = Robot
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
       
        self.server.register_function(self.do_turnONPort,"turnonport")
        self.server.register_function(self.do_turnOFFPort,"turnoffport")
        self.server.register_function(self.do_setMotores,"setmotores")
        self.server.register_function(self.do_setPosicionLineal,"setposicionlineal")
        self.server.register_function(self.do_setAngularMotor1,"setangularmotor1")
        self.server.register_function(self.do_setAngularMotor2,"setangularmotor2")
        self.server.register_function(self.do_setAngularMotor3,"setangularmotor3")
        self.server.register_function(self.do_setPinza,"setpinza")
        self.server.register_function(self.do_Reset,"reset")


    #Ahora definimos metodos que tendra mi clase Servidor

    def run_server(self):
        
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        self.thread.join()

  
    def modoManual(self):

        return self.consola.modoManual()

    def modoAutomatico(self):

        return self.consola.modoAutomatico()
   
    def do_turnONPort(self):
         
        return self.consola.do_turnonport()
    
    def do_turnOFFPort(self):
        
        return self.consola.do_turnoffport()

    def do_setMotores(self,estado):

        return self.consola.do_setmotores(estado)
    

    def do_setPosicionLineal(self,parametros):

        return self.consola.do_setposicionlineal(parametros)

    
    def do_setAngularMotor1(self,parametros):

        return self.consola.do_setangularmotor1(parametros)

    def do_setAngularMotor2(self,parametros):

        return self.consola.do_setangularmotor2(parametros)
    
    def do_setAngularMotor3(self,parametros):

        return self.consola.do_setangularmotor3(parametros)
    
    def do_setPinza(self,estado):

        return self.consola.do_setpinza(estado)

    def do_Reset(self):

        return self.consola.do_reset()
    

    
    

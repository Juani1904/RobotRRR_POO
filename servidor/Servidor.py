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
        """# Se registra cada funcion que realiza el servicio (robot)
        # Los nombres que pongamos entre "" son con los que voy a tener que llamar a la funcion en mi
        codigo cliente. Pueden diferir estos a como estan referenciados en "sv_robot.py"
        # Luego los nombres do_saludar y do_calcular vienen de los metodos que vamos a definir mas
        abajo, junto con run_server y shutdown
        """ 
       
        self.server.register_function(self.do_turnONPort,"habilitarpuerto")
        self.server.register_function(self.do_turnOFFPort,"deshabilitarpuerto")
        # Se lanza el servidor en un hilo de control mediante Thread

        """*target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called. En este caso el run method
        sera run_server y lo creamos a continuacion de esto"""
        #if (self.consola.do_svstatus()):
        self.thread = Thread(target=self.run_server) #Instanciamos el objeto thead

        self.thread.start() #Utilizamos atributo start() del objeto thread

        print("Servidor RPC iniciado en el puerto [%s]" % str(self.server.server_address))

        

    #Ahora definimos algunos otros metodos que tendra mi clase Servidor

    #Metodo para iniciar el servidor
    def run_server(self):
        
        self.server.serve_forever()

    #Metodo para cerrar el servidor
    def shutdown(self):
        
        self.server.shutdown()
        self.thread.join()

    #Metodo para calcular.
  
    #Metodo para habilitar el puerto serie
   
    def do_turnONPort(self):
         
        return self.consola.do_turnonport()
    
    def do_turnOFFPort(self):
        
        return self.consola.do_turnoffport()


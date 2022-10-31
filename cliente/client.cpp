#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
using namespace std;
#include "XmlRpc.h"
using namespace XmlRpc;

// Definimos subrutina para transformar a mayusculas los comandos
string Mayus(string cadena)
{
    for (int i = 0; i < cadena.length(); i++)
        cadena[i] = toupper(cadena[i]);
    return cadena;
}
// Definimos la subrutina que va a contener todos los comandos del servidor
void comandos(XmlRpcClient Cliente)
{
    XmlRpcValue noArg, result;
    Cliente.execute("getcomandos", noArg, result);
    cout << "Lista de comandos. Seleccione opcion (14) para obtener ayuda sobre la funcion de un comando" << endl;
    cout << "=======================================================" << endl;
    int i = 0;
    for (i = 0; i < result.size(); i++)
    {
        cout << i + 1 << "." << Mayus(result[i]) << endl; // Con Mayus los comandos se entregaran en mayusculas
    }
    // Sumamos los comandos propios del cliente
    cout << i + 1 << ".ESTADOROBOT" << endl;
    cout << i + 2 << ".LISTARCOMANDOS" << endl;
    cout << i + 3 << ".AYUDACOMANDOS" << endl;
    cout << i + 4 << ".EXIT" << endl;
    cout << "=======================================================" << endl;
}

void help(string comando)
{
    if (comando == "modomanual")
    {
        cout << "Modo manual(Aprendizaje): Permite al usuario controlar el robot manualmente y almacenar los comandos en un archivo para posterios replicacion" << endl;
    }
    if (comando == "modoautomatico")
    {
        cout << "Modo automatico(Replicacion): Permite al usuario replicar los comandos almacenados en un archivo de texto" << endl;
    }
    if (comando == "turnonport")
    {
        cout << "TurnOnPort: Enciende el puerto serie del robot" << endl;
    }
    if (comando == "turnoffport")
    {
        cout << "TurnOffPort: Apaga el puerto serie del robot" << endl;
    }
    if (comando == "setmotores")
    {
        cout << "SetMotores: Permite al usuario controlar los motores del robot" << endl;
    }
    if (comando == "setposicionlineal")
    {
        cout << "SetPosicionLineal: Permite al usuario establecer una coordenada para un despl. lineal y la velocidad" << endl;
    }
    if (comando == "setangularmotor1")
    {
        cout << "SetAngularMotor1: Permite al usuario establecer un angulo de despl. para el motor1, su velocidad y sentido" << endl;
    }
    if (comando == "setangularmotor2")
    {
        cout << "SetAngularMotor2: Permite al usuario establecer un angulo de despl. para el motor2, su velocidad y sentido" << endl;
    }
    if (comando == "setangularmotor3")
    {
        cout << "SetAngularMotor3: Permite al usuario establecer un angulo de despl. para el motor3, su velocidad y sentido" << endl;
    }
    if (comando == "setpinza")
    {
        cout << "SetPinza: Permite al usuario habilitar o deshabilitar la pinza del robot" << endl;
    }
    if (comando == "reset")
    {
        cout << "Reset: Permite al usuario llevar al robot a su posicion de reposo/origen (HOMING)" << endl;
    }
    if (comando == "estadorobot")
    {
        cout << "EstadoRobot: Permite al usuario conocer el estado de conexion al robot, servidor y numero de ordenes" << endl;
    }
    if (comando == "listarcomandos")
    {
        cout << "ListarComandos: Permite al usuario conocer la lista de comandos disponibles" << endl;
    }
    if (comando == "exit")
    {
        cout << "Exit: Permite al usuario salir de este CLI cliente" << endl;
    }
}

// Creamos una subrutina para crear un submenu, para no anidar 2 switch
int submenuswitch(int comandnumber)
{
    switch (comandnumber)
    {
    case 1:
        help("modomanual");
        break;
    case 2:
        help("modoautomatico");
        break;
    case 3:
        help("turnonport");
        break;
    case 4:
        help("turnoffport");
        break;
    case 5:
        help("setmotores");
        break;
    case 6:
        help("setposicionlineal");
        break;
    case 7:
        help("setangularmotor1");
        break;
    case 8:
        help("setangularmotor2");
        break;
    case 9:
        help("setangularmotor3");
        break;
    case 10:
        help("setpinza");
        break;
    case 11:
        help("reset");
        break;
    case 12:
        help("estadorobot");
        break;
    case 13:
        help("listarcomandos");
        break;
    case 14:
        help("ayudacomandos");
        break;
    case 15:
        help("exit");
        break;
    }
    return 0;
}

int main()
{
    // Lo primero que hacemos es pedirle al usuario que ingrese la ip y el puerto
    int puerto;
    char ip[10];
    cout << "Ingrese la IP del sv al que desea conectarse.Si es local ingrese localhost: ";
    cin >> ip;
    cout << "Ingrese el puerto al que desea conectarse: ";
    cin >> puerto;

    // Creamos al cliente mediante la clase XmlRpcClient

    XmlRpcClient Cliente(ip, puerto);
    bool flag = true;
    cout << "\n\n######################################################################################################" << endl;
    cout << "                                           Veneris                                                ";
    cout << "######################################################################################################" << endl;
    cout << "Bienvenido a Veneris Client ®. Ingrese el comando o help para obtener una descripcion del uso de los mismos\n\n";
    cout << "\n";
    // Llamamos a la funcion que me printea la lista de comandos
    comandos(Cliente);
    while (flag)
    {
        int opcion;
        cout << "\n";
        cout << "Seleccione el numero de opcion.Seleccione opcion (13) para la lista de comandos: ";
        cin >> opcion;
        // Para que el programa no empiece a loopear si el usuario mete un string, usamos la funcion
        // cin.fail() que devuelve true si el usuario mete un string
        bool flag = true;
        while (flag)
        {
            if (cin.fail())
            {
                cout << "\nOpcion no valida.Seleccione el comando nuevamente\n"
                     << endl;
                cout << "Seleccione el numero de opcion.Seleccione opcion (13) para la lista de comandos: ";
                cin.clear();
                cin.ignore(256, '\n');
                cin >> opcion;
            }
            else
            {
                flag = false;
            }
        }
        cout << "\n";
        switch (opcion)
        {

        case 1:
        {
            // Establecer el modo de funcionamiento
            XmlRpcValue OneArg, result;
            string nombreexterno;
            cout << "Ingrese el nombre del archivo que quiere crear: ";
            cin >> nombreexterno;
            cout << "\n";
            OneArg[0] = nombreexterno;
            Cliente.execute("modomanual", OneArg, result);
            cout << "\n\n"
                 << result << "\n\n";
            for (int i = 0; i < result.size(); i++)
            {
                cout << result[i] << "\n";
            }
        }
        break;
        case 2:
        {
            // Establecer el modo de funcionamiento
            XmlRpcValue OneArg, result;
            string nombreexterno;
            cout << "Ingrese el nombre del archivo que quiere abrir: ";
            cin >> nombreexterno;
            cout << "\n";
            OneArg[0] = nombreexterno;
            Cliente.execute("modoautomatico", OneArg, result);
            cout << "\n\n"
                 << result << "\n\n";
        }
        break;
        case 3:
        {
            XmlRpcValue noArg, result;
            Cliente.execute("turnonport", noArg, result);
            cout << "\n\n"
                 << result << "\n\n";
        }
        break;
        case 4:
        {
            XmlRpcValue noArg, result;
            Cliente.execute("turnoffport", noArg, result);
            cout << "\n\n"
                 << result << "\n\n";
        }
        break;
        case 5:
        {
            string respuesta;
            XmlRpcValue OneArg, result;
            cout << "Ingrese 'on' para activar los motores o 'off' para desactivarlos: ";
            cin >> respuesta;
            OneArg[0] = respuesta;
            Cliente.execute("setmotores", OneArg, result);
            cout << "\n\n"
                 << result << "\n\n";
        }
        break;
        case 6:
        {
            // Establecer el modo de funcionamiento
            XmlRpcValue FourArgs, result;
            int posx, posy, posz, vel;
            cout << "Ingrese coordenada X: ";
            cin >> posx;
            FourArgs[0] = posx;
            cout << "Ingrese coordenada Y: ";
            cin >> posy;
            FourArgs[1] = posy;
            cout << "Ingrese coordenada Z: ";
            cin >> posz;
            FourArgs[2] = posz;
            cout << "Ingrese velocidad: ";
            cin >> vel;
            FourArgs[3] = vel;
            Cliente.execute("setposicionlineal", FourArgs, result);
            cout << "\n\n"
                 << result << "\n\n";
        }
        break;
        case 7:
        {
            // Establecer el modo de funcionamiento
            XmlRpcValue ThreeArgs, result;
            int vel, angulo;
            string sentido;
            cout << "Ingrese Velocidad: ";
            cin >> vel;
            ThreeArgs[0] = vel;
            cout << "Ingrese Sentido: ";
            cin >> sentido;
            ThreeArgs[1] = sentido;
            cout << "Ingrese Angulo: ";
            cin >> angulo;
            ThreeArgs[2] = angulo;
            Cliente.execute("setangularmotor1", ThreeArgs, result);
            cout << "\n\n"
                 << result << "\n\n";
        }
        break;
        case 8:
        {
            // Establecer el modo de funcionamiento
            XmlRpcValue ThreeArgs, result;
            int vel, angulo;
            string sentido;
            cout << "Ingrese Velocidad: ";
            cin >> vel;
            ThreeArgs[0] = vel;
            cout << "Ingrese Sentido: ";
            cin >> sentido;
            ThreeArgs[1] = sentido;
            cout << "Ingrese Angulo: ";
            cin >> angulo;
            ThreeArgs[2] = angulo;
            Cliente.execute("setangularmotor2", ThreeArgs, result);
            cout << "\n\n"
                 << result << "\n\n";
        }
        break;
        case 9:
        {
            // Establecer el modo de funcionamiento
            XmlRpcValue ThreeArgs, result;
            int vel, angulo;
            string sentido;
            cout << "Ingrese Velocidad: ";
            cin >> vel;
            ThreeArgs[0] = vel;
            cout << "Ingrese Sentido: ";
            cin >> sentido;
            ThreeArgs[1] = sentido;
            cout << "Ingrese Angulo: ";
            cin >> angulo;
            ThreeArgs[2] = angulo;
            Cliente.execute("setangularmotor3", ThreeArgs, result);
            cout << "\n\n"
                 << result << "\n\n";
        }
        break;
        case 10:
        {
            string respuesta;
            XmlRpcValue OneArg, result;
            cout << "Ingrese 'on' para activar el gripper o 'off' para desactivarlo: ";
            cin >> respuesta;
            OneArg[0] = respuesta;
            Cliente.execute("setpinza", OneArg, result);
            cout << "\n\n"
                 << result << "\n\n";
        }
        break;
        case 11:
        {
            XmlRpcValue noArg, result;
            Cliente.execute("reset", noArg, result);
            cout << "\n\n"
                 << result << "\n\n";
        }
        break;
        case 12:
        {
            // Aca hay que hacer algo para que me diga si el servidor esta conectado o no
            // Aca hay que hacer algo para saber si el puerto serie esta conectado o no
            // Para obtener el numero de operaciones solicitadas
            XmlRpcValue noArg3, result3;
            Cliente.execute("getestadopuertoserie", noArg3, result3);
            cout << "El estado del puerto serie es: " << result3 << "\n\n";
            XmlRpcValue noArg1, result1;
            Cliente.execute("getnumordenes", noArg1, result1);
            cout << "El numero de ordenes solicitadas hasta el momento es: " << result1 << "\n\n";
            // Ahora vamos a mostrar las ordenes ejecutadas
            cout << "Los comandos o ordenes solicitadas fueron: " << endl;
            XmlRpcValue noArg2, result2;
            Cliente.execute("getlistaordenes", noArg2, result2);
            cout << "\n\n";
            for (int i = 0; i < result2.size(); i++)
            {
                cout << result2[i] << "\n\n";
            }
            
        }
        break;
        case 13:
        {
            comandos(Cliente);
        }
        break;
        case 14:
        {
            int comandnumber;
            cout << "\n"
                 << "Escriba el numero de opcion con la que necesita ayuda: ";
            cin >> comandnumber;
            cout << "\n";
            submenuswitch(comandnumber);
        }
        break;
        case 15:
        {
            cout << "Saliendo..." << endl;
            // Cerramos el archivo creado en el modo manual
            XmlRpcValue noArg, result;
            Cliente.execute("cerrararchivoexterno", noArg, result);
            flag = false;
        }
        break;
        default:
            cout << "Opcion no valida.Seleccione el comando nuevamente" << endl;
            break;
        }
    }
    /*Llamamos a la funcion saludar1 del servidor, para ello vamos a utilizar la clase XmlRpcValue
    para establecer los argumentos que vamos a enviar. Luego con el metodo exectute que pertenece
    a la clase XmlRpcClient mandamos al sv la peticion */
}

#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
using namespace std;
#include "XmlRpc.h"
using namespace XmlRpc;


int main(){
    //Lo primero que hacemos es pedirle al usuario que ingrese la ip y el puerto
    int puerto;
    char ip[10];
    cout<<"Ingrese la IP del sv al que desea conectarse.Si es local ingrese localhost: ";
    cin>>ip;
    cout<<"Ingrese el puerto al que desea conectarse: ";
    cin>>puerto;

    //Creamos al cliente mediante la clase XmlRpcClient

    XmlRpcClient Cliente(ip,puerto);
    bool flag=true;
    cout<<"\n\n######################################################################################################"<<endl;
    cout<<"                                           Veneris                                                "<<endl;
    cout<<"######################################################################################################"<<endl;
    cout<<"Bienvenido a Veneris Client ®. Ingrese el comando o help para obtener una descripcion del uso de los mismos\n\n";
    while(flag) {
        int opcion;
        cout<<"\n";
        cout<<"1.Habilitar puerto serie"<<endl;
        cout<<"2.Deshabilitar puerto serie"<<endl;
        cout<<"3.Activar/Desactivar motores robot"<<endl;
        cout<<"4.Exit"<<endl;
        cout<<"\n";
        cout<<"Seleccion: ";
        cin>>opcion;
        cout<<"\n";
        switch(opcion)
        {
            case 1: {
                XmlRpcValue noArg,result;
                Cliente.execute("habilitarpuerto",noArg,result);
                cout<<result<<"\n\n";
                    }
            break;
            case 2: {
                XmlRpcValue noArg,result;
                Cliente.execute("deshabilitarpuerto",noArg,result);
                cout<<result<<"\n\n";
                    }
            break;
            case 3: {
                string respuesta;
                XmlRpcValue OneArg,result;
                cout<<"Ingrese 'on' para activar los motores o 'off' para desactivarlos: ";
                cin>>respuesta;
                OneArg[0]=respuesta;
                Cliente.execute("setmotores",OneArg,result);
                cout<<result<<"\n\n";
                    }
            break;
            default: flag=false; break;
            
        }
        
        

    }
    /*Llamamos a la funcion saludar1 del servidor, para ello vamos a utilizar la clase XmlRpcValue
    para establecer los argumentos que vamos a enviar. Luego con el metodo exectute que pertenece
    a la clase XmlRpcClient mandamos al sv la peticion */
    

    

/*
    XmlRpcValue coord,result2;
   coord[0]=1;
   coord[1]=2;
   coord[2]=3;
   coord[3]=10;
    Cliente.execute("posicion",coord,result2);
    cout<<result2<<"\n\n";
*/
    
    


    //Creamos

}
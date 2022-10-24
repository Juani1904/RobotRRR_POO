#include <iostream>
#include <stdlib.h>
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

    /*Llamamos a la funcion saludar1 del servidor, para ello vamos a utilizar la clase XmlRpcValue
    para establecer los argumentos que vamos a enviar. Luego con el metodo exectute que pertenece
    a la clase XmlRpcClient mandamos al sv la peticion */
    XmlRpcValue noArg,result1;
    Cliente.execute("habilitarpuerto",noArg,result1);
    cout<<result1<<"\n\n";

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
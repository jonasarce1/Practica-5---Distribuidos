import Pyro4
import datetime
import random
from dateutil import parser
from timeit import default_timer as timer
import time
import os
import logging

class ClientRMI:
    def __init__(self):
        self.ServerRMI = Pyro4.Proxy("PYRONAME:ServerRMI")
    
    def CristianAlgorithm(self):
        #Se obtiene la hora actual del cliente
        clientTimeSend = datetime.datetime.now().time()
        serverTime = self.ServerRMI.GetServerTime()
        clientTimeReceive = datetime.datetime.now().time()

        #Se llama al método CristianAlgorithm en el servidor y se pasa el tiempo del cliente como argumento
        result = self.ServerRMI.CristianAlgorithm(clientTimeSend, clientTimeReceive, serverTime)

        print("\n" + result)
        

client = ClientRMI()

while True:
    print("Escriba 1 para acceder a la calculadora")
    print("Escriba 3 para sincronizar relojes con algoritmo de Cristian")
    print("Escriba cualquier otra cosa para salir")
    option = input()
    if option == "1":
        print()
        print("Escriba 1 para sumar")
        print("Escriba 2 para restar")
        print("Escriba 3 para multiplicar")
        print("Escriba 4 para dividir")
        print("Escriba 5 para calcular la potencia")
        print("Escriba 6 para calcular la raiz cuadrada")
        
        operation = input()
        print()
        #Si la operacion es un numero del 1 al 4
        if operation == "1" or operation == "2" or operation == "3" or operation == "4":
            print("Escriba el primer operando")
            num1 = input()
            print("Escriba el segundo operando")
            num2 = input()
            print()
            if operation == "1":
                print("El resultado de la suma de " + num1 + " y " + num2 + " es: " + client.ServerRMI.Sumar(float(num1), float(num2)))
            elif operation == "2":
                print("El resultado de la resta de " + num1 + " y " + num2 + " es: " + client.ServerRMI.Restar(float(num1), float(num2)))
            elif operation == "3":
                print("El resultado de la multiplicacion de " + num1 + " y " + num2 + " es: " + client.ServerRMI.Multiplicar(float(num1), float(num2)))
            elif operation == "4":
                print("El resultado de la division de " + num1 + " y " + num2 + " es: " + client.ServerRMI.Dividir(float(num1), float(num2)))
        #Si la operacion es potencia
        elif operation == "5":
            print("Escriba la base")
            num1 = input()
            print("Escriba el exponente")
            num2 = input()
            print("El resultado de elevar " + num1 + " a la " + num2 + " es: " + client.ServerRMI.Potencia(float(num1), float(num2)))
        #Si la operacion es raiz
        elif operation == "6":
            print("Escriba el numero")
            num1 = input()
            print("La raiz cuadrada de " + num1 + " es: " + client.ServerRMI.RaizCuadrada(float(num1)))
        else:
            print("Operacion no valida")
            
        print()
    
    elif option == "3":
        client.CristianAlgorithm()
        print("\nAlgoritmo de Cristian finalizado\n")
    else:
        break
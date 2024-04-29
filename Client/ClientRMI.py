import Pyro4
import datetime
import random
from dateutil import parser
from timeit import default_timer as timer
import time
import os
import logging

#Usare la biblioteca Pyro4 (Python Remote Objects) para crear un cliente RMI

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

        #Se imprime el resultado devuelto por el servidor
        print("\n" + result)
        

client = ClientRMI()

while True:
    print("Escriba 1 para acceder a la calculadora")
    print("Escriba 3 para sincronizar relojes con algoritmo de Cristian")
    print("Escriba cualquier otra cosa para salir")
    option = input()
    if option == "1":
        print("hola")
    elif option == "3":
        client.CristianAlgorithm()
        print("\nAlgoritmo de Cristian finalizado\n")
    else:
        break
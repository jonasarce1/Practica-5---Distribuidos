import Pyro4
import random
import os
import datetime
from dateutil import parser
from timeit import default_timer as timer
import logging
import math

#Usare la biblioteca Pyro4 (Python Remote Objects) para crear un servidor RMI
#Y hare la posibilidad de sincronizar relojes entre servidor y cliente mediante algoritmo cristian y berkeley

@Pyro4.expose #Expose para exponer los metodos y poder ser llamados por los clientes
class ServerRMI(object):
    ######### Metodos para la calculadora #########
    
    def Sumar(self, num1, num2):
        return str(num1 + num2)
    
    def Restar(self, num1, num2):
        return str(num1 - num2)
    
    def Multiplicar(self, num1, num2):
        return str(num1 * num2)
    
    def Dividir(self, num1, num2):
        return str(num1 / num2)
    
    def Potencia(self, num1, num2):
        return str(math.pow(num1, num2))
    
    def RaizCuadrada(self, num1):
        return str(math.sqrt(num1))
    
    ######### Metodos para la Fibonacci #########
    
    def Fibonacci(self, n): #Metodo recursivo para calcular el n-esimo termino de la secuencia de Fibonacci
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.Fibonacci(n-1) + self.Fibonacci(n-2)
        
    ######### Metodos para el algoritmo de Cristian #########
    
    def GetServerTime(self):
        return datetime.datetime.now().time()
   
    def CristianAlgorithm(self, clientTimeSend, clientTimeReceive, serverTime):
        #Se configura el logging
        #Se obtiene el directorio actual
        current_directory = os.path.dirname(os.path.abspath(__file__))

        #Se obtiene el directorio superior
        parent_directory = os.path.dirname(current_directory)

        #Se crea la carpeta de logs
        log_folder = "logs"

        #Se crea la ruta de la carpeta de logs
        log_path = os.path.join(parent_directory, log_folder)

        #Se crea la carpeta de logs si no existe
        os.makedirs(log_path, exist_ok=True)
        
        #Se crea el archivo cristian.log
        log_file = log_path + "/cristian.log"
        
        #Se termina de configurar el logging
        logging.basicConfig(filename=log_file, level=logging.INFO)
        
        #Se guarda la hora actual
        actualTime = datetime.datetime.now()
        
        #Se guarda en el log la hora en la que el cliente envio mensaje al servidor
        logging.info("Hora del cliente (Envio de mensaje): " + clientTimeSend)
        
        #Se guarda en el log la hora del servidor
        logging.info("Hora del servidor: " + serverTime)
        
        #Se guarda en el log la hora en la que el cliente recibio mensaje del servidor
        logging.info("Hora del cliente (Recepcion de mensaje): " + clientTimeReceive)
        
        clientTimeSendObj = parser.parse(clientTimeSend)
        clientTimeReceiveObj = parser.parse(clientTimeReceive)
        serverTimeObj = parser.parse(serverTime)
        
        #Se calcula la latencia
        latency = (clientTimeReceiveObj - clientTimeSendObj).total_seconds()
        latencyDelta = datetime.timedelta(seconds=latency)
        logging.info("Latencia: " + str(latencyDelta))
        
        #Se calcula el tiempo sincronizado para el cliente
        syncTime = serverTimeObj + (latencyDelta / 2)
        logging.info("Hora sincronizada: " + syncTime.strftime('%H:%M:%S.%f'))
        
        #Se calcula el error de sincronizacion (diferencia entre el tiempo actual y el tiempo sincronizado)
        syncError = actualTime - syncTime
        if syncError.total_seconds() < 0: #Si el error sale negativo se convierte a positivo
            syncError = -syncError
            
        logging.info("Error de sincronizacion: " + str(syncError))
        
        logging.info("-------------------------------------------------")

        #Si el cliente va atrasado (hora del servidor mayor que la hora del cliente cuando recibio el mensaje del servidor)
        if(serverTime > clientTimeReceive):
            return "El cliente va atrasado, su hora ha de sincronizarse con la del servidor"
        else:
            return "El cliente va adelantado, ha de esperar a la hora del servidor"

    
daemon = Pyro4.Daemon() #Pyro daemon es el servidor que escucha las peticiones de los clientes
nameServer = Pyro4.locateNS() #Localiza el servidor de nombres
uri = daemon.register(ServerRMI) #Registra la clase ServerRMI en el servidor
nameServer.register("ServerRMI", uri) #Registra la clase ServerRMI en el servidor de nombres

print("Server RMI ready.")
daemon.requestLoop() #Entra en el bucle de espera para las peticiones de los clientes
              
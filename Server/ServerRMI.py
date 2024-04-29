import Pyro4
import random
import os
import datetime
from dateutil import parser
from timeit import default_timer as timer
import logging
import math
from cryptography.fernet import Fernet

#Usare la biblioteca Pyro4 (Python Remote Objects) para crear un servidor RMI
#Y hare la posibilidad de sincronizar relojes entre servidor y cliente mediante algoritmo cristian y berkeley

@Pyro4.expose #Expose para exponer los metodos y poder ser llamados por los clientes
class ServerRMI(object):
    
    #Funcion para configurar el logging en la carpeta logs
    def CreateLogDirectory(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        log_folder = "logs"
        log_path = os.path.join(parent_directory, log_folder)
        os.makedirs(log_path, exist_ok=True)
        return log_path
    
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
        
    ######### Metodos para encriptacion de mensajes (AES) #########
    
    def GenerateKey(self):
        log_path = self.CreateLogDirectory()
        log_file = log_path + "/keys.log"
        logging.basicConfig(filename=log_file, level=logging.INFO)
        
        key = Fernet.generate_key()
        
        #Si la llave generada ya esta en el log de keys genero otra llave
        while key in logging.Logger.manager.loggerDict:
            key = Fernet.generate_key()
        
        key_str = key.decode()
        
        #Guardo la llave en el log de keys
        logging.info(key_str)
        
        return str(key_str)
    
    def EncryptMessage(self, message, key):
        #Configuro el logging para guardar los mensajes encriptados
        log_path = self.CreateLogDirectory()
        log_file_keys = log_path + "/keys.log"
        
        #Compruebo si la clave ya esta en el log de keys si no esta indico error
        
        with open(log_file_keys, "r") as file:
            lines = file.readlines()
            for line in lines:
                if key in line:
                    break
            else:
                return "Error: la clave no es valida, no se encuentra en el log de keys"
        
        f = Fernet(key)
        encryptedMessage = f.encrypt(message.encode()).decode() #Hay que "decodificar" (que no sea diccionario) el mensaje encriptado para que sea legible
        
        #Guardo el mensaje encriptado en el log
        log_path = self.CreateLogDirectory()
        log_file_encrypted = log_path + "/encryptedMessages.log"
        
        #para asegurar que se escriebe en el archivo encryptedMessages.log y no en keys.log se abre el archivo en modo append
        with open(log_file_encrypted, "a") as file:
            file.write(encryptedMessage + "\n")
        
        return encryptedMessage
    
    def DecryptMessage(self, encryptedMessage, key):
        #Paso la llave y el mensaje encriptado a bytes
        key = key.encode()
        encryptedMessage = encryptedMessage.encode()
        
        f = Fernet(key)

        try:
            decryptedMessage = f.decrypt(encryptedMessage).decode()
            
            return decryptedMessage
        except Exception as e:
            raise Exception("Error: No se puede desencriptar el mensaje, mensaje o clave incorrectos + " + str(e))
        
    ######### Metodos para el algoritmo de Cristian #########
    
    def GetServerTime(self):
        return datetime.datetime.now().time()
   
    def CristianAlgorithm(self, clientTimeSend, clientTimeReceive, serverTime):
        #Se configura el logging
        log_path = self.CreateLogDirectory()
        log_file = log_path + "/cristian.log"
        
        #Se termina de configurar el logging, si no existe el archivo se crea
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
              
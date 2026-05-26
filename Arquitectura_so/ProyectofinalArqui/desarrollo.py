import threading 
import time
import random 
import os

capacidad = 10 # inicializamos la variable que indica el numero de parqueaderos disponibles

# creo semaforo para capacidad que permite sincronizar acceso a los recursos (parqueaderos)
semaforo = threading.Semaphore(capacidad) 

lock_ocupados = threading.Lock()
lock_estados = threading.Lock()

ocupados = 0 #variable que indica cuantos paqueaderos estan ocupados
estados = {} #inicializa un diccionario vacio para almacenar el estado de cada parqueadero (nuevo,esperando,estacionado,saliendo e inactivo)


ruta_logs = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),#obtiene la ruta del directorio actual del archivo desarrollo.py
    "logs_de_eventos.csv")


simu_evento = threading.Event()#se crea evento para controlar los hilos, inicio y fin.es el INTERRUPTOR global del sistema
simu_evento.set() #se inicia en estado "set" para permitir que los hilos comiencen a ejecutarse

simulacion_activa = True #variable global para controlar el estado de la simulacion, se utiliza para permitir que los hilos sepan si la simulacion esta activa o no, esto es util para pausar y reanudar la simulacion de manera inteligente

def ingreso_vehiculo_manual(placa):
    #verifica que la simulacion este activa antes
    #de crear un hilo nuevo para el vehiculo ingresado
    if not simulacion_activa:
        return
    #placa tiene , porque es una tupla
    hilo_placa = threading.Thread(target=vehiculo, args=(placa,))
    hilo_placa.start()

#funcion que permite pausar la simulacion de manera inteligente, es decir, 
#si el evento esta en estado "clear" (pausado) el hilo se bloquea en la linea simu_evento.wait() hasta que el evento vuelva a estar en estado "set" (reanudar)
#espera X segundos,
#pero revisando constantemente
#si el simulador está pausado
def pausa_inteligente(segundos):
    inicio = time.time()#devuelve el tiempo actual en segundos que ha pasado desde el inicio de la pausa
    while time.time() - inicio < segundos and simulacion_activa:#mientras el tiempo transcurrido desde el inicio de la pausa sea menor que los segundos especificados, el hilo sigue en pausa
        simu_evento.wait()# si está pausado, se bloquea aquí ¿la simulacion esta activa? si, sigue esperando, si no, se reanuda y sigue contando el tiempo de la pausa
        time.sleep(0.1)

def detener_simulacion():#funcion para detener la simulacion, se llama desde la interfaz grafica para detener la simulacion,
     #esta funcion cambia el estado de la variable global simulacion_activa a False, y pone el evento en estado "set" para permitir
     #que los hilos se reanuden y terminen su ejecucion
    global simulacion_activa
    simulacion_activa = False
    simu_evento.set()#desbloquea hilos pausados

def reiniciar():#funcion para reiniciar la simulacion, se llama desde la interfaz grafica para reiniciar la simulacion, esta funcion reinicia el estado de la variable global simulacion_activa a True, y pone el evento en estado "set" para permitir que los hilos se reanuden y terminen ejecucion
    global ocupados, estados, simulacion_activa, semaforo
    #se detiene simulacion actual
    simulacion_activa = False
     #desbloquear hilos pausados
    simu_evento.set()
    #se da un tiempo pequeño para que terminen
    time.sleep(2)
    #se reinicia variables globales
    ocupados = 0
    estados = {}
    
    #se crea un semaforo nuevo para reiniciar la capacidad, esto es necesario porque el semaforo no tiene un metodo para reiniciar su contador, por lo que se crea un nuevo semaforo con la capacidad inicial
    semaforo = threading.Semaphore(capacidad)
    simulacion_activa = True
    print("...Simulacion reiniciada...")

#se crea una funcion que toma el lock, lee el valor actual y lo devuelve 
#se vincula en la funcion mostrar_info
def obtener_ocupados():
    with lock_ocupados:
        return ocupados  
    
#devuelve una copia del diccionario de estados para evitar condicion de carrera
def obtener_estados():
    with lock_estados:
        return estados.copy() 
    
def registro_eventos(vehiculo_id):
        with open(ruta_logs, "a", encoding="utf-8") as carrito_log: #abre el archivo de logs en modo append para agregar nuevos eventos
            carrito_log.write(f"{time.time()},{vehiculo_id},{estados[vehiculo_id]},{ocupados}\n")


def vehiculo(vehiculo_id):#uso esta funcion para cambiar ESTADOS y contador de OCUPADOS, que son los recursos compartidos
#va a escribir en el archivo de logs cada vez que haya un evento
    global ocupados
    simu_evento.wait()
    #estado INICIAL 
    with lock_estados:
        estados[vehiculo_id] = "NUEVO" #actualiza el estado del vehiculo a nuevo
        registro_eventos(vehiculo_id)
        print (f"Vehiculo {vehiculo_id}:NUEVO")
        
    pausa_inteligente(random.uniform(1, 3)) #simula el tiempo que tarda el vehiculo en llegar al parqueadero
    if not simulacion_activa: #si la simulacion no esta activa, el hilo se reanuda
        return #si la simulacion no esta activa, el hilo se reanuda y termina su ejecucion,
            #esto es importante para evitar que los hilos queden bloqueados en espera de eventos cuando la simulacion ha sido detenida o reiniciada
    
    #estado ENTRANDO
    with lock_estados:
        estados[vehiculo_id] = "ESPERANDO" #actualiza el estado del vehiculo a ESPERANDO
        registro_eventos(vehiculo_id)
        print (f"Vehiculo {vehiculo_id}:ESPERANDO")
    
    simu_evento.wait() #espera a que el evento este en estado "set" para continuar, si el evento esta "clear" el hilo se bloquea aquí hasta que el evento vuelva a estar "set"
    
    #epara entrar al parqueadero,el semaforo verifica si hay espacio,sino, el hilo se bloquea aquí hasta que haya un espacio disponible
    semaforo.acquire() 

    with lock_ocupados:
        ocupados += 1  
        #aunmenta el contador y registra que un espacio esta lleno

    with lock_estados:
        estados[vehiculo_id] = "ESTACIONADO" #actualiza el estado del vehiculo a ESTACIONADO
        registro_eventos(vehiculo_id)
        print (f"Vehiculo {vehiculo_id}:ESTACIONADO (parqueaderos ocupados = {ocupados})")
   
    #simula el tiempo que tarda el vehiculo estacionado, en los rangos de 2 a 10 segundos
    pausa_inteligente(random.uniform(3, 10)) 
    if not simulacion_activa: #si la simulacion no esta activa, el hilo se reanuda
        return
    

    simu_evento.wait()
    if not simulacion_activa: #si la simulacion no esta activa, el hilo se reanuda
        return
    #disminuye el contador y registra que un espacio esta libre 
    with lock_ocupados:
        ocupados -= 1

    with lock_estados:
        estados[vehiculo_id] = "SALIENDO" #actualiza el estado del vehiculo a SALIENDO
        registro_eventos(vehiculo_id)
        print (f"Vehiculo {vehiculo_id}:SALIENDO (parqueaderos ocupados = {ocupados})")
    
    pausa_inteligente(2)#simula el tiempo que tarda el vehiculo en salir 
    simu_evento.wait()
    #libera el semaforo para salir del parqueadero, permitiendo que otro vehiculo pueda entrar
    semaforo.release()

    with lock_estados:
        estados[vehiculo_id] = "INACTIVO"
        registro_eventos(vehiculo_id)
        print (f"Vehiculo {vehiculo_id}:INACTIVO (parqueaderos ocupados = {ocupados})")


# se crea funcion principal que maneja la simulacion, crea hilos para cada vehiculo, y espera a que terminen su ejecucion 
# para finalizar la simulacion, esta funcion se llama desde la interfaz grafica para iniciar la simulacion
def inicio_simulacion():
    carritos = [] #lista vacia que guarda los hilos 

    with open(ruta_logs, "w", encoding="utf-8") as carrito_log: #se crea un archivo csv para guardar los logs de eventos
            carrito_log.write("tiempo,vehiculo_id,estado,ocupados\n") #escribe la cabecera del archivo csv
           
    for i in range(1,31):
        if not simulacion_activa: #si la simulacion no esta activa, se corta proceso y reanuda
            break
        carrito = threading.Thread(target=vehiculo,args=(i,)) #se crean 30 hilos para simular 30 vehiculos
        carritos.append(carrito) #se agrega cada hilo a la lista de carritos
        carrito.start() #se inicia cada hilo
        #espera un tiempo aleatorio corto para llegada
        time.sleep(random.uniform(0.5, 2)) 

    for carrito in carritos:
        carrito.join() #espera a que todos los hilos terminen su ejecucion para finalizar la simulacion

    print("Simulacion finalizada")

if __name__ == "__main__": #marca punto de arranque del programa, se llama a la funcion principal para iniciar la simulacion
    inicio_simulacion()

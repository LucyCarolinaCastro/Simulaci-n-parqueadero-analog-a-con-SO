import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from desarrollo import (
    inicio_simulacion,
    simu_evento,
    reiniciar as reiniciar_simulacion)
import threading
import desarrollo

hilo_simulacion = None#variable global para almacenar el hilo de la simulacion, esto es necesario para poder reiniciar la simulacion de manera correcta, ya que al reiniciar se crea un nuevo hilo para la simulacion, y el hilo anterior debe ser detenido para evitar que queden hilos bloqueados en espera de eventos cuando la simulacion ha sido detenida o reiniciada

def iniciar():
    global hilo_simulacion
    #se llama a la funcion desde otra funcion conectora para dar inicio a la simulacion
    simu_evento.set() 

    hilo_simulacion = threading.Thread(target=inicio_simulacion) #se crea un nuevo hilo para ejecutar la funcion de inicio de la simulacion, esto permite que la interfaz grafica siga siendo responsiva mientras se ejecuta la simulacion
    hilo_simulacion.start() #se inicia el hilo de la simulacion

def pausarReanudar():#se crea funcion para pausar y reanudar la simulacion, esta funcion se conecta al boton de pausar/reanudar en la interfaz grafica
    if simu_evento.is_set():
        simu_evento.clear() #pausa la simulacion, y cambia boton a reanudar
        boton_pausa.config(text="reanudar Simulación")
    else:
        simu_evento.set() #reanuda la simulacion,y cambia boton a pausar
        boton_pausa.config(text="pausar Simulación")

def reiniciar():
    #esta funcion se conecta al boton de reiniciar en la interfaz grafica, y reinicia la simulacion, esto se logra reiniciando el evento y llamando a la funcion de inicio de la simulacion
    global hilo_simulacion
    reiniciar_simulacion() #se llama a la funcion de reinicio de la simulacion, esta funcion se encarga de reiniciar las variables globales y llamar a la funcion de inicio de la simulacion, esto es necesario para evitar que queden hilos bloqueados en espera de eventos cuando la simulacion ha sido detenida o reiniciada
    
    hilo_simulacion = threading.Thread(target=inicio_simulacion) #se crea un nuevo hilo para ejecutar la funcion de reinicio de la simulacion, esto permite que la interfaz grafica siga siendo responsiva mientras se ejecuta el reinicio de la simulacion
    hilo_simulacion.start() #se inicia el hilo de reinicio de la simulacion

mostrar_alerta = False#evita que hayan muchas de ventanas emergentes

def mostrar_info():
    global mostrar_alerta
    ocupados = desarrollo.obtener_ocupados()
    #actualiza el texto del label que muestra numero de ocupados
    busy.config(text=f"parqueaderos ocupados: {ocupados}")
    disponibles.config(text=f"parqueaderos disponibles: {desarrollo.capacidad - ocupados}")
    if ocupados == desarrollo.capacidad and not mostrar_alerta:
        simu_evento.clear()#pausa la simulacion 
        busy.config(fg="red")#cambia el color del texto a rojo para resaltar que el parqueadero esta lleno
        messagebox.showwarning("PARQUEADERO LLENO", "no hay espacios disponibles.")
        simu_evento.set()#reanuda la simulacion despues de cerrar la ventana emergente
        mostrar_alerta = True
    else:
        busy.config(fg="black")#cambia el color del texto a negro
    if ocupados < desarrollo.capacidad:
        mostrar_alerta = False
    #programa la funcion para que se ejecute cada 200 ms,
    #esto permite que la informacion se actualice constantemente en la interfaz grafica
    ventana.after(200, mostrar_info)
    
    
def actualizar_tabla():
    #se limpia la tabla, get_childen devuelve los items de la tabla,
    #se elimina con delete cada iten de la tabla
    tabla.delete(*tabla.get_children())#se evitan registros duplicados
    estados_actuales = desarrollo.obtener_estados()
    #itera sobre el diccionario de estados
    for vehiculo_id, estado in estados_actuales.items():
       if estado != "INACTIVO":
           tabla.insert("", tk.END, values=(vehiculo_id, estado))#inserta una nueva fila en la tabla con el id del vehiculo y su estado actual
    #programa la funcion para que se ejecute cada 50 ms    
    ventana.after(50, actualizar_tabla) 

def agregar_vehiculo():
    placa = entrada_placa.get().strip()
    if placa == "":#verifica si el campo esta vacio
        messagebox.showerror("Error", "Por favor ingrese una placa válida.")
        return
    desarrollo.ingreso_vehiculo_manual(placa)#llama a la funcion, evia la nueva placa y crea el hilo
    entrada_placa.delete(0, tk.END)#limpia la caja de texto despues de agregar el vehiculo

ventana = tk.Tk()
ventana.title("PARQUEADERO LAS MARGARITAS")
ventana.geometry("400x600")#Da el tamaño a la ventana


#se muestra la ventana con un mensaje de bienvenida
mensaje_bienvenida = tk.Label(ventana, text="Bienvenido al Parqueadero Las Margaritas", font=("Arial", 14))
mensaje_bienvenida.pack(pady=20)#pady es un parametro que agrega espacio vertical entre los elementos


#se crean labels para mostrar informacion actual 
busy = tk.Label(ventana, text="parqueaderos ocupados: 0", font=("Arial", 12))
busy.pack(pady=7)

disponibles = tk.Label(ventana, text=f"parqueaderos disponibles: {desarrollo.capacidad}", font=("Arial", 12))
disponibles.pack(pady=7)


#se crea un frame para contener TABLA de estados y id_vehiculo
frame_tabla = ttk.Frame(ventana)
frame_tabla.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)#se crea un margen para que no toque los bordes
#se crea una tabla para mostrar los eventos de los vehiculos 
columnas =("Placa vehiculo", "Estado")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
#se definden los encabezados de la tabla
tabla.heading("Placa vehiculo", text="Placa vehiculo")
tabla.heading("Estado", text="Estado")
#se crea una barra de scroll
barra = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla.yview)
tabla.configure(yscrollcommand=barra.set)

tabla.pack(side=tk.LEFT, fill=tk.BOTH,expand=True) 
barra.pack(side=tk.RIGHT, fill=tk.Y)#se hace que la tabla se expanda para llenar el espacio disponible en el frame, y se ajuste al tamaño del frame

#se crean los botones para iniciar y pausar la simulacion, cada uno conectado a su respectiva funcion
boton = tk.Button(ventana, text="Iniciar Simulación", command=iniciar)
boton.pack(pady=10)

boton_pausa = tk.Button(ventana, text="Pausar Simulación", command=pausarReanudar)
boton_pausa.pack(pady=10)

boton_reiniciar = tk.Button(ventana, text="Reiniciar Simulación", command=reiniciar)
boton_reiniciar.pack(pady=10)

#se crea una caja de texto para ingresar la placa
entrada_placa = tk.Entry(ventana, font=("Arial", 8))
entrada_placa.pack(pady=5)
entrada_placa.insert(0, "Ingrese placa del vehiculo")#valor inicial 0 y texto que muestra por defecto
#se crea boton para ingresar una nueva placa de vehiculo
boton_agregar = tk.Button(ventana, text="Agregar Vehiculo", command=agregar_vehiculo)
boton_agregar.pack(pady=10)

#llamo a la funcion para mostrar la info actual
mostrar_info() 
#llamo a la funcion que actualiza los datos en la tabla
actualizar_tabla()
#hace aparecer la venana
ventana.mainloop()
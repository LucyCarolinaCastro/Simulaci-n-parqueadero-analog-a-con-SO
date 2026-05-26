# 🚗 PARQUEADERO LAS MARGARITAS

Simulador de parqueadero desarrollado en **Python** utilizando **concurrencia con hilos (threads)**, **semáforos**, **locks** y **eventos**, realizando una analogía con el funcionamiento interno de un **Sistema Operativo**.

---

## Descripción del proyecto

**Parqueadero Las Margaritas** es un simulador concurrente donde múltiples vehículos ingresan, esperan, se estacionan y salen de un parqueadero con capacidad limitada.

El proyecto implementa conceptos fundamentales de **Arquitectura de Computadores y Sistemas Operativos**, simulando el manejo de procesos, sincronización y acceso controlado a recursos compartidos.

Cada vehículo se ejecuta como un **hilo independiente**, permitiendo representar un entorno concurrente similar al comportamiento de procesos en un sistema operativo real.

---

## ⚙️ Tecnologías utilizadas

- **Python 3**
- **threading**
- **Tkinter (GUI)**
- **CSV para registro de logs**

---

## Conceptos de Sistemas Operativos implementados

### 🔹 Threads (Hilos)
Cada vehículo se ejecuta como un hilo independiente:

```python
threading.Thread(target=vehiculo, args=(i,))
```

Simulando múltiples procesos concurrentes.

### 🔹 Semáforos (Semaphore)
Controlan el acceso al recurso compartido:

```python
threading.Semaphore(capacidad)
```

Garantizando que nunca ingresen más vehículos que la capacidad permitida.

### 🔹 Locks (Lock)
Protegen las secciones críticas del sistema:

- contador de parqueaderos ocupados
- diccionario de estados

Evitan condiciones de carrera y acceso simultáneo incorrecto.

### 🔹 Eventos (Event)
Funcionan como el **interruptor global del sistema**:

- iniciar simulación
- pausar
- reanudar
- detener procesos

---

## 🖥️ Interfaz gráfica

El simulador cuenta con una interfaz desarrollada con **Tkinter** que permite:

✅ Iniciar simulación

✅ Pausar / Reanudar

✅ Reiniciar sistema

✅ Visualizar parqueaderos ocupados y disponibles en tiempo real

✅ Ver estados actuales de los vehículos mediante tabla dinámica

✅ Mostrar alertas cuando el parqueadero alcanza capacidad máxima

---

## 🚦 Estados de los vehículos

Cada vehículo atraviesa diferentes estados durante la simulación:

| Estado | Analogía SO |
|--------|-------------|
| NUEVO | New |
| ESPERANDO | Waiting / Blocked |
| ESTACIONADO | Running |
| SALIENDO | Finalización de proceso |
| INACTIVO | Terminated |

---

## 📄 Sistema de logs

Todos los eventos generados por el simulador se almacenan automáticamente en un archivo CSV.

Cada registro contiene:

- tiempo
- ID del vehículo
- estado
- ocupación actual

Esto permite mantener un historial completo de ejecución del sistema.

---

## 🔄 Analogía con Sistemas Operativos

| Simulador | Sistema Operativo |
|-----------|------------------|
| Vehículos | Procesos |
| Parqueaderos | Recursos compartidos |
| Semáforo | Control de acceso |
| Locks | Protección de sección crítica |
| Evento global | Scheduler / control de ejecución |
| Reiniciar simulación | Reboot del sistema |
| Logs CSV | Historial del sistema |

---

## ▶️ Ejecución del proyecto

Clona el repositorio:

```bash
git clone <tu-url-del-repositorio>
```

Ingresa a la carpeta:

```bash
cd Parqueadero-Las-Margaritas
```

Ejecuta:

```bash
python GUI.py
```

---


## 👩‍💻 Autor

Proyecto desarrollado por **Lucy Carolian Castro Rojas **  
**Arquitectura de Computadores y Sistemas Operativos**

---
⭐ Proyecto académico enfocado en concurrencia, sincronización y analogía con Sistemas Operativos.

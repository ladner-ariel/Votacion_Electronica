import customtkinter as ctk
import time
import threading

class Lista:
    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color
        self.votos = 0

    def votar(self):
        self.votos += 1

    def __str__(self):
        return f"Lista {self.nombre} (Color: {self.color}, Votos: {self.votos})"

class SistemaVotacion:
    def __init__(self):
        self.listas = []

    def agregar_lista(self, lista):
        self.listas.append(lista)

    def votar(self, nombre_lista):
        """Permite votar por una lista específica, con un retraso."""
        lista = next((l for l in self.listas if l.nombre == nombre_lista), None)
        if lista:
            # Pausar la ejecución por 5 segundos
            time.sleep(5)
            lista.votar()
            return f"¡Votaste por la {nombre_lista}!"
        else:
            return f"La lista {nombre_lista} no existe."

    def obtener_resultados(self):
        """Devuelve los resultados como un string."""
        resultados = "Resultados de la votación:\n"
        for lista in self.listas:
            resultados += f"{lista}\n"
        return resultados

# Crear la interfaz con CustomTkinter
class VotacionApp(ctk.CTk):
    def __init__(self, sistema):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("Sistema de Votación Electrónica")
        self.geometry("400x300")
        
        # Guardar referencia al sistema de votación
        self.sistema = sistema
        
        # Etiqueta de título
        self.label_titulo = ctk.CTkLabel(self, text="Seleccione una lista para votar", font=("Arial", 16))
        self.label_titulo.pack(pady=10)
        
        # Crear botones para cada lista
        self.lista_botones = []
        for lista in self.sistema.listas:
            boton = ctk.CTkButton(self, text=f"{lista.nombre} ({lista.color})", 
                                  command=lambda l=lista.nombre: self.votar_con_retraso(l))
            boton.pack(pady=5)
            self.lista_botones.append(boton)
        
        # Etiqueta de mensaje
        self.label_mensaje = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.label_mensaje.pack(pady=10)
        
        # Botón para mostrar resultados
        self.boton_resultados = ctk.CTkButton(self, text="Mostrar Resultados", command=self.mostrar_resultados)
        self.boton_resultados.pack(pady=10)
    
    def votar_con_retraso(self, nombre_lista):
        """Inicia un hilo para manejar el voto con retraso."""
        # Lanza el proceso de votación en un hilo para evitar que la interfaz se congele
        threading.Thread(target=self.votar, args=(nombre_lista,)).start()

    def votar(self, nombre_lista):
        """Lógica para manejar el voto desde la interfaz con un retraso."""
        # Muestra un mensaje temporal mientras se espera
        self.label_mensaje.configure(text=f"Votando por la {nombre_lista}... Espere un momento.")
        
        # Llama a la función de votar del sistema
        mensaje = self.sistema.votar(nombre_lista)
        
        # Actualiza el mensaje después del retraso
        self.label_mensaje.configure(text=mensaje)

    def mostrar_resultados(self):
        """Muestra los resultados de la votación."""
        resultados = self.sistema.obtener_resultados()
        self.label_mensaje.configure(text=resultados)

# Crear el sistema de votación y las listas
sistema = SistemaVotacion()
sistema.agregar_lista(Lista("Roja", "Rojo"))
sistema.agregar_lista(Lista("Azul", "Azul"))

# Iniciar la aplicación
app = VotacionApp(sistema)
app.mainloop()
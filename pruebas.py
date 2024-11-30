from customtkinter import *
import os

class Lista:
    def __init__(self, color, name):
        self.color = color
        self.name = name.capitalize()
        self.votos = 0

    def votar(self):
        self.votos += 1

    def __str__(self):
        return f'Lista {self.name} (Color: {self.color}, Votos: {self.votos})'


class SistemaVotacion:
    def __init__(self, txt_file="resultados_votacion.txt"):
        self.listas = []
        self.txt_file = txt_file
        self.total_votos = 0
        self.inicializar_txt()

    def agregar_lista(self, lista):
        self.listas.append(lista)

    def votar(self, nombre_lista):
        lista = next((l for l in self.listas if l.name == nombre_lista.capitalize()), None)
        if lista:
            lista.votar()
            self.total_votos += 1
            self.actualizar_txt()
            return f"¡Votaste por la {nombre_lista}!"
        else:
            return f"La lista {nombre_lista} no existe."

    def inicializar_txt(self):
        with open(self.txt_file, "w") as file:
            file.write("Resultados de la Votación:\n\n")

    def actualizar_txt(self):
        with open(self.txt_file, "w") as file:
            file.write("Resultados de la Votación:\n\n")
            for lista in self.listas:
                porcentaje = (lista.votos / self.total_votos * 100) if self.total_votos > 0 else 0
                file.write(f"{lista.name}: {lista.votos}  -  {porcentaje:.2f}%\n")

    def obtener_resultados(self):
        resultados = "Resultados de la votación:\n\n"
        for lista in self.listas:
            porcentaje = (lista.votos / self.total_votos * 100) if self.total_votos > 0 else 0
            resultados += f"{lista.name}: {lista.votos} votos ({porcentaje:.2f}%)\n"
        return resultados


class VotacionApp(CTk):
    def __init__(self, sistema):
        super().__init__()

        # Maximizar la ventana para ocupar toda la pantalla
        self.attributes('-fullscreen', True)

        # Desactivar el botón de cerrar
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        # Permitir cerrar con la tecla "p"
        self.bind("<p>", lambda event: self.destroy())

        self.title("Sistema de Votación Electrónica")

        # Frames
        self.frame_botones = CTkFrame(self)
        self.frame_mensaje = CTkFrame(self)

        self.frame_botones.pack(fill="both", expand=True)

        # Sistema de votación
        self.sistema = sistema

        # Frame de botones (votación)
        self.label_titulo = CTkLabel(self.frame_botones, text="Seleccione una lista para votar", font=("Arial", 16))
        self.label_titulo.pack(pady=10)

        self.lista_botones = []
        for lista in self.sistema.listas:
            boton = CTkButton(self.frame_botones, text=f"Lista {lista.name}",
                              command=lambda nombre=lista.name: self.mostrar_mensaje_temporal(nombre, 5000))
            boton.pack(pady=5)
            self.lista_botones.append(boton)

        # Frame de mensaje (descanso)
        self.label_mensaje = CTkLabel(self.frame_mensaje, text="Gracias por votar. Espere unos segundos...",
                                      font=("Arial", 22))
        self.label_mensaje.pack(expand=True)

    def mostrar_mensaje_temporal(self, nombre_lista, retraso):
        # Realiza la votación
        resultado = self.sistema.votar(nombre_lista)
        print(resultado)

        # Muestra el mensaje temporal
        self.frame_botones.pack_forget()
        self.frame_mensaje.pack(fill="both", expand=True)

        # Vuelve al frame de botones después de un retraso
        self.after(retraso, self.mostrar_botones)

    def mostrar_botones(self):
        self.frame_mensaje.pack_forget()
        self.frame_botones.pack(fill="both", expand=True)


# Configuración inicial
listas = {
    'roja': '#F80606',
    'naranja': '#F89706'
}

sistema = SistemaVotacion()
for nombre, color in listas.items():
    sistema.agregar_lista(Lista(name=nombre, color=color))

# Inicializa el archivo de texto con las listas
sistema.inicializar_txt()

# Inicia la aplicación
app = VotacionApp(sistema)
app.mainloop()
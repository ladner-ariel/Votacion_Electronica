from customtkinter import *
import os

class Lista:
    def __init__(self, color, name):
        self.color = color
        self.name = name.upper()  # Convertir el nombre a mayúsculas
        self.votos = 0

    def votar(self):
        self.votos += 1

    def __str__(self):
        return f'LISTA {self.name} (COLOR: {self.color}, VOTOS: {self.votos})'


class SistemaVotacion:
    def __init__(self, txt_file="resultados_votacion.txt"):
        self.listas = []
        self.txt_file = txt_file
        self.total_votos = 0
        self.inicializar_txt()

    def agregar_lista(self, lista):
        self.listas.append(lista)

    def votar(self, nombre_lista):
        lista = next((l for l in self.listas if l.name == nombre_lista.upper()), None)
        if lista:
            lista.votar()
            self.total_votos += 1
            self.actualizar_txt()
            return f"¡VOTASTE POR LA {nombre_lista}!"
        else:
            return f"LA LISTA {nombre_lista} NO EXISTE."

    def inicializar_txt(self):
        with open(self.txt_file, "w") as file:
            file.write("RESULTADOS DE LA VOTACIÓN:\n\n")

    def actualizar_txt(self):
        with open(self.txt_file, "w") as file:
            file.write("RESULTADOS DE LA VOTACIÓN:\n\n")
            for lista in self.listas:
                porcentaje = (lista.votos / self.total_votos * 100) if self.total_votos > 0 else 0
                file.write(f"{lista.name}: {lista.votos}  -  {porcentaje:.2f}%\n")

    def guardar_backup(self):
        with open("backup_resultados_votacion.txt", "w") as file:
            file.write("COPIA DE SEGURIDAD - RESULTADOS DE LA VOTACIÓN:\n\n")
            for lista in self.listas:
                porcentaje = (lista.votos / self.total_votos * 100) if self.total_votos > 0 else 0
                file.write(f"{lista.name}: {lista.votos}  -  {porcentaje:.2f}%\n")


class VotacionApp(CTk):
    def __init__(self, sistema):
        super().__init__()
        # Ocupa toda la pantalla
        self.title("Sistema de Votación Electrónica")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        # self.attributes('-fullscreen', True)

        # Desactiva el botón de cerrar
        self.protocol("WM_DELETE_WINDOW", self.guardar_copia_seguridad)
        self.bind("<p>", lambda event: self.destroy())

        # Sistema de votación
        self.sistema = sistema

        # Frames
        self.frame_botones = CTkFrame(self)
        self.frame_mensaje = CTkFrame(self)

        self.frame_botones.pack(fill="both", expand=True)

        # Etiqueta principal
        self.label_titulo = CTkLabel(
            self.frame_botones,
            text="SELECCIONE UNA LISTA PARA VOTAR",
            font=("Arial", 24, "bold")  # Texto más grande y en negrita
        )
        self.label_titulo.pack(pady=(30, 0))

        # Subtítulo
        self.label_subtitulo = CTkLabel(
            self.frame_botones,
            text="",
            font=("Arial", 18, "bold")  # Texto más grande y en negrita
        )
        self.label_subtitulo.pack(pady=(5, 20))

        # Botones de votación
        self.lista_botones = []
        for lista in self.sistema.listas:
            boton = CTkButton(
                self.frame_botones,
                text=lista.name,
                fg_color=lista.color,
                hover_color=lista.color,
                corner_radius=10,  # Hacer los botones cuadrados
                font=("Arial", 18, "bold"),  # Texto en negrita
                command=lambda nombre=lista.name: self.mostrar_mensaje_temporal(nombre, 2000)
            )
            boton.pack(pady=70, ipadx=30, ipady=60)  # Ajustar tamaño del botón
            self.lista_botones.append((boton, lista))  # Asocia el botón con su lista

        # Vincula eventos de hover
        for boton, lista in self.lista_botones:
            boton.bind("<Enter>", lambda event, l=lista: self.mostrar_subtitulo_hover(l))
            boton.bind("<Leave>", lambda event: self.limpiar_subtitulo_hover())

        # Frame de mensaje (descanso)
        self.label_mensaje = CTkLabel(
            self.frame_mensaje,
            text="GRACIAS POR VOTAR. ESPERE UNOS SEGUNDOS...",
            font=("Arial", 22, "bold")  # Texto grande y en negrita
        )
        self.label_mensaje.pack(expand=True)

    def mostrar_subtitulo_hover(self, lista):
        """Actualiza el subtítulo al pasar el cursor sobre un botón."""
        self.label_subtitulo.configure(
            text=f"(LISTA {lista.name})",
            text_color=lista.color  # Cambia el color del texto al color de la lista
        )

    def limpiar_subtitulo_hover(self):
        """Limpia el subtítulo al salir del hover."""
        self.label_subtitulo.configure(text="")

    def mostrar_mensaje_temporal(self, nombre_lista, retraso):
        # Realiza la votación
        resultado = self.sistema.votar(nombre_lista)
        print(resultado)  # Imprime en la consola

        # Muestra el mensaje temporal
        self.frame_botones.pack_forget()
        self.frame_mensaje.pack(fill="both", expand=True)

        # Vuelve al frame de botones después de un retraso
        self.after(retraso, self.mostrar_botones)

    def mostrar_botones(self):
        self.frame_mensaje.pack_forget()
        self.frame_botones.pack(fill="both", expand=True)

    def guardar_copia_seguridad(self):
        self.sistema.guardar_backup()
        print("Copia de seguridad guardada en 'backup_resultados_votacion.txt'")


set_appearance_mode("dark")  # Activa el modo oscuro
set_default_color_theme("dark-blue")  # Tema de color oscuro

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
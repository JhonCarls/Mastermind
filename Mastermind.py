import tkinter as tk
import random
from tkinter import messagebox
import pygame

# Inicializar la música de fondo con pygame
pygame.mixer.init()

# Colores posibles (7 colores)
COLORES = ['Rojo', 'Azul', 'Verde', 'Amarillo', 'Morado', 'Naranja', 'Rosado']

# Diccionario para mapear colores en español con sus valores de color
MAPA_COLORES = {
    'Rojo': 'red',
    'Azul': 'blue',
    'Verde': 'green',
    'Amarillo': 'yellow',
    'Morado': 'purple',
    'Naranja': 'orange',
    'Rosado': 'pink'
}

# Generar combinación secreta aleatoria de 5 colores
def generar_combinacion():
    return random.sample(COLORES, 5)

# Comparar intento con la combinación secreta y devolver las pistas
def evaluar_intento(combinacion_secreta, intento):
    correctos_y_posicion = sum([1 for i in range(5) if intento[i] == combinacion_secreta[i]])
    correctos_sin_posicion = sum([min(combinacion_secreta.count(c), intento.count(c)) for c in set(intento)]) - correctos_y_posicion
    return correctos_y_posicion, correctos_sin_posicion

# Clase principal del juego
class Mastermind(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mastermind - Adivina la combinación de colores")
        self.geometry("700x700")
        self.config(bg="lightgray")
        
        # Reproducir música de fondo
        pygame.mixer.music.load("musica_fondo.mp3")
        pygame.mixer.music.play(-1)  # Reproduce en bucle
        
        # Generar combinación secreta
        self.combinacion_secreta = generar_combinacion()
        self.intentos = []
        self.max_intentos = 5

        # Etiqueta del título del juego
        self.label_titulo = tk.Label(self, text="MASTERMIND", font=("Arial", 24, "bold"), bg="lightgray", fg="black")
        self.label_titulo.pack(pady=10)

        # Etiqueta de listado de colores
        self.label_colores = tk.Label(self, text="Listado de colores disponibles:", font=("Arial", 14), bg="lightgray", fg="black")
        self.label_colores.pack(pady=5)
        
        # Crear interfaz gráfica con botones de colores
        self.canvas = tk.Canvas(self, width=550, height=400, bg='white', highlightbackground="black")
        self.canvas.pack(pady=10)

        # Botones de colores disponibles
        self.botones_colores = []
        for i, color in enumerate(COLORES):
            btn = tk.Button(self, text=color, bg=MAPA_COLORES[color], width=8, command=lambda c=color: self.seleccionar_color(c))
            btn.place(x=130 + i * 70, y=550)
            self.botones_colores.append(btn)
        
        # Etiqueta para mostrar el intento actual
        self.label_intento = tk.Label(self, text="Selecciona 5 colores:", font=("Arial", 10), bg="lightgray", fg="black")
        self.label_intento.pack(pady=(0,35))

        # Botón para validar el intento
        self.btn_validar = tk.Button(self, text="Validar intento", font=("Arial", 12, "bold"), command=self.validar_intento)
        self.btn_validar.pack(pady=0)
        
        # Botón para reiniciar el juego
        self.btn_reiniciar = tk.Button(self, text="Reiniciar juego", font=("Arial", 12, "bold"), command=self.reiniciar_juego)
        self.btn_reiniciar.pack(pady=5)

        # Variables para el intento actual
        self.intento_actual = []

    def seleccionar_color(self, color):
        if len(self.intento_actual) < 5:
            self.intento_actual.append(color)
            self.dibujar_intento()

    def dibujar_intento(self):
        self.canvas.delete("intento")
        for i, color in enumerate(self.intento_actual):
            self.canvas.create_oval(20 + i * 60, 270, 70 + i * 60, 320, fill=MAPA_COLORES[color], tags="intento")

    def validar_intento(self):
        if len(self.intento_actual) == 5:
            # Evaluar el intento actual
            correctos_y_posicion, correctos_sin_posicion = evaluar_intento(self.combinacion_secreta, self.intento_actual)
            
            # Mostrar pistas
            self.intentos.append((self.intento_actual, correctos_y_posicion, correctos_sin_posicion))
            self.mostrar_intentos()
            
            # Limpiar el intento actual
            self.intento_actual = []
            self.canvas.delete("intento")
            
            # Verificar si el jugador ha ganado
            if correctos_y_posicion == 5:
                self.mostrar_ganador()
            elif len(self.intentos) >= self.max_intentos:
                self.mostrar_perdedor()

    def mostrar_intentos(self):
        self.canvas.delete("intentos_previos")
        for idx, (intento, correctos_y_posicion, correctos_sin_posicion) in enumerate(self.intentos):
            # Dibujar los colores del intento
            for i, color in enumerate(intento):
                self.canvas.create_oval(20 + i * 60, 20 + idx * 60, 70 + i * 60, 70 + idx * 60, fill=MAPA_COLORES[color], tags="intentos_previos")
            
            # Mostrar las pistas al lado del intento
            self.canvas.create_text(410, 40 + idx * 60, text=f"Adivinados: {correctos_sin_posicion}, Posición correcta: {correctos_y_posicion}", font=("Arial", 9, "bold"), tags="intentos_previos")

    def mostrar_ganador(self):
        messagebox.showinfo("¡Ganaste!", "¡Felicitaciones, has adivinado la combinación!")
        self.reiniciar_juego()

    def mostrar_perdedor(self):
        respuesta = messagebox.askyesno("Perdiste", f"La combinación secreta era {self.combinacion_secreta}. ¿Quieres volver a intentar?")
        if respuesta:
            self.reiniciar_juego()
        else:
            self.destroy()

    def reiniciar_juego(self):
        self.combinacion_secreta = generar_combinacion()
        self.intentos = []
        self.canvas.delete("intentos_previos")
        self.intento_actual = []
        self.canvas.delete("intento")

# Iniciar el juego
if __name__ == "__main__":
    juego = Mastermind()
    juego.mainloop()
    pygame.mixer.music.stop()  # Detener la música al salir

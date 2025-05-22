

import random
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import pyttsx3

engine = pyttsx3.init()

# Obtener todas las voces disponibles
voices = engine.getProperty('voices')

# Buscar una voz en español (puede variar según tu sistema)
for voice in voices:
    if 'spanish' in voice.name.lower() or 'español' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
else:
    # Si no encuentra voz en español, usar la primera disponible
    engine.setProperty('voice', voices[0].id)

engine.setProperty('rate', 150)  # Velocidad del habla



# Variables globales del juego
numbers_called = []
card = []
game_over = False
card_labels = []
called_numbers_text = None
number_label = None
last_number_label = None  # Nueva etiqueta para mostrar el último número llamado
completed_patterns = set()  # Para registrar los patrones ya completados

def speak(text):
    engine.say(text)
    engine.runAndWait()

def reset_game():
    global numbers_called, card, game_over, completed_patterns
    numbers_called = []
    card = generate_card()
    game_over = False
    completed_patterns = set()  # Limpiar patrones completados
    update_display()

def generate_card():
    # Generar una tarjeta de bingo válida
    card_columns = []
    # B: 1-15, I: 16-30, N:31-45, G:46-60, O:61-75
    ranges = [(1, 15), (16, 30), (31, 45), (46, 60), (61, 75)]
    
    for i in range(5):
        column = random.sample(range(ranges[i][0], ranges[i][1] + 1), 5)
        if i == 2:  # La columna N tiene un espacio libre en el medio
            column[2] = "⭐"
        card_columns.append(column)
    
    # Transponer para tener filas en lugar de columnas
    rows = list(zip(*card_columns))
    return [list(row) for row in rows]

def get_letter(number):
    # Determinar la letra correspondiente al número
    if 1 <= number <= 15:
        return "B"
    elif 16 <= number <= 30:
        return "I"
    elif 31 <= number <= 45:
        return "N"
    elif 46 <= number <= 60:
        return "G"
    elif 61 <= number <= 75:
        return "O"
    return ""

def call_number():
    global numbers_called, game_over
    
    if game_over:
        messagebox.showinfo("Juego terminado", "¡BINGO COMPLETO! Presiona 'Reiniciar Juego' para jugar otra vez.")
        return
        
    if len(numbers_called) == 75:
        messagebox.showinfo("Fin del juego", "Todos los números han sido llamados!")
        game_over = True
        return
        
    available_numbers = [num for num in range(1, 76) if num not in numbers_called]
    number = random.choice(available_numbers)
    numbers_called.append(number)
    
    # Obtener letra y anunciar
    letter = get_letter(number)
    display_text = f"{letter}-{number}"
    
    # Actualizar display visual
    last_number_label.config(text=display_text, font=("Helvetica", 24, "bold"), fg="red")
    
    speak(f"{letter} {number}")
    
    # Verificar si hay ganador (solo para BINGO COMPLETO)
    result = check_card()
    if result == "BINGO COMPLETO!":
        messagebox.showinfo("¡Ganador!", "¡FELICIDADES! ¡BINGO COMPLETO!")
        speak("¡Bingo completo! ¡Felicidades!")
        game_over = True
    elif result and result not in completed_patterns:  # Solo muestra patrones nuevos
        messagebox.showinfo("Patrón completado", f"¡Completaste un {result}! Sigue jugando...")
        speak(f"¡Patrón completado! {result}")
        completed_patterns.add(result)  # Registrar que este patrón ya fue notificado
    
    update_display()

def check_card():
    marked = [[False for _ in range(5)] for _ in range(5)]
    
    # Marcar las casillas que coinciden con números llamados
    for i in range(5):
        for j in range(5):
            if card[i][j] in numbers_called or card[i][j] == "⭐":
                marked[i][j] = True
                
    # Verificar bingo completo (solo este termina el juego)
    if all(all(row) for row in marked):
        return "BINGO COMPLETO!"
        
    # Verificar otros patrones (no terminan el juego)
    # Líneas horizontales
    for row in marked:
        if all(row):
            return "Línea horizontal"
            
    # Líneas verticales
    for col in zip(*marked):
        if all(col):
            return "Línea vertical"
            
    # Diagonales
    if all(marked[i][i] for i in range(5)):
        return "Diagonal principal"
        
    if all(marked[i][4-i] for i in range(5)):
        return "Diagonal secundaria"
        
    # Esquinas
    if (marked[0][0] and marked[0][4] and marked[4][0] and marked[4][4]):
        return "Cuatro esquinas"
        
    return None

def update_display():
    # Actualizar la tarjeta en pantalla
    for i in range(5):
        for j in range(5):
            value = card[i][j]
            card_labels[i][j].config(text=str(value))
            
            # Resaltar números marcados
            if value == "⭐":
                card_labels[i][j].config(bg="yellow")
            elif value in numbers_called:
                card_labels[i][j].config(bg="light green")
            else:
                card_labels[i][j].config(bg="white")
    
    # Actualizar números llamados
    called_numbers_text.delete(1.0, tk.END)
    if numbers_called:
        called_str = ", ".join(map(str, sorted(numbers_called)))
        called_numbers_text.insert(tk.END, called_str)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Bingo")
ventana.geometry("900x700")

# Configurar fuente
custom_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")

# Marco principal
main_frame = tk.Frame(ventana)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Título
title_label = tk.Label(
    main_frame, 
    text="BINGO", 
    font=title_font,
    fg="red"
)
title_label.pack(pady=10)

# Marco para mostrar el último número llamado
last_number_frame = tk.Frame(main_frame)
last_number_frame.pack(pady=10)

tk.Label(last_number_frame, text="Último número:", font=custom_font).pack(side=tk.LEFT)

last_number_label = tk.Label(
    last_number_frame,
    text="Ninguno",
    font=("Helvetica", 24, "bold"),
    fg="black"
)
last_number_label.pack(side=tk.LEFT, padx=10)

# Marco para la tarjeta de bingo
card_frame = tk.Frame(main_frame)
card_frame.pack(pady=20)

# Letras B-I-N-G-O arriba de cada columna
letters = ["B", "I", "N", "G", "O"]
for j in range(5):
    letter_label = tk.Label(
        card_frame, 
        text=letters[j], 
        font=custom_font,
        fg="blue"
    )
    letter_label.grid(row=0, column=j, pady=(0, 5))

# Crear etiquetas para la tarjeta
etiquetas_tarjetas = []
para i en rango(1, 6):  # Empieza en 1 por las letras arriba
 etiquetas_fila = []
 para j en rango(5):
 etiqueta = tk.Etiqueta(
 card_frame, 
 texto="", 
 ancho=4, 
 alta=2,
 alivio=tk.CRESTA,
 fuente=fuente_personalizada
        )
 etiqueta.rejilla(fila=i, columna=j, padx=2, pady=2)
 row_labels.append(etiqueta)
 card_labels.append(fila_etiquetas)

# Marco para los controles
control_frame = tk.Marco(main_frame)
control_frame.paquete(pady=20)

# Botón para llamar al mundo
botón_llamada = tk.Botón(
 marco_control,
 texto=„Llamar Número",
 comando=número_llamada,
 fuente=fuente_personalizada,
 bg="verde",
 fg="blanco"
)
botón_llamada.paquete(lado=tk.IZQUIERDA, padx=10)

# Botón para reiniciar
botón_reset = tk.Botón(
 marco_control,
 texto=„Reiniciar Juego",
 comando=reset_game,
 fuente=fuente_personalizada,
 bg="azul",
 fg="blanco"
)
reset_button.paquete(lado=tk.IZQUIERDA, padx=10)

# Área para matar nuevos llamados
llamado_números_marco = tk.Marco(main_frame)
marco_números_llamado.paquete(pady=10)

tk.Etiqueta(marco_números_llamado, texto="Números llamados:", fuente=fuente_personalizada).paquete()

llamado_números_texto = tk.Texto(
 marco_números_llamado,
 alta=5,
 ancho=50,
 fuente=(„Helvética", 10)
)
llamado_números_texto.paquete()

# Inicializar el juego
reset_game()

# Iniciar la aplicación
ventana.mainloop()

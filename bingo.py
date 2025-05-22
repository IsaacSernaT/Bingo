importar aleatorio
importar tkinter como tk
desde tkinter importar cuadro de mensaje
desde tkinter importar fuente como fuente tk
importar pyttsx3

motor = pyttsx3.init()

# Obtener todas las voces disponibles
voces = motor.obtener propiedad('voces')

# Buscar una voz en español (puede variar según tu sistema)
para voz en voces:
 si 'español' en voz.nombre.inferior() o 'español' en voz.nombre.inferior():
 motor.establecer propiedad('voz', voz.id)
 romper
de lo contrario:
 # Si no encuentro voz en español, usar la primera disponible
 motor.establecer propiedad('voz', voces[0].id)

motor.establecer propiedad('tasa', 150) # Velocidad del habla

# Variables globales del juego
números_llamados = []
tarjeta = []
game_over = Falso
etiquetas_tarjetas = []
texto_números_llamados = Ninguno
etiqueta_número = Ninguno
etiqueta_último_número = Ninguno # Nueva etiqueta para perder el último número llamado
patrones_completados = set() # Para registrador los patrones ya completos

def hablar(texto):
 motor.decir(texto)
 motor.correr y esperar()

def reset_game():
 global números_llamados, carta, juego_terminado, patrones_completados
 números_llamados = []
 tarjeta = generar_tarjeta()
 game_over = Falso
 patrones_completados = set() # Limpiar patrones completos
 actualizar_display()

def generar_tarjeta():
 # Generar una tarjeta de bingo válida
 columnas_tarjetas = []
 # B: 1-15, I: 16-30, N:31-45, G:46-60, O:61-75
 rangos = [(1, 15), (16, 30), (31, 45), (46, 60), (61, 75)]
    
 para i en rango(5):
 columna = aleatoria.muestra(rango(rangos[i][0], rangos[i][1] + 1), 5)
 si yo == 2: # La columna N tiene un espacio libre en el medio
 columna[2] = "⭐"
 card_columns.append(columna)
    
 # Transponedor para tener filas en lugar de columnas
 filas = lista(cremallera(*card_columns))
 retorno [lista(fila) para fila en filas]

def obtener_letra(número):
 # Determinar la letra correspondiente al número
 si 1 <= número <= 15:
 retorno "B"
 elif 16 <= número <= 30:
 retorno "Yo"
 elif 31 <= número <= 45:
 retorno "N"
 elif 46 <= número <= 60:
 retorno "G"
 elif 61 <= número <= 75:
 retorno "O"
 retorno ""

def número de llamada():
 global números_llamados, juego_terminado
    
 si game_over:
 cuadro de mensaje.showinfo("Juego terminado", "¡BINGO COMPLETO! Presiona 'Reiniciar Juego' para jugar otra vez.")
 retorno
        
 si len(números_llamados) == 75:
 cuadro de mensaje.showinfo(„Fin del juego", "¡Todos los números han sido llamados!")
 game_over = Verdaddero
 retorno
        
 números_disponibles = [num para num en el rango (1, 76) si num no está en números_llamados]
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
para i en el rango (1, 6): # Empieza en 1 por las letras arriba
 etiquetas_fila = []
 para j en el rango (5):
 etiqueta = tk.Label(
 card_frame, 
 text="", 
 ancho=4, 
 alta=2,
 alivio=tk.RIDGE,
 fuente=fuente_personalizada
        )
 etiqueta.grid(fila=i, columna=j, padx=2, pady=2)
 row_labels.append(etiqueta)
 card_labels.append(row_labels)

# Marco para los controles
control_frame = tk.Frame(main_frame)
control_frame.pack(pady=20)

# Botón para llamar al mundo
call_button = tk.Button(
 marco_control,
 texto="Llamar Número",
 comando=número_llamada,
 fuente=fuente_personalizada,
 bg="verde",
 fg="blanco"
)
call_button.pack(lado=tk.IZQUIERDA, padx=10)

# Botón para reiniciar
botón_reset = tk.Button(
 marco_control,
 texto="Reiniciar Juego",
 comando=reset_game,
 fuente=fuente_personalizada,
 bg="azul",
 fg="blanco"
)
reset_button.pack(lado=tk.IZQUIERDA, padx=10)

# Área para matar nuevos llamados
marco_números_llamado = tk.Frame(marco_principal)
llamado_numbers_frame.pack(pady=10)

tk.Label(llamado_numbers_frame, text="Números llamados:", font=custom_font).pack()

llamado_números_texto = tk.Texto(
 marco_números_llamado,
 alta=5,
 ancho=50,
 font=("Helvetica", 10)
)
llamado_números_texto.pack()

# Inicializar el juego
restablecer_juego()

# Iniciar la aplicación
ventana.mainloop

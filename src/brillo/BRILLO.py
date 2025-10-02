from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw, ImageFont
import screen_brightness_control as sbc
import threading
import schedule
import time

# Variable global para el brillo actual
current_brightness = sbc.get_brightness()[0]  # Obtener el brillo inicial

# Función para crear un ícono dinámico con el nivel de brillo actual
def create_icon(brightness):
    width, height = 64, 64
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Texto a mostrar
    text = f"{brightness}%"

    # Configurar fuente y tamaño (fuente por defecto si no encuentra Arial)
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except IOError:
        font = ImageFont.load_default()

    # Calcular posición del texto para centrarlo usando textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)  # Calcula los límites del texto
    text_width = text_bbox[2] - text_bbox[0]  # Ancho
    text_height = text_bbox[3] - text_bbox[1]  # Alto

    text_x = (width - text_width) // 2  # Centrar horizontalmente
    text_y = (height - text_height) // 2  # Centrar verticalmente

    # Dibujar el texto en la imagen
    draw.text((text_x, text_y), text, fill="black", font=font)
    return image

# Función para actualizar el icono con el brillo actual
def update_icon(icon):
    icon.icon = create_icon(current_brightness)  # Actualiza el icono dinámicamente

# Función genérica para ajustar el brillo
def adjust_brightness(amount, icon, item):
    global current_brightness
    try:
        # Modificar el brillo con el límite de 0 a 100
        new_brightness = max(0, min(current_brightness + amount, 100))
        sbc.set_brightness(new_brightness)  # Aplicar el nuevo brillo
        current_brightness = new_brightness  # Actualizar la variable global
        print(f"Brillo ajustado a {new_brightness}%")
        update_icon(icon)  # Actualizar icono
    except Exception as e:
        print(f"Error al ajustar el brillo: {e}")

# Funciones específicas para ajustar el brillo
def increase_brightness(icon, item):
    adjust_brightness(10, icon, item)  # Aumentar brillo en 10%

def decrease_brightness(icon, item):
    adjust_brightness(-10, icon, item)  # Reducir brillo en 10%

def set_brightness_100(icon, item):
    global current_brightness
    current_brightness = 100
    sbc.set_brightness(100)  # Establecer brillo al 100%
    print("Brillo establecido al 100%")
    update_icon(icon)  # Actualizar icono

def set_brightness_0(icon, item):
    global current_brightness
    current_brightness = 0
    sbc.set_brightness(0)  # Establecer brillo al 0%
    print("Brillo establecido al 0%")
    update_icon(icon)  # Actualizar icono

def set_brightness_50(icon, item):
    global current_brightness
    current_brightness = 50
    sbc.set_brightness(50)  # Establecer brillo al 50%
    print("Brillo establecido al 50%")
    update_icon(icon)  # Actualizar icono

# Crear menú para el tray icon
menu = Menu(
    MenuItem("Subir brillo al 100%", set_brightness_100),
    MenuItem("Subir brillo 10%", increase_brightness),
    MenuItem("Bajar brillo 50%", set_brightness_50),
    MenuItem("Bajar brillo 10%", decrease_brightness),
    MenuItem("Bajar brillo al 0%", set_brightness_0),
    MenuItem("Salir", lambda icon, item: icon.stop())
)

# Función para manejar clic izquierdo en el icono
def on_left_click(icon, event):
    # Puedes definir lo que debe hacer al hacer clic izquierdo
    print("Clic izquierdo realizado. Opciones disponibles:")
    icon.menu = menu  # Cambia el menú al hacer clic izquierdo
    icon.visible = True  # Asegúrate de que el icono sea visible
    icon.update_menu()

def auto_dim():
    global current_brightness
    try:
        if current_brightness != 0:
            sbc.set_brightness(0)
            current_brightness = 0
            print("Brillo automático: 0% por horario nocturno (schedule)")
            update_icon(icon)
    except Exception as e:
        print(f"Error al poner brillo en 0%: {e}")

# Programar la tarea diaria a las 21:00
schedule.every().day.at("21:00").do(auto_dim)

def schedule_thread():
    while True:
        schedule.run_pending()
        time.sleep(30)

# Inicializar el ícono con el brillo actual
icon = Icon("Control de Brillo", create_icon(current_brightness), menu=menu)

# Asignar evento de clic izquierdo
icon.on_left_click = on_left_click

# Lanzar el hilo de schedule para la tarea automática
threading.Thread(target=schedule_thread, daemon=True).start()

# Ejecutar el tray icon
icon.run()

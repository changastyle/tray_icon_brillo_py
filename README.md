# Tray Icon Brillo

Descarga el ejecutable para tu sistema desde la sección Releases:
- **Windows:** descarga el archivo `BRILLO.exe` y ejecútalo.
- **Linux:** descarga el archivo `brillo-linux`, dale permisos de ejecución (`chmod +x brillo-linux`) y ejecútalo (`./brillo-linux`).

Controla el brillo de la pantalla desde la bandeja del sistema en Windows y Linux.

## Características
- Ajusta el brillo manualmente desde el menú del icono.
- Brillo automático a 0% todos los días a las 21:00.
- Icono dinámico que muestra el nivel de brillo actual.
- Compatible con Windows y Linux.

## Instalación
1. Clona el repositorio o descarga los archivos.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta el programa:
   ```bash
   python src/brillo/BRILLO.py
   ```

## Dependencias principales
- pystray
- pillow
- screen-brightness-control
- schedule

## Uso
- Haz clic derecho en el icono para ver las opciones de brillo.
- El brillo se pondrá automáticamente en 0% a las 21:00 cada día.

## Contribuir
¡Se aceptan mejoras y sugerencias! Abre un issue o haz un pull request.

## Licencia
MIT

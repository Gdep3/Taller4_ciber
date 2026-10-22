# Taller 4 CIBER:
Abre una terminal en Kali Linux y ejecuta los siguientes bloques de comandos en orden:

### Crear los directorios del proyecto
```bash
mkdir -p ~/taller4_phishing/templates
cd ~/taller4_phishing
```

### Configurar el entorno virtual de Python e instalar Flask
```bash
# 1. Crear el entorno virtual
python3 -m venv venv

# 2. Activar el entorno virtual (verás '(venv)' al inicio de tu terminal)
source venv/bin/activate

# 3. Instalar Flask
pip install flask
```

### Crear el archivo del servidor (`app.py`)
Ejecuta el editor `nano` en la raíz del proyecto:
```bash
nano app.py
```
Pegar el archivo app.py, guarda con `Ctrl + O`, presiona `Enter` y sal con `Ctrl + X`:

### Crear la plantilla HTML (`templates/index.html`)
Ejecuta `nano` asegurándote de guardarlo dentro del directorio `templates/`:
```bash
nano templates/index.html
```
Pega el código HTML, guarda con `Ctrl + O`, presiona `Enter` y sal con `Ctrl + X`:
* **Error `500 Internal Server Error` en el navegador:**
  Ocurre cuando Flask no encuentra `index.html`. Detén el servidor (`Ctrl + C`), verifica que la carpeta se llame exactamente `templates` (en minúsculas y plural) y que `index.html` esté adentro (`ls templates/`).

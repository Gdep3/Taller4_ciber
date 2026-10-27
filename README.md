# Taller 4 CIBER

Abre una terminal en Kali Linux y ejecuta los siguientes bloques de comandos en orden:

### Clonar el repositorio
```bash
git clone https://github.com/Gdep3/Taller4_ciber.git ~/taller4_phishing
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

### Ejecutar el servidor
```bash
python3 app.py
```
Abre Firefox dentro de Kali y entra a http://127.0.0.1:5000

### Solución de problemas
* **Error `500 Internal Server Error` en el navegador:**
  Flask no encuentra `index.html`. Detén el servidor (`Ctrl + C`) y verifica que `index.html` esté dentro de la carpeta `templates/` (`ls templates/`).
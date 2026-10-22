# Laboratorio Taller 4: Phishing Local y Defensa de Formularios

Este repositorio contiene el entorno controlado para el **Taller 4 de Ciberseguridad**. Consiste en una plataforma web local desarrollada en Python (Flask) que simula un formulario de solicitud de desbloqueo de cuenta para analizar el flujo de captura de entradas, observar una vulnerabilidad de **Cross-Site Scripting Almacenado (Stored XSS)** y demostrar su mitigación mediante validación en el servidor y escape de salida.

---

## ⚠️ Reglas Éticas del Laboratorio
De acuerdo con la rúbrica de la asignatura, el uso de este entorno está sujeto a las siguientes condiciones estrictas:
* **Ejecución exclusiva en entorno local:** El servidor está configurado para escuchar únicamente en `127.0.0.1` (`localhost`).
* **Uso de datos ficticios:** No ingresar RUN, correos ni datos personales reales.
* **Prohibido exponer a Internet:** No utilizar túneles externos ni enviar enlaces a terceros.

---

## 📁 Estructura del Proyecto

El proyecto debe mantener exactamente la siguiente estructura de carpetas para que Flask encuentre la plantilla HTML sin arrojar un error `500 Internal Server Error`:

```text
taller4_phishing/
├── app.py                  # Servidor backend local, consola de observación y filtros de defensa
├── README.md               # Este archivo de instrucciones
└── templates/
    └── index.html          # Interfaz del formulario simulado y panel de auditoría
```

---

## 🚀 Guía de Instalación Paso a Paso (Kali Linux)

Abre una terminal en Kali Linux y ejecuta los siguientes bloques de comandos en orden:

### Paso 1: Crear los directorios del proyecto
```bash
mkdir -p ~/taller4_phishing/templates
cd ~/taller4_phishing
```

### Paso 2: Configurar el entorno virtual de Python e instalar Flask
```bash
# 1. Crear el entorno virtual
python3 -m venv venv

# 2. Activar el entorno virtual (verás '(venv)' al inicio de tu terminal)
source venv/bin/activate

# 3. Instalar Flask
pip install flask
```

### Paso 3: Crear el archivo del servidor (`app.py`)
Ejecuta el editor `nano` en la raíz del proyecto:
```bash
nano app.py
```
Pega el siguiente código completo, guarda con `Ctrl + O`, presiona `Enter` y sal con `Ctrl + X`:

```python
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import html
import re

app = Flask(__name__)

# Simulación de almacenamiento en backend (para demostrar Stored XSS)
SOLICITUDES_SOPORTE = []

def registrar_en_consola(modo, usuario, correo, mensaje):
    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "="*65)
    print(f"[CONSOLA LOCAL DE OBSERVACIÓN] - Hora: {hora_actual}")
    print(f"[MODO DEL SISTEMA]            - {modo}")
    print("-" * 65)
    print(f" -> Campo 'usuario' : {repr(usuario)}")
    print(f" -> Campo 'correo'  : {repr(correo)}")
    print(f" -> Campo 'mensaje' : {repr(mensaje)}")
    print("="*65 + "\n")

@app.route("/", methods=["GET", "POST"])
def portal():
    errores = []

    if request.method == "POST":
        if "limpiar" in request.form:
            SOLICITUDES_SOPORTE.clear()
            return redirect(url_for("portal"))

        usuario = request.form.get("usuario", "")
        correo = request.form.get("correo", "")
        mensaje = request.form.get("mensaje", "")
        modo_seguro = request.form.get("modo_seguro") == "on"

        estado = "PROTEGIDO (Validación en Servidor + Escape)" if modo_seguro else "VULNERABLE (Stored XSS Activo)"
        registrar_en_consola(estado, usuario, correo, mensaje)

        if modo_seguro:
            # 1. Validación estricta del lado servidor
            if len(usuario) > 20 or not re.match(r"^[a-zA-Z0-9_.-]+$", usuario):
                errores.append("Usuario inválido: debe ser alfanumérico y máximo 20 caracteres.")
            
            if len(correo) > 60 or not re.match(r"^[^@]+@[^@]+\.[^@]+$", correo):
                errores.append("Formato de correo electrónico no válido.")

            if len(mensaje) > 250:
                errores.append("El mensaje excede el límite permitido (máx 250 caracteres).")

            # 2. Escape de salida antes de persistir
            if not errores:
                SOLICITUDES_SOPORTE.append({
                    "hora": datetime.now().strftime("%H:%M:%S"),
                    "usuario": html.escape(usuario),
                    "correo": html.escape(correo),
                    "mensaje": html.escape(mensaje),
                    "seguro": True
                })
        else:
            # Modo vulnerable: persiste directamente la entrada sin sanitizar
            SOLICITUDES_SOPORTE.append({
                "hora": datetime.now().strftime("%H:%M:%S"),
                "usuario": usuario,
                "correo": correo,
                "mensaje": mensaje,
                "seguro": False
            })

    return render_template("index.html", solicitudes=SOLICITUDES_SOPORTE, errores=errores)

if __name__ == "__main__":
    print("Servidor iniciado en http://127.0.0.1:5000 (localhost estricto)")
    app.run(host="127.0.0.1", port=5000, debug=False)
```

### Paso 4: Crear la plantilla HTML (`templates/index.html`)
Ejecuta `nano` asegurándote de guardarlo dentro del directorio `templates/`:
```bash
nano templates/index.html
```
Pega el siguiente código HTML, guarda con `Ctrl + O`, presiona `Enter` y sal con `Ctrl + X`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Portal de Acceso Ciudadano - DemoLab</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f3f4f6; margin: 0; padding: 25px; display: flex; justify-content: center; gap: 25px; }
        .card { background: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); width: 420px; padding: 24px; box-sizing: border-box; }
        .banner-academico { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; padding: 8px; border-radius: 6px; font-size: 12px; text-align: center; margin-bottom: 18px; font-weight: 500; }
        h2 { font-size: 18px; color: #111827; margin-top: 0; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; }
        h3 { font-size: 15px; color: #1f2937; margin-top: 0; }
        label { display: block; font-size: 13px; font-weight: 600; color: #374151; margin-top: 12px; }
        input[type="text"], textarea { width: 100%; padding: 9px; margin-top: 5px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 13px; box-sizing: border-box; }
        input[type="text"]:focus, textarea:focus { border-color: #2563eb; outline: none; }
        .box-mitigacion { margin-top: 15px; background: #eff6ff; border: 1px solid #bfdbfe; padding: 10px; border-radius: 6px; }
        .box-mitigacion label { margin: 0; font-size: 13px; color: #1e40af; cursor: pointer; display: flex; align-items: center; gap: 8px; font-weight: 500; }
        button { width: 100%; margin-top: 16px; background-color: #1e40af; color: white; border: none; padding: 10px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 14px; }
        button:hover { background-color: #1d4ed8; }
        .btn-clear { background-color: #6b7280; margin-top: 8px; }
        .btn-clear:hover { background-color: #4b5563; }
        .errores { margin-top: 12px; padding: 10px; background: #fee2e2; border-left: 4px solid #ef4444; color: #b91c1c; font-size: 12px; border-radius: 0 4px 4px 0; }
        .registro-item { background: #f9fafb; border: 1px solid #e5e7eb; border-left: 4px solid #2563eb; padding: 10px; margin-bottom: 10px; border-radius: 4px; font-size: 13px; }
    </style>
</head>
<body>

    <!-- Panel izquierdo: Formulario de Campaña Simulada -->
    <div class="card">
        <div class="banner-academico">
            SIMULACIÓN LOCAL CONTROLADA<br>Uso exclusivo con datos ficticios (Kali Linux)
        </div>
        <h2>Portal de Acceso - Solicitud de Desbloqueo</h2>
        <form method="POST" action="/">
            <label for="usuario">Usuario / Identificador ficticio:</label>
            <input type="text" id="usuario" name="usuario" placeholder="Ej: 19876543-k" required>

            <label for="correo">Correo electrónico de contacto:</label>
            <input type="text" id="correo" name="correo" placeholder="Ej: usuario@laboratorio.local" required>

            <label for="mensaje">Motivo / Mensaje de soporte:</label>
            <textarea id="mensaje" name="mensaje" rows="3" placeholder="Ej: Solicito restablecer mi credencial..." required></textarea>

            <div class="box-mitigacion">
                <label>
                    <input type="checkbox" id="modo_seguro" name="modo_seguro">
                    Activar defensas del servidor (Validación + Escape)
                </label>
            </div>

            <button type="submit">Enviar Solicitud</button>
        </form>

        <form method="POST" action="/">
            <button type="submit" name="limpiar" class="btn-clear">Limpiar Registros del Servidor</button>
        </form>

        {% if errores %}
            <div class="errores">
                <strong>Solicitud rechazada:</strong>
                <ul style="margin: 4px 0 0 0; padding-left: 18px;">
                    {% for err in errores %}
                        <li>{{ err }}</li>
                    {% endfor %}
                </ul>
            </div>
        {% endif %}
    </div>

    <!-- Panel derecho: Registro de Solicitudes (Auditoría / Persistencia) -->
    <div class="card" style="width: 500px;">
        <h3>Consola Web de Auditoría (Datos Almacenados)</h3>
        <p style="font-size: 12px; color: #6b7280; margin-top: -5px;">Visualización de solicitudes persistentes en backend:</p>

        {% if not solicitudes %}
            <p style="font-size: 13px; color: #9ca3af; font-style: italic;">No hay registros almacenados.</p>
        {% endif %}

        {% for sol in solicitudes %}
            <div class="registro-item">
                <div style="font-size: 11px; color: #6b7280; margin-bottom: 4px;">
                    Hora: {{ sol.hora }} | Estado: {% if sol.seguro %}<span style="color:#16a34a; font-weight:bold;">Filtrado Seguro</span>{% else %}<span style="color:#dc2626; font-weight:bold;">Vulnerable (Stored XSS)</span>{% endif %}
                </div>
                <div><strong>Usuario:</strong> {{ sol.usuario }}</div>
                <div><strong>Correo:</strong> {{ sol.correo }}</div>
                <div><strong>Mensaje:</strong>
                    {% if not sol.seguro %}
                        {{ sol.mensaje | safe }}
                    {% else %}
                        {{ sol.mensaje }}
                    {% endif %}
                </div>
            </div>
        {% endfor %}
    </div>

</body>
</html>
```

---

## 🖥️ Ejecución del Laboratorio

1. Verifica con `ls -R` que tienes `app.py` en la carpeta raíz y `index.html` dentro de `templates/`.
2. Inicia el servidor ejecutando:
   ```bash
   python3 app.py
   ```
3. Abre Firefox en Kali Linux e ingresa a:
   ```text
   http://127.0.0.1:5000
   ```
4. **Disposición para el video:** Coloca la ventana de Firefox en la mitad izquierda de tu pantalla y la terminal de Kali Linux en la mitad derecha para que el registro por consola se vea en tiempo real.

---

## 🧪 Guía de Pruebas para la Demostración (Rúbrica)

### 1. Prueba de Flujo Normal (Observación en Consola)
* **Acción:** Con la casilla de defensas **desmarcada**, ingresa datos ficticios:
  * Usuario: `11222333-k`
  * Correo: `ciudadano@prueba.local`
  * Mensaje: `Solicito desbloqueo de mi cuenta.`
* **Qué evidenciar:** Mostrar cómo la terminal de Kali Linux imprime instantáneamente la **hora exacta**, el **nombre de cada campo** y el **valor ficticio capturado**.

### 2. Prueba de Entrada Hostil (Stored XSS / Modo Vulnerable)
* **Acción:** Dejando la casilla de defensas **desmarcada**, ingresa en el campo de mensaje una entrada con etiquetas HTML:
  ```html
  <u><b>Alerta: Entrada HTML inyectada de forma persistente</b></u>
  ```
* **Qué evidenciar:**
  1. En el panel derecho ("Consola Web de Auditoría"), el navegador **interpreta el código HTML** mostrando el texto subrayado y en negrita en lugar de tratarlo como texto plano.
  2. Si recargas la página (`F5`), el payload sigue almacenado en el servidor y se vuelve a ejecutar (persistencia).
  3. En la terminal de Kali queda registrada la cadena exacta con las etiquetas crudas para análisis forense.

### 3. Prueba de Mitigación y Defensa Activa (Modo Seguro)
* **Acción 1 (Validación de formato):** Marca la casilla **"Activar defensas del servidor"**. En el campo `usuario` escribe `usuario<script>` y envía.
  * **Resultado:** El servidor rechaza la petición antes de guardarla porque no cumple con la expresión regular de lista blanca (`^[a-zA-Z0-9_.-]+$`).
* **Acción 2 (Escape de salida):** Con la casilla marcada, ingresa un usuario y correo válidos, y en el mensaje vuelve a colocar `<u><b>Texto de prueba</b></u>`.
  * **Resultado:** El servidor aplica `html.escape()`, transformando `<` en `&lt;` y `>` en `&gt;`. En el panel derecho se observa la etiqueta impresa literalmente como texto inofensivo, neutralizando por completo la inyección.

---

## 🛠️ Solución de Problemas Comunes

* **Error `can't open file '.../app.py': [Errno 2] No such file or directory`:**
  Asegúrate de estar ubicado en la carpeta correcta ejecutando `cd ~/taller4_phishing` y verifica con `ls` que el archivo esté allí.
* **Error `500 Internal Server Error` en el navegador:**
  Ocurre cuando Flask no encuentra `index.html`. Detén el servidor (`Ctrl + C`), verifica que la carpeta se llame exactamente `templates` (en minúsculas y plural) y que `index.html` esté adentro (`ls templates/`).
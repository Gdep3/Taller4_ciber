from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import html
import re

app = Flask(__name__)

# Simulación de almacenamiento en backend
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
            # Validación estricta del lado servidor (Pág. 10)
            if len(usuario) > 20 or not re.match(r"^[a-zA-Z0-9_.-]+$", usuario):
                errores.append("Usuario inválido: debe ser alfanumérico y máximo 20 caracteres.")
            
            if len(correo) > 60 or not re.match(r"^[^@]+@[^@]+\.[^@]+$", correo):
                errores.append("Formato de correo electrónico no válido.")

            if len(mensaje) > 250:
                errores.append("El mensaje excede el límite permitido (máx 250 caracteres).")

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
    

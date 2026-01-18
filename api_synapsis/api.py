from flask import Flask, request, jsonify, send_from_directory
from processing.acoustic import analizar_audio
import os

app = Flask(__name__, static_folder="static")

BASE_UPLOAD = "uploads/pacientes"
os.makedirs(BASE_UPLOAD, exist_ok=True)

# ===== SERVIR FRONTEND =====
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# ===== API =====
@app.route("/analyze_audio", methods=["POST"])
def analyze_audio():
    paciente = request.form.get("paciente")
    file = request.files.get("file")

    if not paciente or not file:
        return jsonify({"error": "Faltan datos"}), 400

    paciente = paciente.replace(" ", "_")

    paciente_dir = os.path.join(BASE_UPLOAD, paciente)
    os.makedirs(paciente_dir, exist_ok=True)

    audio_path = os.path.join(paciente_dir, file.filename)
    file.save(audio_path)

    resultado = analizar_audio(audio_path, paciente_dir)
    return jsonify(resultado)

# ===== SERVIR IMÁGENES =====
@app.route("/uploads/pacientes/<paciente>/<filename>")
def serve_files(paciente, filename):
    return send_from_directory(
        os.path.join(BASE_UPLOAD, paciente),
        filename
    )

if __name__ == "__main__":
    app.run(debug=True)

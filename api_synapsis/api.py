# api.py
import os
import json
from flask import render_template
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from processing.acoustic import analizar_audio

app = Flask(__name__)
CORS(app)

BASE_UPLOAD = "uploads/pacientes"

if not os.path.exists(BASE_UPLOAD):
    os.makedirs(BASE_UPLOAD)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze_audio", methods=["POST"])
def analyze_audio():

    if "audio" not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400

    file = request.files["audio"]
    paciente = request.form.get("paciente")
    sexo = request.form.get("sexo")

    if file.filename == "":
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    paciente_dir = os.path.join(BASE_UPLOAD, paciente.replace(" ", "_"))

    if not os.path.exists(paciente_dir):
        os.makedirs(paciente_dir)

    audio_path = os.path.join(paciente_dir, file.filename)
    file.save(audio_path)

    resultado = analizar_audio(audio_path, paciente_dir, sexo)

    return jsonify(resultado)


@app.route("/historial/<paciente>")
def obtener_historial(paciente):

    paciente_dir = os.path.join(BASE_UPLOAD, paciente)
    historial_path = os.path.join(paciente_dir, "historial.json")

    if not os.path.exists(historial_path):
        return jsonify([])

    with open(historial_path, "r") as f:
        historial = json.load(f)

    return jsonify(historial)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)

if __name__ == "__main__":
    app.run(debug=True)
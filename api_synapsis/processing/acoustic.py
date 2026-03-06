import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime


def analizar_audio(path_audio, paciente_dir, sexo):

    snd = parselmouth.Sound(path_audio)

    pitch = snd.to_pitch()
    pitch_values = pitch.selected_array["frequency"]
    pitch_values = pitch_values[pitch_values > 0]

    f0_mean = np.mean(pitch_values)
    pitch_std = np.std(pitch_values)
    pitch_range = np.max(pitch_values) - np.min(pitch_values)
    cv_pitch = pitch_std / f0_mean

    intensity = snd.to_intensity()
    intensidad_mean = np.mean(intensity.values)

    point_process = parselmouth.praat.call(snd, "To PointProcess (periodic, cc)", 75, 500)
    jitter = parselmouth.praat.call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    shimmer = parselmouth.praat.call([snd, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    hnr = parselmouth.praat.call(snd, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr_mean = parselmouth.praat.call(hnr, "Get mean", 0, 0)

    # -----------------------
    # SCORE HEURÍSTICO
    # -----------------------

    score = 0

    if jitter > 0.01:
        score += 1
    if shimmer > 0.04:
        score += 1
    if hnr_mean < 20:
        score += 1

    if score == 0:
        clasificacion = "Normal"
    elif score == 1:
        clasificacion = "Leve"
    elif score == 2:
        clasificacion = "Moderado"
    else:
        clasificacion = "Severo"

    # -----------------------
    # COMPARACIÓN NORMATIVA
    # -----------------------

    if sexo == "M":
        rango_min = 85
        rango_max = 180
    else:
        rango_min = 165
        rango_max = 255

    if f0_mean < rango_min:
        estado_f0 = "Bajo"
    elif f0_mean > rango_max:
        estado_f0 = "Alto"
    else:
        estado_f0 = "Normal"

    # -----------------------
    # GRÁFICO PITCH
    # -----------------------

    plt.figure(figsize=(10, 4))
    plt.plot(pitch_values)
    plt.axhline(f0_mean, linestyle="--")
    plt.title("Curva de Pitch")
    plt.xlabel("Frames")
    plt.ylabel("Frecuencia (Hz)")
    plt.tight_layout()
    plt.savefig(os.path.join(paciente_dir, "pitch.png"), dpi=300)
    plt.close()

    # -----------------------
    # ESPECTROGRAMA
    # -----------------------

    plt.figure(figsize=(10, 4))
    plt.specgram(snd.values[0], Fs=snd.sampling_frequency)
    plt.title("Espectrograma")
    plt.xlabel("Tiempo")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig(os.path.join(paciente_dir, "spectrogram.png"), dpi=300)
    plt.close()

    # -----------------------
    # GUARDAR HISTORIAL
    # -----------------------

    historial_path = os.path.join(paciente_dir, "historial.json")

    registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "F0_mean": round(float(f0_mean), 2),
        "Jitter": round(float(jitter), 5),
        "Shimmer": round(float(shimmer), 5),
        "HNR": round(float(hnr_mean), 2),
        "Score": score
    }

    if os.path.exists(historial_path):
        with open(historial_path, "r") as f:
            historial = json.load(f)
    else:
        historial = []

    historial.append(registro)

    with open(historial_path, "w") as f:
        json.dump(historial, f, indent=4)

    return {
        "F0_mean": round(float(f0_mean), 2),
        "Pitch_std": round(float(pitch_std), 2),
        "Pitch_range": round(float(pitch_range), 2),
        "CV_pitch": round(float(cv_pitch), 4),
        "Intensidad": round(float(intensidad_mean), 2),
        "Jitter": round(float(jitter), 5),
        "Shimmer": round(float(shimmer), 5),
        "HNR": round(float(hnr_mean), 2),
        "Score": score,
        "Clasificacion": clasificacion,
        "F0_estado": estado_f0,
        "F0_rango_min": rango_min,
        "F0_rango_max": rango_max
    }
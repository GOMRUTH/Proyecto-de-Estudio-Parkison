# Proyecto-de-Estudio-Parkison
Proyecto de estudio para detección temprana de Parkinson

# Módulo de Análisis Acústico – SYNAPSIS

## 1. Descripción
Este proyecto corresponde al módulo de análisis acústico automático del sistema SYNAPSIS, orientado al estudio de parámetros vocales relevantes para la detección y seguimiento del Parkinson.

El sistema permite cargar audios de voz, analizarlos utilizando Praat-Parselmouth y generar métricas acústicas y visualizaciones que luego pueden ser integradas a un sistema clínico mayor.

---

## 2. Objetivo del Proyecto
Desarrollar un entorno local que:
- Analice audios de voz automáticamente
- Extraiga parámetros acústicos (Pitch, F0, etc.)
- Genere gráficos (Pitch y Espectrograma)
- Organice los resultados por paciente
- Permita futura integración con PHP y MySQL

---

## 3. Tecnologías Utilizadas
- Python 3.10+
- Flask
- Praat-Parselmouth
- NumPy
- Matplotlib
- HTML / CSS (Bootstrap)
- WAMP (para futura integración con MySQL)

---

## 4. Estructura del Proyecto

api_synapsis/
│
├── api.py # Servidor Flask
│
├── processing/
│ ├── init.py
│ └── acoustic.py # Análisis acústico con Praat
│
├── uploads/
│ └── Lucas/
│ ├ ── voz.wav
│ ├ ── pitch.png
│ └ ── spectrogram.png
│
├── static/
│ ├── index.html # Interfaz web
│ └── style.css
│
└── requirements.txt (a futuro)

# JazzNet Chord Generation

Este repositorio contiene un pipeline para generar, convertir y anotar progresiones de acordes en formato MIDI, WAV y JAMS.

## 🚀 Instalación

1. Clona este repositorio:
   ```sh
   git clone https://github.com/TU-USUARIO/jazznet-chord-generation.git
   cd jazznet-chord-generation

2. Crea y activa un entorno virtual:

    ```sh
    conda create --name jazznet-env python=3.9
    conda activate jazznet-env

3. Instala las dependencias:

    ```sh
    pip install -r requirements.txt


## 📜 Uso
Ejecuta el pipeline con:

    python main.py

## 📂 Estructura del Proyecto

```
CHORD_PROGRESSION_GENERATOR/
│
├── data/
│   ├── patterns/   # Archivos .mid que se generan
│   ├── wav/        # Archivos .wav convertidos
│   └── jams/       # Archivos .jams con anotaciones
│
├── notebooks/
│   └── chord_progressions.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuración global (rutas de carpetas, etc.)
│   ├── midi_generation.py  # Funciones para generar MIDI
│   ├── audio_conversion.py # Funciones para convertir MIDI a WAV, etc.
│   ├── jams_creation.py    # Funciones para generar JAMS
│   ├── chord_logic.py      # Lógica de acordes y progresiones
│   └── utils.py            # Funciones de utilidad, helper scripts
│
├── main.py                 # Punto de entrada si quisiéramos un CLI
├── requirements.txt
├── README.md
└── .gitignore

```
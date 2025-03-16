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
jazznet-chord-generation/
│── patterns/       # Archivos MIDI generados
│── wav/            # Archivos WAV convertidos
│── jams/           # Anotaciones JAMS
│── src/            # Código fuente del proyecto
│── notebooks/      # Jupyter Notebooks
│── requirements.txt
│── README.md
│── .gitignore
│── main.py
```
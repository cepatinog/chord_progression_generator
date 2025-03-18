#!/usr/bin/env python

import subprocess
from pathlib import Path
# Importamos variables globales desde config.py
from .config import MIDI_DIR, WAV_DIR, DEFAULT_SAMPLE_RATE

def midi_to_wav(midi_file: Path, sample_rate: int = DEFAULT_SAMPLE_RATE) -> Path:
    """
    Convierte un archivo MIDI a formato WAV usando Timidity y lo coloca en WAV_DIR.

    :param midi_file: Path absoluto o relativo del archivo .mid.
    :param sample_rate: Frecuencia de muestreo (por defecto la de config.py).
    :return: Ruta absoluta al archivo .wav generado.
    """
    # Nombre base sin extensión
    base_name = midi_file.stem
    # Construct la ruta final en WAV_DIR
    wav_file = WAV_DIR / f"{base_name}.wav"
    wav_file.parent.mkdir(parents=True, exist_ok=True)

    # Ejecutamos timidity:
    #  -Ow1 => salida WAV con 16 bits
    #  -s <sample_rate> => tasa de muestreo
    #  -o => archivo de salida
    subprocess.call([
        'timidity',
        str(midi_file),
        '-Ow1',
        '-s', str(sample_rate),
        '-o', str(wav_file)
    ])

    return wav_file


def convert_all_mid_in_folder(folder: Path):
    """
    Convierte todos los archivos .mid en la carpeta dada a formato WAV y
    los guarda en WAV_DIR.

    :param folder: Ruta de la carpeta donde se encuentran archivos .mid.
    """
    if not folder.exists():
        print(f"No existe la carpeta {folder}")
        return

    mid_files = list(folder.rglob("*.mid"))
    if not mid_files:
        print(f"No hay archivos .mid en {folder}")
        return

    for mf in mid_files:
        # Convertir y avisar
        output = midi_to_wav(mf)
        print(f"Convertido: {mf} => {output}")

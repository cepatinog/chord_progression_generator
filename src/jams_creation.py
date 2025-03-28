#!/usr/bin/env python

import jams
import json
from pathlib import Path

from .config import JAMS_DIR
from .roman_to_chord import roman_to_chord_label

def create_jams_file(
    roman_sequence: list,
    key: str,
    jam_name: str,
    progression_name: str = "",
    durations: list[float] = None
) -> Path:
    """
    Genera un archivo .jams a partir de una secuencia de acordes dada en 
    notación de numerales romanos (por ej. ["ii7", "V7", "Imaj7"]) y una tonalidad.
    Usa 'roman_to_chord_label' para obtener la etiqueta 
    oficial JAMS (p. ej. "D:min7", "G:7", "C:maj7").

    :param roman_sequence: Lista de numerales romanos (strings).
                           Ej: ["ii7", "V7", "Imaj7"]
    :param key: Tonalidad. Ej: "C"
    :param jam_name: Nombre base del archivo .jams
    :param progression_name: Nombre de la progresión (guarda en metadatos)
    :param duration_per_chord: Duración en segundos de cada acorde.
    :return: Path al archivo .jams creado.
    
    Sus duraciones reales son tomadas del archivo durations.json. Si no se pasan duraciones, se usa 2.0s por defecto.
    """
    jam = jams.JAMS()
    chord_annotation = jams.Annotation(namespace='chord')

    chord_labels = [roman_to_chord_label(roman, key) for roman in roman_sequence]

    start_time = 0.0
    for i, chord_lab in enumerate(chord_labels):
        dur = durations[i] if durations and i < len(durations) else 2.0
        chord_annotation.append(
            time=start_time,
            duration=dur,
            value=chord_lab
        )
        start_time += dur

    my_sandbox = jams.Sandbox()
    my_sandbox.roman_numerals = roman_sequence
    my_sandbox.key = key
    my_sandbox.durations = durations if durations else [2.0] * len(chord_labels)

    chord_annotation.sandbox = my_sandbox
    jam.annotations.append(chord_annotation)

    jam.file_metadata.title = progression_name
    jam.file_metadata.duration = start_time

    jam_path = JAMS_DIR / f"{jam_name}.jams"
    jam_path.parent.mkdir(parents=True, exist_ok=True)
    jam.save(str(jam_path))
    return jam_path

def create_jams_for_folder(folder: Path, roman_sequence: list, key: str, progression_name: str):
    if not folder.exists():
        print(f"No existe la carpeta {folder}")
        return

    mid_files = list(folder.rglob("*.mid"))
    if not mid_files:
        print(f"No hay archivos .mid en {folder}")
        return

    durations_path = folder / "durations.json"
    if durations_path.exists():
        with open(durations_path, "r") as f:
            durations_dict = json.load(f)
    else:
        durations_dict = {}

    for mf in mid_files:
        base_name = mf.stem
        durations = durations_dict.get(f"{base_name}.mid", None)
        jam_path = create_jams_file(
            roman_sequence=roman_sequence,
            key=key,
            jam_name=base_name,
            progression_name=progression_name,
            durations=durations
        )
        print(f"Creado .jams: {jam_path}")

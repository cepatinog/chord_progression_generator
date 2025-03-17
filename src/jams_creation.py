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
    duration_per_chord: float = 2.0
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
    :param duration_per_chord: Duración en segundos de cada acorde (por defecto, 2.0s).
    :return: Path al archivo .jams creado.
    """
    jam = jams.JAMS()
    chord_annotation = jams.Annotation(namespace='chord')

    # Mapeamos cada numeral romano a la etiqueta estilo "D:min7" usando 'roman_to_chord_label'
    chord_labels = []
    for roman in roman_sequence:
        chord_labels.append(roman_to_chord_label(roman, key))

    # Agregamos al annotation en el campo 'value' => "D:min7", etc.
    start_time = 0.0
    for chord_lab in chord_labels:
        chord_annotation.append(
            time=start_time,
            duration=duration_per_chord,
            value=chord_lab
        )
        start_time += duration_per_chord

    # Guardamos la secuencia de numerales romanos en sandbox
    #chord_annotation.sandbox["roman_numerals"] = roman_sequence
    #chord_annotation.sandbox["key"] = key  # opcional, por si quieres registrar la tonalidad

    my_sandbox = jams.Sandbox()
    my_sandbox.roman_numerals = roman_sequence
    my_sandbox.key = key

    chord_annotation.sandbox = my_sandbox
    jam.annotations.append(chord_annotation)

    # Agregamos la anotación de acordes al jam
    jam.annotations.append(chord_annotation)

    # Metadata
    jam.file_metadata.title = progression_name
    jam.file_metadata.duration = start_time

    # Construimos la ruta final en JAMS_DIR
    jam_path = JAMS_DIR / f"{jam_name}.jams"
    jam_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardamos
    jam.save(str(jam_path))
    return jam_path


def create_jams_for_folder(folder: Path, roman_sequence: list, key: str, progression_name: str):
    """
    Crea un archivo .jams para cada .mid en la carpeta dada, usando la misma
    secuencia de numerales romanos (roman_sequence) y tonalidad (key).
    La idea es que cada .mid corresponde a la misma progresión, 
    solo cambian las inversiones / octavas en la práctica.

    :param folder: Carpeta que contiene archivos .mid
    :param roman_sequence: Lista de numerales romanos, ej: ["ii7", "V7", "Imaj7"]
    :param key: Tonalidad. Ej: "C"
    :param progression_name: Nombre global de la progresión.
    """
    if not folder.exists():
        print(f"No existe la carpeta {folder}")
        return

    mid_files = list(folder.rglob("*.mid"))
    if not mid_files:
        print(f"No hay archivos .mid en {folder}")
        return

    for mf in mid_files:
        # Nombre base = nombre del .mid sin extensión
        base_name = mf.stem  
        # Llamamos a create_jams_file con la misma roman_sequence y key
        jam_path = create_jams_file(
            roman_sequence=roman_sequence,
            key=key,
            jam_name=base_name,
            progression_name=progression_name
        )
        print(f"Creado .jams: {jam_path}")

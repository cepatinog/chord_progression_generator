#!/usr/bin/env python

"""
Módulo: roman_to_chord
----------------------
Provee funciones para mapear un numeral romano (I, ii, V7, etc.)
a una etiqueta de acorde compatible con JAMS (p.ej. 'C:maj7', 'D:min7', 'G:7'),
para tonalidades mayores o menores, permitiendo notación # y b en la tónica.
"""


# 1) Diccionarios básicos de notas

# Notas con sostenido y bemol, mapeando a semitonos 0..11
NOTE_TO_INT = {
    "C": 0,   "C#": 1,  "Db": 1,
    "D": 2,   "D#": 3,  "Eb": 3,
    "E": 4,   "Fb": 4,  # 'Fb' = E
    "F": 5,   "E#": 5,  # 'E#' = F
    "F#": 6,  "Gb": 6,
    "G": 7,   "G#": 8,  "Ab": 8,
    "A": 9,   "A#": 10, "Bb": 10,
    "B": 11,  "Cb": 11, # 'Cb' = B
    "B#": 0   # 'B#' = C
}

# Transformación inversa (0..11 -> una forma de notación)
# Escogemos la forma # como principal
INT_TO_NOTE = {
    0: "C",   1: "C#",  2: "D",   3: "D#",
    4: "E",   5: "F",   6: "F#",  7: "G",
    8: "G#",  9: "A",  10: "A#", 11: "B"
}


# 2) Escalas para tonalidad mayor/menor

MAJOR_SCALE_INTERVALS = [0, 2, 4, 5, 7, 9, 11]  # I, II, III, IV, V, VI, VII
NATURAL_MINOR_INTERVALS = [0, 2, 3, 5, 7, 8, 10]  # i, ii°, III, iv, v, VI, VII

def parse_key(key_str: str):
    """
    Dado un string de tonalidad (ej. 'C', 'Am', 'Abm', 'F#', etc.),
    retorna (root_int, scale_type), donde:
      - root_int es el semitono base (0..11)
      - scale_type es 'major' o 'minor'
    Si la clave no se reconoce, fallback -> (0, 'major') => C mayor.
    """
    # Ejemplos: "Am" => root="A", minor
    #           "C" => root="C", major
    #           "F#m" => root="F#", minor
    #           "Abm" => root="Ab", minor
    # Verificamos si termina en 'm'
    k = key_str.strip()
    if k.lower().endswith("m"):
        # Tonalidad menor
        root_part = k[:-1]  # todo menos la 'm'
        scale_type = "minor"
    else:
        root_part = k
        scale_type = "major"

    root_part = root_part.strip()
    # Convertimos la raíz a semitonos
    if root_part not in NOTE_TO_INT:
        # fallback
        return 0, "major"  # C mayor
    root_int = NOTE_TO_INT[root_part]

    return root_int, scale_type

def get_scale_intervals(scale_type: str):
    """
    Retorna la lista de semitonos para la escala (major o minor).
    Por simplicidad, solo manejamos mayor o menor natural.
    """
    if scale_type == "minor":
        return NATURAL_MINOR_INTERVALS
    # default => major
    return MAJOR_SCALE_INTERVALS


# 3) Lógica para parsear numeral romano

# def roman_to_chord_label(roman: str, key: str = "C") -> str:
#     """
#     Convierte un numeral romano (por ej. 'I', 'ii', 'V7', 'iv,7', etc.)
#     a una etiqueta de acorde JAMS (por ej. 'C:maj7', 'D:min7', 'G:7'),
#     asumiendo la tonalidad dada (p. ej. 'A', 'Am', 'Eb', 'F#m').

#     Ejemplo:
#         roman_to_chord_label("I", "C")     -> "C:maj"
#         roman_to_chord_label("V7", "F")    -> "C:7"
#         roman_to_chord_label("ii,7", "G")  -> "A:min7"
#         roman_to_chord_label("i", "Am")    -> "A:min"
#         roman_to_chord_label("VII", "Ab")  -> "Eb:maj"
#     """

#     # 1) Parse tonalidad -> (root_int, scale_type)
#     root_key_int, scale_type = parse_key(key)

#     # 2) Definir la escala
#     scale_intervals = get_scale_intervals(scale_type)

#     # 3) Parse numeral: base + sufijo (7, maj7, etc.)
#     #   e.g. "V7" => base="V", sufijo="7"
#     #   e.g. "ii,7" => base="ii", sufijo="7"
#     #   e.g. "Imaj7" => base="I", sufijo="maj7"
#     r = roman.strip().lower()  # para manipular
#     suffix = ""

#     # Busca sufijo por si hay coma
#     # p.ej. "ii,7" => "ii" + "7"
#     if "," in r:
#         base_part, suffix = r.split(",", 1)
#         base_part = base_part.strip()
#         suffix = suffix.strip()
#     else:
#         # Si no hay coma, vemos si endswith
#         possible_suffixes = ["7", "maj7", "min7", "dim7", "hdim7"]
#         # Buscamos si hay uno de estos sufijos
#         # (ej. "V7" => base="v", suffix="7")
#         found_suf = None
#         for suf in possible_suffixes:
#             if r.endswith(suf):
#                 found_suf = suf
#                 break
#         if found_suf:
#             suffix = found_suf
#             # Remover el sufijo
#             base_part = r[: -len(suffix)].strip()
#         else:
#             base_part = r

#     # Chequeamos uppercase -> major triad, lowercase -> minor triad
#     # mapeo: I=0, II=1, III=2, IV=3, V=4, VI=5, VII=6
#     # Por si hay algo como "VII", "iii"
#     roman_map = {"i":0, "ii":1, "iii":2, "iv":3, "v":4, "vi":5, "vii":6}
#     # fallback
#     if base_part not in roman_map:
#         return "C:maj"

#     scale_index = roman_map[base_part]

#     # 4) Hallar semitonos de la raíz del acorde
#     offset = scale_intervals[scale_index]
#     chord_root_int = (root_key_int + offset) % 12

#     # 5) Triada base: uppercase => mayor, lowercase => menor
#     # OJO: base_part es minúscula siempre, pues hicimos r.lower()
#     # Debemos ver si en la original 'roman' estaba uppercase
#     # -> check first char
#     is_upper = roman.strip()[0].isupper()

#     if is_upper:
#         triad_qual = "maj"
#     else:
#         triad_qual = "min"

#     # Nombre de la nota => e.g. 2 => "D"
#     note_name = INT_TO_NOTE[chord_root_int]
#     chord_label = f"{note_name}:{triad_qual}"

#     # 6) Extender sufijo (7, maj7, min7, etc.)
#     # Ej. si suffix="7" y triad_qual="maj" => "C:7"
#     #     si suffix="7" y triad_qual="min" => "A:min7"
#     #     si suffix="maj7" => "C:maj7", etc.
#     if suffix == "7":
#         if triad_qual == "maj":
#             chord_label = f"{note_name}:7"
#         else:
#             chord_label = f"{note_name}:min7"
#     elif suffix == "maj7":
#         chord_label = f"{note_name}:maj7"
#     elif suffix == "min7":
#         chord_label = f"{note_name}:min7"
#     elif suffix == "dim7":
#         chord_label = f"{note_name}:dim7"
#     elif suffix == "hdim7":
#         chord_label = f"{note_name}:hdim7"

#     return chord_label

def roman_to_chord_label(roman: str, key: str = "C") -> str:
    """
    Convierte un numeral romano (por ej. 'I', 'ii', 'V7', 'iv,7', etc.)
    a una etiqueta de acorde JAMS (por ej. 'C:maj7', 'D:min7', 'G:7'),
    asumiendo la tonalidad dada (p. ej. 'A', 'Am', 'Eb', 'F#m').

    Soporta los siguientes sufijos:
    min, maj, dim, aug, min6, maj6, min7, minmaj7, maj7, 7, dim7, hdim7, sus2, sus4
    """

    # 1) Parse tonalidad -> (root_int, scale_type)
    root_key_int, scale_type = parse_key(key)

    # 2) Definir la escala
    scale_intervals = get_scale_intervals(scale_type)

    # 3) Parse numeral: base + sufijo
    r = roman.strip()
    suffix = ""

    possible_suffixes = [
        "min", "maj", "dim", "aug",
        "min6", "maj6",
        "min7", "minmaj7", "maj7", "7", "dim7", "hdim7",
        "sus2", "sus4"
    ]

    # Busca sufijo separado por coma
    if "," in r:
        base_part, suffix = r.split(",", 1)
        base_part = base_part.strip()
        suffix = suffix.strip()
    else:
        # Si no hay coma, busca sufijo al final del string
        r_lower = r.lower()
        found_suf = None
        for suf in possible_suffixes:
            if r_lower.endswith(suf):
                found_suf = suf
                break
        if found_suf:
            suffix = found_suf
            base_part = r[:-len(suffix)].strip()
        else:
            base_part = r

    # Mapeo numeral -> índice en escala
    roman_map = {"i": 0, "ii": 1, "iii": 2, "iv": 3, "v": 4, "vi": 5, "vii": 6}
    base_lower = base_part.lower()
    if base_lower not in roman_map:
        raise ValueError(f"Numeral romano no reconocido: {base_part}")

    scale_index = roman_map[base_lower]

    # Calcular nota raíz del acorde
    offset = scale_intervals[scale_index]
    chord_root_int = (root_key_int + offset) % 12
    note_name = INT_TO_NOTE[chord_root_int]

    # Si no hay sufijo, aplicar por defecto maj/min según mayúscula
    if not suffix:
        is_upper = base_part[0].isupper()
        triad_qual = "maj" if is_upper else "min"
        return f"{note_name}:{triad_qual}"

    # Retornar etiqueta JAMS final
    return f"{note_name}:{suffix}"




# def test_roman_to_chord():
#     """
#     Pruebas manuales de varios casos.
#     """

#     examples = [
#         # Tonalidad mayor
#         ("I", "C"),      # => "C:maj"
#         ("V7", "F"),     # => "C:7"
#         ("ii,7", "G"),   # => "A:min7"
#         ("VI", "G"),     # => "E:maj"
#         ("iii,maj7", "D"),  # => "F#:maj7"
#         # Tonalidad menor
#         ("i", "Am"),     # => "A:min"
#         ("vii", "Am"),   # => "G:maj" (en la nat. menor, 9 + 10?)
#         ("vii,7", "Am"), # => "G:7" => minimal dominantes
#         # Bemoles
#         ("I", "Ab"),     # => "Ab:maj"
#         ("IV,7", "Eb"),  # => "Ab:7"
#         # Sufijos
#         ("v,7", "Cm"),   # => relativo a ?
#         ("ii,7", "Bb"),  # => "C:min7"?
#     ]

#     for roman, key_name in examples:
#         label = roman_to_chord_label(roman, key_name)
#         print(f"roman_to_chord_label({roman}, {key_name}) => {label}")

def test_roman_to_chord():
    examples = [
        ("I", "C"),        # C:maj
        ("ii,7", "C"),     # D:min7
        ("V,maj7", "D"),   # A:maj7
        ("i,hdim7", "Am"), # A:hdim7
        ("iii,minmaj7", "C"), # E:minmaj7
        ("vi,sus2", "Bb"), # G:sus2
        ("V,sus4", "A"),   # E:sus4
        ("ii,dim", "F"),   # G:dim
        ("IV,aug", "Eb"),  # Ab:aug
        ("vi,maj6", "D"),  # B:maj6
        ("i,min6", "Em"),  # E:min6
    ]

    for roman, key_name in examples:
        label = roman_to_chord_label(roman, key_name)
        print(f"roman_to_chord_label({roman}, {key_name}) => {label}")


if __name__ == "__main__":

    test_roman_to_chord()

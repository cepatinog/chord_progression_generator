#!/usr/bin/env python

"""
Módulo: roman_to_chord
----------------------
Provee funciones para mapear un numeral romano (I, ii, V7, etc.)
a una etiqueta de acorde compatible con JAMS (p.ej. 'C:maj7', 'D:min7', 'G:7'),
según una tonalidad mayor básica.
"""

# Diccionario de notas en semitonos (C = 0, C# = 1, D = 2, ...)
# Aquí se asume una sola forma de nomenclatura #. Podrías expandirlo si necesitas bemoles.
NOTE_TO_INT = {
    "C": 0,  "C#": 1,  "D": 2,  "D#": 3,  "E": 4,  "F": 5,
    "F#": 6, "G": 7,  "G#": 8,  "A": 9,  "A#": 10, "B": 11
}

# Si deseas permitir notación bemol, puedes duplicar con alias:
# NOTE_TO_INT["Db"] = 1
# NOTE_TO_INT["Eb"] = 3
# ...

# Inversa para volver de semitonos a nota con sostenido
INT_TO_NOTE = {v: k for k, v in NOTE_TO_INT.items()}

# Escala mayor en semitonos: I=0, II=2, III=4, IV=5, V=7, VI=9, VII=11
MAJOR_SCALE_INTERVALS = [0, 2, 4, 5, 7, 9, 11]

def roman_to_chord_label(roman: str, key: str = "C") -> str:
    """
    Convierte un numeral romano (por ej. 'I', 'ii', 'V', 'vii', etc.)
    a una etiqueta de acorde JAMS (por ej. 'C:maj7', 'D:min7', 'G:7'),
    asumiendo una tonalidad mayor simplificada.

    Ejemplos de uso:
        roman_to_chord_label("I", "C")   -> "C:maj"
        roman_to_chord_label("V7", "F")  -> "C:7"
        roman_to_chord_label("ii", "G")  -> "A:min"
    
    Notas:
    - Por simplicidad, asumimos que la tonalidad es mayor
      y que las extensiones de séptima siguen la costumbre jazz (dominantes en V).
    - No se manejan alteraciones (#, b) en el numeral. 
    - El mapeo a "maj7", "min7", etc. es limitado y demostrativo.
    """

    # 1) Determinar índice en la escala mayor: I=0, II=1, III=2, IV=3, V=4, VI=5, VII=6
    #    - uppercase => mayor, lowercase => menor
    #    - chequeo si hay '7'
    #    - etc.
    roman_clean = roman.strip()  # p.ej. "V7"
    
    # Extraemos cualquier sufijo (p.ej. '7', 'maj7') que el usuario ponga en el numeral
    # y definimos la triada base y su séptima si procede.
    # Ej: "V7" => base "V" + '7'
    #     "ii" => base "ii", sin sufijo
    # Nota: Este parse es *muy* simplificado.
    suffix = ""
    for possible_suffix in ["7", "maj7", "min7"]:  
        # Podrías ampliarlo con "dim7", "hdim7", "9", "11", etc.
        if roman_clean.endswith(possible_suffix):
            suffix = possible_suffix
            roman_clean = roman_clean.replace(possible_suffix, "")
            break

    # Para indexar la escala:
    # I -> 0, II -> 1, III -> 2, IV -> 3, V -> 4, VI -> 5, VII -> 6
    # i -> 0, ii -> 1, iii -> 2, ...
    base_roman = roman_clean.lower()  # "i", "v", etc.
    roman_map = {"i":0, "ii":1, "iii":2, "iv":3, "v":4, "vi":5, "vii":6}
    if base_roman not in roman_map:
        # Caso no contemplado -> fallback
        return "C:maj"

    scale_index = roman_map[base_roman]

    # 2) Hallar la nota en semitonos que corresponde
    #    a la fundamental del acorde en la tonalidad "key"
    key = key.strip()
    if key not in NOTE_TO_INT:
        # fallback a C si el user da un key no reconocido
        root_key_int = 0
    else:
        root_key_int = NOTE_TO_INT[key]
    
    # El offset en la escala mayor:
    offset = MAJOR_SCALE_INTERVALS[scale_index]
    chord_root_int = (root_key_int + offset) % 12

    # 3) Determinar si es mayor o menor 
    #    - uppercase roman => mayor
    #    - lowercase roman => menor
    # Chequeamos la original 'roman' para ver si era upper/lower
    # EJ: "ii" => minor, "V" => major
    is_major = roman[0].isupper()

    # 4) Construir la etiqueta de triada
    # JAMS requiere p.ej. "D:maj" o "A:min"
    note_name = INT_TO_NOTE[chord_root_int]  # p.ej. 2 => 'D'
    if is_major:
        base_qual = "maj"
    else:
        base_qual = "min"

    chord_label = f"{note_name}:{base_qual}"  # "D:maj" o "A:min"

    # 5) Manejo del sufijo (p.ej. "7", "maj7", etc.)
    #    - Este paso es *demostrativo*. Podrías mapear 
    #      "V7" => "G:7", 
    #      "Imaj7" => "C:maj7", etc.
    if suffix == "7":
        # Si is_major => "C:7", si no => "D:min7"
        # Nota: en jazz, V7 se asume "dominante".
        # Si la base era menor + '7', se asume "min7".
        if is_major:
            chord_label = f"{note_name}:7"
        else:
            chord_label = f"{note_name}:min7"
    elif suffix == "maj7":
        chord_label = f"{note_name}:maj7"
    elif suffix == "min7":
        chord_label = f"{note_name}:min7"

    return chord_label


def test_roman_to_chord():
    """
    Pequeña rutina de pruebas manuales.
    """
    examples = [
        ("I", "C"),
        ("Imaj7", "C"),
        ("ii", "C"),
        ("ii7", "C"),
        ("V", "C"),
        ("V7", "C"),
        ("vi", "C"),
        ("iii", "G"),
        ("VII", "D"),  # D => [0,2,4,5,7,9,11] => VII => offset=11 => C#:maj
    ]

    for roman, key in examples:
        label = roman_to_chord_label(roman, key)
        print(f"roman_to_chord_label({roman}, {key}) => {label}")

if __name__ == "__main__":
    test_roman_to_chord()

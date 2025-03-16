import json
from .config import JAMS_DIR

def create_jams(chord_labels, jams_name):
    """
    Crea un archivo JAMS con anotaciones de acordes.
    :param chord_labels: lista de strings (acordes)
    :param jams_name: nombre del archivo .jams
    """
    jam_data = {
        "chord": []
    }

    # Supongamos que cada acorde dura 2 segundos
    start_time = 0
    for chord in chord_labels:
        jam_data["chord"].append({
            "start": start_time,
            "end": start_time + 2,
            "label": chord
        })
        start_time += 2

    JAMS_DIR.mkdir(parents=True, exist_ok=True)
    output_jams = JAMS_DIR / jams_name

    with open(output_jams, 'w') as f:
        json.dump(jam_data, f, indent=4)

    return output_jams

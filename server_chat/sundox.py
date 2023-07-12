import json
from channels.generic.websocket import AsyncWebsocketConsumer
import subprocess


def string_to_dictlist(chaine):
    chaine = chaine.strip()
    dicts = []
    decoder = json.JSONDecoder()
    while chaine:
        dict_, idx = decoder.raw_decode(chaine)
        dicts.append(dict_)
        chaine = chaine[idx:].strip()
    #print(dicts)
    return dicts


def run_in_sandbox(file, inputs):
    res = []

    # Vérifie si l'image Docker existe
    check_image = subprocess.run(['docker', 'images', '-q', 'python-sandbox'])
    
    # Si l'image Docker n'existe pas, la construit
    if check_image.returncode != 0:
        build_process = subprocess.Popen(["docker", "build", "-t", "python-sandbox", "."], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = build_process.communicate()

        if build_process.returncode != 0:
            print(f"Erreur lors de la construction de Docker: {stderr.decode()}")
            return

    # Prépare toutes les données à envoyer
    json_inputs = '\n'.join(json.dumps(input_data) for input_data in inputs) + '\n'

    # Exécute le script Python dans un nouveau conteneur Docker
    run_process = subprocess.Popen(["docker", "run", "-i", "python-sandbox", "python3", file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = run_process.communicate(input=json_inputs.encode())
    res = string_to_dictlist(stdout.decode())
    if run_process.returncode != 0:
        print(f"Erreur lors de l'exécution de Docker: {stderr.decode()}")
    else:
        print("victoire")

    return res
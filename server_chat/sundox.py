import json
from channels.generic.websocket import AsyncWebsocketConsumer
import subprocess


def run_in_sandbox(file, input_data):
    # Construit l'image Docker
    build_process = subprocess.Popen(["docker", "build", "-t", "python-sandbox", "."], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = build_process.communicate()

    if build_process.returncode != 0:
        print(f"Erreur lors de la construction de Docker: {stderr.decode()}")
        return

    # Encode la donnée en JSON
    json_input = json.dumps(input_data) + "\n"

    # Exécute le script Python dans un nouveau conteneur Docker
    run_process = subprocess.Popen(["docker", "run", "-i", "python-sandbox", "python3", file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = run_process.communicate(input=json_input.encode())
    print(f"Sortie de morpion.py:\n{stdout.decode()}")

    res = stdout.decode()

    if run_process.returncode != 0:
        print(f"Erreur lors de l'exécution de Docker: {stderr.decode()}")
    else:
        # Afficher la sortie standard de morpion.py
        print(f"Sortie de morpion.py:\n{stdout.decode()}")

    return res
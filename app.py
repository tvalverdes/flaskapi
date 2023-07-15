from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from appfolder.getMeta import *
from appfolder.pln_svc import *
from appfolder.modelo_metadata import *
from appfolder.obtenerMetadata import *
import threading

app = Flask(__name__)
CORS(app)

# Variable de bloqueo
lock = threading.Lock()

@app.route("/")
def index():
    return jsonify({"message": "Estás usando la API de análisis de metadata y PLN de la tesis"})

@app.route("/url/<path:url>")
def analisis(url):
    respuesta = []
    if lock.locked():
        print("El análisis ya está en progreso")

    with lock:
        respuestaMeta = analisis_modelo(url)
        respuestaPLN = analisis_pln(url)

        print("Respuesta META: ", respuestaMeta)
        print("Respuesta PLN: ", respuestaPLN)
        print("Respuesta URL: ", url)

        respuesta.append(respuestaMeta)
        respuesta.append(respuestaPLN)
        respuesta.append({"url": url})
        print(respuesta)
        return jsonify(respuesta)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")

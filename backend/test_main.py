import mongomock
import pytest

from pymongo import MongoClient
from fastapi import FastAPI
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)
fake_mongo_client = mongomock.MongoClient()
fake_database = fake_mongo_client.practica1
fake_collection_historial = fake_database.historial

@pytest.mark.parametrize(
    "numeroA, numeroB, resultado",
    [
        (5, 10, 15),
        (0, 0, 0),
        (-5, 5, 0),
        (-10, -5, -15),
        (10, -20, -10)
    ]
)
def test_sumar(monkeypatch, numeroA, numeroB, resultado):
    monkeypatch.setattr(main, "collection_historial", fake_collection_historial)
    
    response = client.get(f"/calculadora/sum?a={numeroA}&b={numeroB}")
    assert response.status_code == 200
    assert response.json() == {"a": numeroA, "b": numeroB, "resultado": resultado}

    assert fake_collection_historial.find_one({"resultado": resultado, "a": numeroA, "b": numeroB}) is not None



def test_historial(monkeypatch):
    monkeypatch.setattr(main, "collection_historial", fake_collection_historial)

    response = client.get("/calculadora/historial")
    assert response.status_code == 200

    # Obtenemos todos los documentos que ya fueron insertados por los tests de /sum
    expected_data = list(fake_collection_historial.find({}))

    historial = []
    for document in expected_data:
        historial.append({
            "a": document["a"],
            "b": document["b"],
            "resultado": document["resultado"],
            "date": document["date"].isoformat()
        })

    # Comparamos que la respuesta sea exactamente lo que hay en la colección
    assert response.json() == {"historial": historial}


@pytest.mark.parametrize(
    "numeroA, numeroB, resultado",
    [
        (4, 2, 2),
        (16, 4, 4),
    ]
)
def test_dividir(monkeypatch, numeroA, numeroB, resultado):
    monkeypatch.setattr(main, "collection_historial", fake_collection_historial)

    response = client.get(f"/calculadora/dividir?dividendo={numeroA}&divisor={numeroB}")
    assert response.status_code == 200
    assert response.json() == {"a": numeroA, "b": numeroB, "resultado": resultado}


@pytest.mark.parametrize(
    "numeroA, numeroB, resultado",
    [
        (4, 0, 2),
        (16, -4, 4),
    ]
)
def test_dividir_error_msg(monkeypatch, numeroA, numeroB, resultado):
    monkeypatch.setattr(main, "collection_historial", fake_collection_historial)

    response = client.get(f"/calculadora/dividir?dividendo={numeroA}&divisor={numeroB}")
    assert response.status_code == 200
    if numeroB < 0:
        assert response.json() == {"error": "No se puede dividir entre numeros negativos."}
    if numeroB == 0:
        assert response.json() == {"error": "No se puede dividir entre cero."}

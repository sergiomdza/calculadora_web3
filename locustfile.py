from locust import HttpUser, task, between
import random

class CalculatorUser(HttpUser):
    # Cuanto tiempo esperar entre tareas
    wait_time = between(1, 2)

    @task
    def sumar(self):
        a = random.randint(-100, 1000)
        b = random.randint(-100, 1000)
        self.client.get(f"/calculadora/sum?a={a}&b={b}")

    @task
    def dividir(self):
        a = random.randint(-100, 1000)
        b = random.randint(-100, 1000)
        self.client.get(f"/calculadora/dividir?dividendo={a}&divisor={b}")

    @task
    def get_historial(self):
        self.client.get("/calculadora/historial")
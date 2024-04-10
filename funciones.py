import time
from typing import List, Any

import numpy as np


class GeneradorAleatorio:

    def __init__(self, seed=0):
        self.seed = seed
        np.random.seed(self.seed)

    def generar_numeros_uniformes(self, a, b, n) -> list:
        return [round(self.generar_uniforme(a, b), 4) for _ in range(n)]

    def generar_numeros_exponenciales(self, media, n) -> list:
        return [self.generar_exponencial_negativa(media) for _ in range(n)]

    def generar_uniforme(self, a, b) -> float:
        rnd = np.random.rand()
        return rnd * (b - a) + a

    def generar_exponencial_negativa(self, media) -> float:
        rnd = np.random.rand()
        lam = 1 / media
        num = - (1.0 / lam) * np.log(1 - rnd)
        return round(num, 4)

    def generar_normales(self, media, desviacion, n) -> list:
        datos = []
        while len(datos) < n:
            u1 = self.generar_uniforme(0, 1)
            u2 = self.generar_uniforme(0, 1)
            # Evitar que u1 sea 0 o 1 ya que el logaritmo de 0 no está definido y la raiz de un número negativo tampoco
            if u1 == 0:
                u1 = 0.0001
            n1 = round(((np.sqrt(-2 * np.log(u1))) * np.cos(2 * np.pi * u2)) * desviacion + media, 4)
            n2 = round(((np.sqrt(-2 * np.log(u1))) * np.sin(2 * np.pi * u2)) * desviacion + media, 4)
            datos.append(n1)
            datos.append(n2)

        if n % 2 != 0:
            return datos[:-1]  # Si la cantidad de datos es impar, se elimina el último elemento
        return datos


if __name__ == "__main__":
    generador = GeneradorAleatorio(seed=0)
    print(generador.generar_normales(1, 1, 200000))




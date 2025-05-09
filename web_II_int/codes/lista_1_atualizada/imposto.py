from abc import ABC, abstractmethod


class Imposto(ABC):

    @abstractmethod
    def calcular_imposto(self):
        pass

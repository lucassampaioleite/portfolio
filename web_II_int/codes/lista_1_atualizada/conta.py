from abc import ABC, abstractmethod


class Conta(ABC):
    def __init__(self, titular, saldo=0.0):
        self._titular = titular
        self._saldo = saldo

    @property
    def saldo(self):
        return self._saldo

    @property
    def titular(self):
        return self._titular

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(
                f"[{self._titular.nome}] Depósito de R$ {valor:.2f} realizado. Novo saldo: R$ {self._saldo:.2f}")
        else:
            print(f"[{self._titular.nome}] Valor de depósito inválido.")

    @abstractmethod
    def sacar(self, valor):
        pass

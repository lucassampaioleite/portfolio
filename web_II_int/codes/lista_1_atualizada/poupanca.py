from conta import Conta
from imposto import Imposto


class Poupanca(Conta, Imposto):
    def sacar(self, valor):
        if valor <= self._saldo:
            self._saldo -= valor
            print(
                f"[{self._titular.nome}] Saque de R$ {valor:.2f} realizado. Novo saldo: R$ {self._saldo:.2f}")
        else:
            print(
                f"[{self._titular.nome}] Saldo insuficiente para saque de R$ {valor:.2f}.")

    def render_juros(self):
        rendimento = self.saldo * 0.005
        self._saldo += rendimento
        print(
            f"[{self._titular.nome}] Rendimento de R$ {rendimento:.2f} aplicado. Novo saldo: R$ {self._saldo:.2f}")

    def calcular_imposto(self):
        imposto = self._saldo * 0.003
        self._saldo -= imposto
        print(
            f"[{self._titular.nome}] Imposto de R$ {imposto:.2f} debitado. Novo saldo: R$ {self._saldo:.2f}")

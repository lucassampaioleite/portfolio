from conta import Conta
from imposto import Imposto


class ContaCorrente(Conta, Imposto):

    def sacar(self, valor):
        TAXA_SAQUE = 2.00
        total = valor + TAXA_SAQUE
        if total <= self._saldo:
            self._saldo -= total
            print(
                f"[{self._titular.nome}] Saque de R$ {valor:.2f} + taxa de R$ {TAXA_SAQUE:.2f} realizado. Novo saldo: R$ {self._saldo:.2f}")
        else:
            print(
                f"[{self._titular.nome}] Saldo insuficiente para saque com taxa (R$ {total:.2f}).")

    def calcular_imposto(self):
        imposto = self._saldo * 0.005
        self._saldo -= imposto
        print(
            f"[{self._titular.nome}] Imposto de R$ {imposto:.2f} debitado. Novo saldo: R$ {self._saldo:.2f}")

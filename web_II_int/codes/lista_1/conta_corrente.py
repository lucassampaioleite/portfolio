from conta import Conta


class ContaCorrente(Conta):

    def sacar(self, valor):
        TAXA_SAQUE = 2.00
        total = valor + TAXA_SAQUE
        if total <= self.saldo:
            self.saldo -= total
            print(
                f"[{self.titular.nome}] Saque de R$ {valor:.2f} + taxa de R$ {TAXA_SAQUE:.2f} realizado. Novo saldo: R$ {self.saldo:.2f}")
        else:
            print(
                f"[{self.titular.nome}] Saldo insuficiente para saque com taxa (R$ {total:.2f}).")

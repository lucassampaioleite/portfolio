class Conta:
    def __init__(self, titular, saldo=0.0):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print(
                f"[{self.titular.nome}] Depósito de R$ {valor:.2f} realizado. Novo saldo: R$ {self.saldo:.2f}")
        else:
            print(f"[{self.titular.nome}] Valor de depósito inválido.")

    def sacar(self, valor):
        if valor > 0:
            self.saldo -= valor
            print(
                f"[{self.titular.nome}] Saque de R$ {valor:.2f} realizado. Novo saldo: R$ {self.saldo:.2f}")
        else:
            print(f"[{self.titular.nome}] Valor de saque inválido.")

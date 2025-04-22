from conta import Conta


class Poupanca(Conta):
    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            print(
                f"[{self.titular.nome}] Saque de R$ {valor:.2f} realizado. Novo saldo: R$ {self.saldo:.2f}")
        else:
            print(
                f"[{self.titular.nome}] Saldo insuficiente para saque de R$ {valor:.2f}.")

    def render_juros(self):
        rendimento = self.saldo * 0.005
        self.saldo += rendimento
        print(
            f"[{self.titular.nome}] Rendimento de R$ {rendimento:.2f} aplicado. Novo saldo: R$ {self.saldo:.2f}")

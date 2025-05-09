class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self._cpf = cpf
        self._contas = []

    @property
    def cpf(self):
        return self._cpf

    @property
    def contas(self):
        return self._contas

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def saldo_total(self):
        return f"{sum(conta.saldo for conta in self._contas):.2f}"

    def exibir_contas(self):
        print(f"Contas de {self.nome}:")
        for conta in self._contas:
            tipo = conta.__class__.__name__
            print(f" - {tipo}: R$ {conta.saldo:.2f}")

class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def saldo_total(self):
        return f"{sum(conta.saldo for conta in self.contas): .2f}"

    def exibir_contas(self):
        print(f"Contas de {self.nome}:")
        for conta in self.contas:
            tipo = conta.__class__.__name__
            print(f" - {tipo}: R$ {conta.saldo:.2f}")

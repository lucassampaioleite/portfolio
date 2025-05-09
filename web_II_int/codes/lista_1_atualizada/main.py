from conta_corrente import ContaCorrente
from poupanca import Poupanca
from cliente import Cliente

if __name__ == "__main__":

    cliente1 = Cliente("Lucas", "00000000000")

    conta1 = ContaCorrente(cliente1, 100)
    conta2 = Poupanca(cliente1,  200)

    cliente1.adicionar_conta(conta1)
    cliente1.adicionar_conta(conta2)

    cliente1.exibir_contas()
    print(cliente1.saldo_total())

    conta1.depositar(50)
    conta1.sacar(120)
    conta1.sacar(100)

    conta2.sacar(50)
    conta2.render_juros()
    conta2.sacar(200)

    cliente1.exibir_contas()
    print(cliente1.saldo_total())

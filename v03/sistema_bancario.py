from datetime import datetime
import textwrap
from abc import ABC, abstractmethod


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def __str__(self):
        return f'{self.nome} - CPF: {self.cpf} - Nasc.: {self.data_nascimento} - Endereço: {self.endereco}'


class Conta:
    def __init__(self, numero, cliente, agencia='0001'):
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._saldo = 0
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        if valor > self.saldo:
            print('Operação falhou. Saldo insuficiente')
            return False
        if valor <= 0:
            print('Operação falhou. Valor inválido')
            return False
        self._saldo -= valor
        print('Saque realizado com sucesso')
        return True

    def depositar(self, valor):
        if valor <= 0:
            print('Operação falhou. Valor inválido')
            return False
        else:
            self._saldo += valor
            print('Depósito realizado com sucesso')
            return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_valor_saque=500, limite_quantidade_saques=3):
        super().__init__(numero, cliente)
        self.limite_valor_saque = limite_valor_saque
        self.limite_quantidade_saques = limite_quantidade_saques
    
    def sacar(self, valor):
        quantidade_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
        )
        excedeu_quantidade_saque = quantidade_saques >= self.limite_quantidade_saques
        excedeu_valor_saque = valor > self.limite_valor_saque
        if excedeu_quantidade_saque:
            print('Operação falhou. Quantidade limite de saques excedida')
            return False
        elif excedeu_valor_saque:
            print('Operação falhou. Valor limite de saque excedido')
            return False
        else:
            return super().sacar(valor)

    def __str__(self):
        return f'Agência: {self.agencia}. C/C: {self.numero}. Titular: {self.cliente.nome}'


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        return self._transacoes.append(
            {
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass   

    @abstractmethod
    def registrar(self,conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor

    def registrar(self,conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor

    def registrar(self,conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = '''
    =================== MENU ===================
    [1]\tDepósito\t[5]\tNova conta
    [2]\tSaque\t\t[6]\tListar clientes
    [3]\tExtrato\t\t[7]\tListar contas
    [4]\tNovo cliente\t[0]\tSair
    ============================================
    '''
    return input(textwrap.dedent(menu))


def depositar(clientes):
    cpf = input('Informe o CPF: ').strip()
    cliente = consultar_cliente(cpf, clientes)
    if not cliente:
        print('Cliente não encontrado')
        return
    valor = float(input('Informe o valor: '))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)


def consultar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Cliente não possui conta')
        return
    return cliente.contas[0]
    

def realizar_transacao():
    pass


def sacar(clientes):
    cpf = input('Informe o CPF: ').strip()
    cliente = consultar_cliente(cpf, clientes)
    if not cliente:
        print('Cliente não encontrado')
        return
    valor = float(input('Informe o valor: '))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cpf = input('Informe o CPF: ').strip()
    cliente = consultar_cliente(cpf, clientes)
    if not cliente:
        print('Cliente não encontrado')
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print('==================== EXTRATO ====================')
    transacoes = conta.historico.transacoes
    extrato = ''
    if not transacoes:
        extrato = 'Não foram realizadas transações'
    else:
        for transacao in transacoes:
            extrato += f"{transacao['data']}\t{transacao['tipo']}\t{transacao['valor']:.2f}\n"
    print(extrato)
    print(f"{agora}\tSaldo\tR$ {conta.saldo:.2f}")
    print('=================================================')


def criar_cliente(clientes):
    cpf = input('Informe o CPF: ').strip()
    cliente = consultar_cliente(cpf, clientes)
    if cliente:
        print('Cliente já cadastrado')
        return
    nome = input('Nome: ').strip()
    data_nascimento = input('Data de nascimento: ').strip()
    endereco = input('Endereço: ').strip()
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print('Cliente cadastrado com sucesso')


def listar_clientes(clientes):
    if clientes:
        for cliente in clientes:
            print(textwrap.dedent(str(cliente)))
    else:
        print('Não foram encontrados clientes')


def criar_conta(numero_conta, clientes, contas):
    cpf = input('Informe o CPF: ').strip()
    cliente = consultar_cliente(cpf, clientes)
    if not cliente:
        print('Cliente não encontrado')
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print('Conta criada com sucesso')


def listar_contas(contas):
    if contas:
        for conta in contas:
            print(textwrap.dedent(str(conta)))
    else:
        print('Não foram encontradas contas')


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu().strip()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)
            
        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            listar_clientes(clientes)

        elif opcao == "7":
            listar_contas(contas)

        elif opcao == "0":
            print('Saindo...')
            break


main()
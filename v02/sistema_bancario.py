from datetime import datetime
import textwrap

def deposito(saldo, extrato, /):
    valor = input('Quanto deseja depositar?\n').strip()

    try:
        valor = float(valor)

        if valor > 0:
            saldo += valor
            agora = datetime.now().strftime("%d/%m/%Y %H:%M")
            extrato += f'{agora}\tDepósito\tR$ {valor:.2f}\n'
            print(f'Depósito de R$ {valor:.2f} realizado com sucesso')
        else:
            print('Valor inválido. Digite um número maior que zero.')

    except ValueError:
        print('Digite um valor válido.')

    return saldo, extrato

def sacar(*, valor_saque, saldo, extrato):
   
    valor = input('Quanto deseja sacar?\n').strip()

    try:
        valor = float(valor)

        if valor > valor_saque:
            print(f'Não é possível sacar mais que R$ {valor_saque:.2f} por saque.')

        elif valor > saldo:
            print(f'Você tentou sacar R$ {valor:.2f}, mas possui R$ {saldo:.2f}.')

        elif valor <= 0:
            print('Digite um valor positivo.')

        else:
            saldo -= valor
            agora = datetime.now().strftime("%d/%m/%Y %H:%M")
            extrato += f'{agora}\tSaque\t\tR$ {valor:.2f}\n'
            print(f'Saque de R$ {valor:.2f} realizado com sucesso')

    except ValueError:
        print('Digite um valor válido.')

    return saldo, extrato


def mostrar_extrato(horario_inicial, saldo_inicial, saldo, /, *, extrato):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    print('==================== EXTRATO ====================')
    print(f'{horario_inicial}\tSaldo inicial\tR$ {saldo_inicial:.2f}')
    print(extrato.rstrip('\n') if extrato else 'Não foram realizadas operações.')
    print(f'{agora}\tSaldo final\tR$ {saldo:.2f}')
    print('=================================================')

def novo_usuario(usuarios):
    cpf = input('CPF: ').strip()
    usuario_encontrado = consultar_usuario(cpf, usuarios)
    if usuario_encontrado:
        print('CPF já está em uso')
        return usuarios

    nome = input('Nome: ').strip()
    data_nascimento = input('Data de nascimento: ').strip()
    endereco = input('Endereço: ').strip()
    usuario = {"nome":nome, "data_nascimento":data_nascimento,"cpf":cpf,"endereco":endereco}
    usuarios.append(usuario)
    return usuarios

def nova_conta(contas, usuarios, AGENCIA):
    cpf = input('CPF: ').strip()
    usuario_encontrado = consultar_usuario(cpf, usuarios)
    if usuario_encontrado: 
        conta_existente = [conta["numero_conta"] for conta in contas]
        numero_conta = max(conta_existente, default=0) + 1
        conta = {"agencia":AGENCIA, "numero_conta":numero_conta, "usuario":usuario_encontrado}
        contas.append(conta)
        print(f'Conta criada com sucesso!')
        return contas

    print('Usuário não encontrado')
    return contas

def consultar_usuario(cpf, usuarios):
    for consultar_usuario in usuarios:
        if consultar_usuario["cpf"] == cpf:
            return consultar_usuario
    return None

def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        for usuario in usuarios:
            print(f"Nome: {usuario['nome']}, CPF: {usuario['cpf']}, Data de Nascimento: {usuario['data_nascimento']}, Endereço: {usuario['endereco']}")

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Nome: {conta['usuario']['nome']}, CPF: {conta['usuario']['cpf']}")

menu = '''
    =================== MENU ===================
    [1]\tDepósito\t[5]\tNova conta
    [2]\tSaque\t\t[6]\tListar usuários
    [3]\tExtrato\t\t[7]\tListar contas
    [4]\tNovo usuário\t[0]\tSair
    ============================================
    '''
saldo = 0
saldo_inicial = saldo
horario_inicial = datetime.now().strftime("%d/%m/%Y %H:%M")
valor_saque = 500
limite_saque = 3
quantidade_saque = 0
extrato = ''
limite_transacoes = 10
quantidade_transacoes = 0
usuarios = []
contas = []
AGENCIA = '0001'

while True:

    opcao = input(textwrap.dedent(menu)).strip()

    if not opcao.isdigit():
        print('Escolha uma opção válida.')
        continue

    opcao = int(opcao)

    if opcao == 1:
        if limite_transacoes > quantidade_transacoes:
            saldo, extrato = deposito(saldo, extrato)
            quantidade_transacoes += 1
        else:
            print(f'Você realisou {limite_transacoes} transações e atingiu o limite diário')

    elif opcao == 2:
        if quantidade_saque >= limite_saque:
            print(f'Você alcançou o limite de {limite_saque} saques hoje.')
        else:
            if limite_transacoes > quantidade_transacoes:
                saldo, extrato,  = sacar(valor_saque=valor_saque, saldo=saldo, extrato=extrato)
                quantidade_transacoes += 1
                quantidade_saque += 1
            else:
                print(f'Você realisou {limite_transacoes} transações e atingiu o limite diário')

    elif opcao == 3:
        mostrar_extrato(horario_inicial, saldo_inicial, saldo, extrato=extrato)

    elif opcao == 4:
        usuarios = novo_usuario(usuarios)

    elif opcao == 5:
        contas = nova_conta(contas, usuarios, AGENCIA)

    elif opcao == 6:
        lista_usuarios = listar_usuarios(usuarios)

    elif opcao == 7:
        lista_contas = listar_contas(contas)

    elif opcao == 0:
        print('Saindo...')
        break

    else:
        print('Escolha uma opção válida.')
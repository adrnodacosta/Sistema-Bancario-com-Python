menu = '''
------------------- MENU -------------------
           Escolha uma operação:           
[1] Depósito [2] Saque [3] Extrato [0] Sair
--------------------------------------------

'''

saldo = 0
saldo_inicial = saldo
valor_saque = 500
limite_saque = 3
quantidade_saque = 0
extrato = ''

while True:

    opcao = input(menu).strip()

    nao_inteiro = not opcao.isdigit()

    if nao_inteiro:
        print('Escolha uma opção válida')

    else:

        opcao = int(opcao)

        if opcao == 1:
            deposito = input('Quanto deseja depositar?\n')

            nao_inteiro = not deposito.isdigit()

            if nao_inteiro:
                print('Digite um valor válido')

            else:

                deposito = int(deposito)

                if deposito > 0:
                    saldo += deposito
                    extrato += f'Você depositou R$ {deposito:.2f}\n'
                    print(f'Você depositou R$ {deposito:.2f}. Seu saldo é R$ {saldo:.2f}')

                else:
                    print(f'Não é possível depositar R$ {deposito:.2f}. Tente outro valor!')

        elif opcao == 2:
            
            excedeu_limite_saque = quantidade_saque >= limite_saque

            if excedeu_limite_saque:
                print(f'Você alcançou o limite de {quantidade_saque} saques hoje')
            
            else:
                saque = input('Quanto deseja sacar?\n')

                nao_inteiro = not saque.isdigit()

                if nao_inteiro:
                    print('Digite um valor válido')

                else:
                    saque = int(saque)

                    excedeu_valor_saque = saque > valor_saque

                    if excedeu_valor_saque:

                        print(f'Não é possível sacar mais que R$ {valor_saque:.2f} por saque. Tente outro valor!')

                    else:

                        excedeu_saldo = saque > saldo

                        if excedeu_saldo:

                            print(f'Você tentou sacar R$ {saque:.2f}, mas possui R$ {saldo:.2f}. Tente outro valor!')

                        else:

                            saldo -= saque
                            quantidade_saque += 1
                            extrato += f'Você sacou R$ {saque:.2f}\n'
                            print(f'Você sacou R$ {saque:.2f}. Seu novo saldo é R$ {saldo:.2f}')
                
       
        elif opcao == 3:
            print('-------- EXTRATO --------\n')
            print(f'Seu saldo inicial é R$ {saldo_inicial:.2f}\n')
            print('Não foram realizadas operações\n' if not extrato else extrato)
            print(f'Seu saldo final é R$ {saldo:.2f}\n')
            print('-------------------------\n')
       
        elif opcao == 0:
            break
       
        else:
            print('Escolha uma opção válida')
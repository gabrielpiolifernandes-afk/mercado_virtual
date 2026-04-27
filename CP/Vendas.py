from Cliente import Cadastro,Leitura_de_dados
import json
import os

arquivo = "NotaFiscal.json"

def Comprar():
    while True:
        try:
            user_id = int(input("Qual é seu ID? "))

            clientes_existentes = Leitura_de_dados()
            ids_existentes = [c['id'] for c in clientes_existentes]

            if user_id not in ids_existentes:
                print("ID não encontrado! Digite um ID já cadastrado.")
            else:
                print("ID encontrado. Prosseguindo com a compra...")
                break

        except ValueError:
            print("Digite um número válido para o ID.")
    print(input(Forma_de_pagamento))#tem erro aqui
                                      
def Forma_de_pagamento(valor_compra):
    print("Formas de pagamento disponíveis:")
    print("1. Cartão de crédito")
    print("2. Débito")
    print("3. Pix")

    escolha = input("Escolha a forma de pagamento (1, 2 ou 3): ")

    if escolha == "1":
        while True:
            try:
                parcelas = int(input("Quantas parcelas? (1 a 3 sem juros / até 12 com juros): "))

                if 1 <= parcelas <= 3:
                    total = valor_compra
                    valor_parcela = total / parcelas

                    print(f"Total: R${total:.2f}")
                    print(f"{parcelas}x de R${valor_parcela:.2f} sem juros")

                    return f"Cartão de crédito {parcelas}x sem juros"

                elif 4 <= parcelas <= 12:
                    #conta de juros compostos: M=P×(1+i)°n
                    juros = 0.05
                    total = valor_compra * (1 + juros) ** parcelas
                    valor_parcela = total / parcelas

                    print(f"Total com juros: R${total:.2f}")
                    print(f"{parcelas}x de R${valor_parcela:.2f}")

                    return f"Cartão de crédito {parcelas}x com juros"

                else:
                    print("Digite um número entre 1 e 12.")

            except ValueError:
                print("Digite apenas números.")

    elif escolha == "2":
        print(f"Pagamento no débito: R${valor_compra:.2f}")
        return "Débito"

    elif escolha == "3":
        print(f"Pagamento no Pix: R${valor_compra:.2f}")
        return "Pix"

    else:
        print("Opção inválida.")
        return "Desconhecida"
    
def Nota_fical():
    # Se o arquivo não existir, criamos uma lista vazia
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = []
    else:
        dados = []

    # Adiciona o cliente recém-criado
    dados.append(cliente.__dict__)

    # Salva de volta no JSON
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

#terminal

while True:
    print("\n===== MENU PRINCIPAL =====")
    print("1. Comprar")
    print("2. Sair")
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cliente = Cadastro()  
        Comprar(cliente) 
        print("Compra finalizada!")
    
    elif opcao == "2":
        print("fechando sistema")
        break

    else:
        print("Opção inválida!")




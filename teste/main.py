# from Cadastro_de_produtos import ProdutoEletronico
# from Cliente import Cadastro, Salvar_dados, Leitura_de_dados
# from Vendas import Comprar 
import json

while True:
    print("\n===MENU PRINCIPAL===")
    print("1. Tela de cadastro")
    print("2. - Compra")
    print("3. - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cliente = Cadastro()
        print("Cliente cadastrado com sucesso!")
    
    if opcao == "2":
        compra = Comprar()

    elif opcao == "3":
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida!")
    
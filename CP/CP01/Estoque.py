import json
from Cadastro_de_produtos import ProdutoEletronico

arquivo = "eletronicos.json"

# cria um objeto para usar os métodos
produto_obj = ProdutoEletronico(0, "", 0, 0, "", "", "", False, "")


def adicionar_produto():
    dados = produto_obj.leitura()

    # ID
    while True:
        try:
            id = int(input("ID: "))
            ids_existentes = [c['id'] for c in dados]

            if id in ids_existentes:
                print("ID já cadastrado! Digite outro.")
            else:
                break
        except ValueError:
            print("Digite um número válido.")

    # Nome
    while True:
        nome = input("Nome: ").strip()
        if nome:
            break
        print("Nome não pode ser vazio.")

    # Preço
    while True:
        try:
            preco = float(input("Preço: "))
            if preco >= 0:
                break
            else:
                print("Preço não pode ser negativo.")
        except ValueError:
            print("Digite um número válido.")

    # Estoque
    while True:
        try:
            estoque = int(input("Estoque: "))
            if estoque >= 0:
                break
            else:
                print("Estoque não pode ser negativo.")
        except ValueError:
            print("Digite um número inteiro válido.")

    # Marca
    while True:
        marca = input("Marca: ").strip()
        if marca:
            break
        print("Marca não pode ser vazia.")

    # Fornecedor
    while True:
        fornecedor = input("Fornecedor: ").strip()
        if fornecedor:
            break
        print("Fornecedor não pode ser vazio.")

    # Componente
    while True:
        componente = input("Componente: ").strip()
        if componente:
            break
        print("Componente não pode ser vazio.")

    # Carregável
    while True:
        entrada = input("Carregável (S/N): ").strip().upper()
        if entrada == "S":
            carregavel = True
            break
        elif entrada == "N":
            carregavel = False
            break
        else:
            print("Digite apenas S ou N.")

    # Descrição
    while True:
        descricao = input("Descrição: ").strip()
        if descricao:
            break
        print("Descrição não pode ser vazia.")

    novo_produto = {
        "id": id,
        "nome": nome,
        "preco": preco,
        "estoque": estoque,
        "marca": marca,
        "fornecedor": fornecedor,
        "componente": componente,
        "carregavel": carregavel,
        "descricao": descricao
    }

    dados.append(novo_produto)
    produto_obj.salvar_dados(dados)

    print("Produto adicionado com sucesso!")

    novo_produto = {
        "id": id,
        "nome": nome,
        "preco": preco,
        "estoque": estoque,
        "marca": marca,
        "fornecedor": fornecedor,
        "componente": componente,
        "carregavel": carregavel,
        "descricao": descricao
    }

    dados.append(novo_produto)
    produto_obj.salvar_dados(dados)

    print("Produto adicionado com sucesso!")


def remover_produto():
    dados = produto_obj.leitura()

    id_produto = int(input("ID do produto: "))
    confirmacao = input("Tem certeza? (S/N): ").upper()

    if confirmacao == "S":
        for produto in dados:
            if produto["id"] == id_produto:
                dados.remove(produto)
                produto_obj.salvar_dados(dados)
                print("Removido com sucesso!")
                return
        print("Produto não encontrado.")
    else:
        print("Cancelado.")


def alerta():
    dados = produto_obj.leitura()
    estoque_baixo = False

    for produto in dados:
        if produto["estoque"] < 5:
            print(f"⚠ {produto['nome']} com estoque baixo ({produto['estoque']})")
            estoque_baixo = True

    if not estoque_baixo:
        print("🟢 Estoque ok")


def atualizar_produto():
    dados = produto_obj.leitura()

    id_produto = int(input("ID do produto: "))

    for produto in dados:
        if produto["id"] == id_produto:

            print(f"\nProduto: {produto['nome']}")

            while True:
                print("\n1-Nome 2-Preço 3-Estoque 4-Marca 5-Fornecedor")
                print("6-Componente 7-Carregável 8-Descrição 9-Sair")

                opcao = input("Opção: ")

                if opcao == "1":
                    produto["nome"] = input("Novo nome: ")

                elif opcao == "2":
                    produto["preco"] = float(input("Novo preço: "))

                elif opcao == "3":
                    produto["estoque"] = int(input("Novo estoque: "))

                elif opcao == "4":
                    produto["marca"] = input("Nova marca: ")

                elif opcao == "5":
                    produto["fornecedor"] = input("Novo fornecedor: ")

                elif opcao == "6":
                    produto["componente"] = input("Novo componente: ")

                elif opcao == "7":
                    produto["carregavel"] = input("True/False: ") == "True"

                elif opcao == "8":
                    produto["descricao"] = input("Nova descrição: ")

                elif opcao == "9":
                    produto_obj.salvar_dados(dados)
                    print("Atualizado com sucesso!")
                    return

                else:
                    print("Opção inválida!")

    print("Produto não encontrado.")


# MENU
while True:
    print("\n===== SISTEMA =====")
    print("1 - Listar")
    print("2 - Adicionar")
    print("3 - Remover")
    print("4 - Atualizar")
    print("5 - Sair")

    alerta()

    opcao = input("Escolha: ")

    if opcao == "1":
        produto_obj.listar_produtos()

    elif opcao == "2":
        adicionar_produto()

    elif opcao == "3":
        remover_produto()

    elif opcao == "4":
        atualizar_produto()

    elif opcao == "5":
        break

    else:
        print("Opção inválida!")
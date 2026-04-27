import json

arquivo = "eletronicos.json"

def Leitura():
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados(dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def listar_produtos():
    dados = Leitura()

    print("\nLISTA DE PRODUTOS\n")

    for produto in dados:
        print(
            f"ID: {produto['id']} | Nome: {produto['nome']} | Preço: {produto['preco']} | "
            f"Estoque: {produto['estoque']} | Marca: {produto['marca']} | Fornecedor: {produto['fornecedor']} | "
            f"Componente: {produto['componente']}")

def adicionar_produto():
    dados = Leitura()
    
    while True:
        try:
            id = int(input("ID: "))
            clientes_existentes = Leitura()
            ids_existentes = [c['id'] for c in clientes_existentes]

            if id in ids_existentes:
                print("ID já cadastrado! Digite um ID diferente.")
            else:
                break
        except ValueError:
            print("Digite um número válido para o ID.")

    nome = input("Nome: ")
    preco = float(input("Preço: "))
    estoque = int(input("Estoque: "))
    marca = input("Marca: ")
    fornecedor = input("Fornecedor: ")
    componente = input("Componente: ")
    carregavel = input("Carregável (True/False): ") == "True"
    descricao = input("Descrição: ")

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

    salvar_dados(dados)

    print("Produto adicionado com sucesso!")

def remover_produto():
    
    dados = Leitura()  

    id_produto = int(input("Digite o ID do produto que deseja remover: "))

    id_produto_confirmação = input("Você tem certeza? (S/N): ").strip().upper()

    if id_produto_confirmação == 'S':  
        for produto in dados:
            if produto["id"] == id_produto:
                dados.remove(produto)
                salvar_dados(dados)  
                
                print("Produto removido com sucesso!")
                return  
        print("Produto não encontrado.")
    else:
        print("Remoção cancelada.")

def alerta():
    dados = Leitura()
    estoque_baixo = False

    for produto in dados:
        if produto["estoque"] < 5:
            print(f"Alerta: O produto {produto['nome']} está com estoque baixo ({produto['estoque']} unidades).")
            estoque_baixo = True

    if not estoque_baixo:
        print("🟢Todos os produtos estão com estoque suficiente.🟢")

def atualizar_produto():
    dados = Leitura()

    id_produto = int(input("Digite o ID do produto: "))

    for produto in dados:
        if produto["id"] == id_produto:

            print(f"\nProduto encontrado: {produto['nome']}")

            while True:
                print("\nO que deseja atualizar?")
                print("1 - Nome")
                print("2 - Preço")
                print("3 - Estoque")
                print("4 - Marca")
                print("5 - Fornecedor")
                print("6 - Componente")
                print("7 - Carregável")
                print("8 - Descrição")
                print("9 - Sair")

                opcao = input("Escolha uma opção: ")

                if opcao == "1":
                    print(f"Nome atual: {produto['nome']}")
                    produto["nome"] = input("Novo nome: ")

                elif opcao == "2":
                    print(f"Preço atual: {produto['preco']}")
                    produto["preco"] = float(input("Novo preço: "))

                elif opcao == "3":
                    print(f"Estoque atual: {produto['estoque']}")
                    produto["estoque"] = int(input("Novo estoque: "))

                elif opcao == "4":
                    print(f"Marca atual: {produto['marca']}")
                    produto["marca"] = input("Nova marca: ")

                elif opcao == "5":
                    print(f"Fornecedor atual: {produto['fornecedor']}")
                    produto["fornecedor"] = input("Novo fornecedor: ")

                elif opcao == "6":
                    print(f"Componente atual: {produto['componente']}")
                    produto["componente"] = input("Novo componente: ")

                elif opcao == "7":
                    print(f"Carregável atual: {produto['carregavel']}")
                    produto["carregavel"] = input("Carregável (True/False): ") == "True"

                elif opcao == "8":
                    print(f"Descrição atual: {produto['descricao']}")
                    produto["descricao"] = input("Nova descrição: ")

                elif opcao == "9":
                    salvar_dados(dados)
                    print("Produto atualizado com sucesso!")
                    return

                else:
                    print("Opção inválida!")

            return

    print("Produto não encontrado.")
    
# MENU PRINCIPAL
while True:

    print("\n===== SISTEMA DE PRODUTOS =====")
    print("1 - Listar produtos")
    print("2 - Adicionar produto")
    print("3 - Remover produto")
    print("4 - Atualizar produto")
    print("5 - Sair")
    alerta()

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        listar_produtos()

    elif opcao == "2":
        adicionar_produto()

    elif opcao == "3":
        remover_produto()

    elif opcao == "4":
        atualizar_produto()

    elif opcao == "5":
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida!")
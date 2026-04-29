from Cadastro_de_produtos import ProdutoEletronico

arquivo = "eletronicos.json"

# cria um objeto para usar os métodos
produto_obj = ProdutoEletronico(0, "", 0, 0, "", "", "", False, "")

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

def confirmar_alteracao(produto, campo, novo_valor, label):
    print(f"\n{label}")
    print(f"Atual: {produto[campo]}")
    print(f"Novo : {novo_valor}")

    confirmacao = input("Confirmar alteração? (S/N): ").strip().upper()

    if confirmacao == "S":
        produto[campo] = novo_valor
        print(f"{label} atualizado!")
    else:
        print("Alteração cancelada.")

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
                    confirmar_alteracao(produto, "nome", input("Novo nome: "), "Nome")

                elif opcao == "2":
                    confirmar_alteracao(produto, "preco", float(input("Novo preço: ")), "Preço")

                elif opcao == "3":
                    confirmar_alteracao(produto, "estoque", int(input("Novo estoque: ")), "Estoque")

                elif opcao == "4":
                    confirmar_alteracao(produto, "marca", input("Nova marca: "), "Marca")

                elif opcao == "5":
                    confirmar_alteracao(produto, "fornecedor", input("Novo fornecedor: "), "Fornecedor")

                elif opcao == "6":
                    confirmar_alteracao(produto, "componente", input("Novo componente: "), "Componente")

                elif opcao == "7":
                    confirmar_alteracao(produto, "carregavel", input("True/False: ") == "True", "Carregável")

                elif opcao == "8":
                    confirmar_alteracao(produto, "descricao", input("Nova descrição: "), "Descrição")

                elif opcao == "9":
                    produto_obj.salvar_dados(dados)
                    print("Atualizado com sucesso!")
                    return

                else:
                    print("Opção inválida!")
        
# MENU
def menu_admin_empressa():
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
            produto_obj.adicionar_produto()

        elif opcao == "3":
            remover_produto()

        elif opcao == "4":
            atualizar_produto()

        elif opcao == "5":
            break

        else:
            print("Opção inválida!")

menu_admin_empressa()
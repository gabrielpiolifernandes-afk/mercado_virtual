from Cadastro_de_produtos import ProdutoEletronico
from carrinho import Carrinho
from vendas import Vendas

def main():
    produto_obj = ProdutoEletronico(0, "", 0, 0, "", "", "", False, "")
    carrinho_obj = Carrinho()
    vendas_obj = Vendas(produto_obj, carrinho_obj   )

    while True:
        print("\nMENU DE OPÇÕES")
        print("1. Listar Produtos")
        print("2. Buscar Descrição")
        print("3. Carrinho de Compra")
        print("4. Vendas")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            produto_obj.listar_produtos()

        elif escolha == "2":
            produto_id = int(input("Digite o ID do produto: "))
            print(produto_obj.buscar_descricao(produto_id))

        elif escolha == "3":
            try:
                id = int(input("Digite o ID do produto: "))

                produto = produto_obj.buscar_produto(id)

                if produto:
                    quantidade = int(input("Quantidade: "))
                    print(carrinho_obj.adicionar(produto, quantidade))
                else:
                    print("Produto não encontrado")

            except ValueError:
                print("Entrada inválida")

        elif escolha == "4":
            vendas_obj.confirmar_compra()

        elif escolha == "5":
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida! Tente novamente.")

main()
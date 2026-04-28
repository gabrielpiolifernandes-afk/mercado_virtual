from Cadastro_de_produtos import ProdutoEletronico
from carrinho import Carrinho
from vendas import Vendas

def main():
    produto_obj = ProdutoEletronico(0, "", 0, 0, "", "", "", False, "")
    carrinho_obj = Carrinho()
    vendas_obj = Vendas()

    while True:
        print("\nMENU DE OPÇÕES")
        print("1. Adicionar Produto")
        print("2. Listar Produtos")
        print("3. Buscar Descrição")
        print("4. Carrinho de Compra")
        print("5. Vendas")
        print("6. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            produto_obj.adicionar_produto()
        
        elif escolha == "2":
            produto_obj.listar_produtos()
        
        elif escolha == "3":
            id = int(input("Digite o ID do produto para buscar descrição: "))
            print(produto_obj.buscar_descricao(id))
        
        elif escolha == "4":
            id = int(input("Digite o ID do produto para adicionar ao carrinho: "))
            print(produto_obj.carrinho_de_compra(id))
        
        elif escolha == "5":
            vendas_obj.relatorio(produto_obj.leitura())
        
        elif escolha == "6":
            print("Saindo do programa...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")
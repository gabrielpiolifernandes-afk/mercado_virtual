import json

arquivo = "eletronicos.json"


class Produtos:
    def __init__(self, id, nome, preco, estoque, marca, fornecedor):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
        self.marca = marca
        self.fornecedor = fornecedor


class ProdutoEletronico(Produtos):

    def __init__(self, id, nome, preco, estoque, marca, fornecedor, componente, carregavel, descricao):
        super().__init__(id, nome, preco, estoque, marca, fornecedor)

        self.componente = componente
        self.carregavel = carregavel
        self.descricao = descricao

    def leitura(self):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def salvar_dados(self, dados):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def listar_produtos(self):
        dados = self.leitura()

        print("\nLISTA DE PRODUTOS\n")

        for produto in dados:
            alerta_estoque = ""
            if produto['estoque'] < 5:
                alerta_estoque = "⚠ Últimas peças!"

            print(
                f"ID: {produto['id']} | "
                f"Nome: {produto['nome']} | "
                f"Preço: {produto['preco']} | "
                f"Estoque: {produto['estoque']} {alerta_estoque}"
            )

    def buscar_produto(self, id):
        dados = self.leitura()

        for p in dados:
            if p['id'] == id:
                return p

        return None
    
    
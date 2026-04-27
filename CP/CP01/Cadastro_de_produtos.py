import json

arquivo = "eletronicos.json"

class Produtos:
    def __init__(self,id,nome,preco,estoque,marca,fornecedor):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
        self.marca = marca
        self.fornecedor = fornecedor

class ProdutoEletronico(Produtos):

    def __init__(self,id,nome,preco,estoque,marca,fornecedor,componente,carregavel,descricao):
        super().__init__(id,nome,preco,estoque,marca,fornecedor)
        self.componente = componente
        self.carregavel = carregavel
        self.descricao = descricao

    def leitura(self):
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
        
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
            print(f"ID: {produto['id']} | Nome: {produto['nome']} | Preço: {produto['preco']} {alerta_estoque}")

    def buscar_descricao(self, id):
        dados = self.leitura()
        for produto in dados:
            if produto['id'] == id:
                nome = produto['nome']
                descricao = produto.get('descricao', 'Sem descrição')
                return f"Produto: {nome} | Descrição: {descricao}"
        return "Produto não encontrado."

    def carrinho_de_compra(self, id):
        dados = self.leitura()
        for produto in dados:
          if produto['id'] == id:4

          if produto['estoque'] > 0:
            produto['estoque'] -= 1
            self.salvar_dados(dados)
            return (f"Compra realizada!")
          else:
            return "Produto esgotado."
        return "Produto não encontrado."
    
    
# Criando o objeto para acessar os métodos
produto = ProdutoEletronico(0,"",0,0,"","","",False,"")

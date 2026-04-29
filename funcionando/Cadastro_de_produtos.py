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
    
    def adicionar_produto(self):
        dados = self.leitura()

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
        self.salvar_dados(dados)

        print("Produto adicionado com sucesso!")
    
    def buscar_descricao(self, id):
        produto = self.buscar_produto(id)
        if produto:
            return produto.get("descricao", "Sem descrição")
        return "Produto não encontrado"
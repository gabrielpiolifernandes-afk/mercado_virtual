import json
from datetime import datetime


class Carrinho:

    def __init__(self):
        self.itens = []
        self.abandonos = []
        self.fechado = False

    def adicionar(self, produto, quantidade):
        if quantidade <= 0:
            return "Quantidade inválida"

        for item in self.itens:
            if item["id"] == produto["id"]:
                item["quantidade"] += quantidade
                return "Quantidade atualizada no carrinho"

        self.itens.append({
            "id": produto["id"],
            "nome": produto["nome"],
            "preco": produto["preco"],
            "quantidade": quantidade
        })

        return "Adicionado ao carrinho"

    def remover(self, id_produto):
        for item in self.itens:
            if item["id"] == id_produto:
                self.itens.remove(item)
                return "Removido do carrinho"
        return "Produto não encontrado"

    def finalizar(self, compra_realizada):
        if compra_realizada:
            self.itens.clear()
            self.fechado = True
            return "Compra finalizada"

        # se não comprou e tinha itens, considera abandono
        if len(self.itens) > 0:
            self.abandonar()

        return "Carrinho não finalizado"

    def abandonar(self):
        if len(self.itens) == 0:
            return

        for item in self.itens:
            self.abandonos.append({
                "id": item['id'],
                "produto": item['nome'],
                "motivo": "não finalizou compra",
                "timestamp": datetime.now().isoformat()
            })

        self.itens.clear()

    def salvar_abandonos(self, arquivo="abandonos.json"):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(self.abandonos, f, ensure_ascii=False, indent=4)

    def carregar_abandonos(self, arquivo="abandonos.json"):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                self.abandonos = json.load(f)
        except FileNotFoundError:
            self.abandonos = []

    def relatorio_abandono(self):
        print("\n===== ABANDONO DE CARRINHO =====")

        if not self.abandonos:
            print("Nenhum abandono registrado")
            return

        for item in self.abandonos:
            print(f"Produto: {item['produto']} | Data: {item['timestamp']}")

    def listar(self):
        return self.itens
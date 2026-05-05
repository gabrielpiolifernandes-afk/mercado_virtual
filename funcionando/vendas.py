import json
from datetime import datetime
from cupons import Cupons

arquivo = "jsons/cupom.json"
arquivo_vendas = "jsons/historico_de_vendas.json"

class Vendas:

    def __init__(self, produto_obj, carrinho):
        self.produto_obj = produto_obj
        self.carrinho = carrinho
        self.metricas_venda = {}

    # ---------------- ESTOQUE ----------------
    def validar_estoque(self):
        dados = self.produto_obj.leitura()

        for item in self.carrinho.itens:
            for p in dados:
                if p['id'] == item['id']:
                    if p['estoque'] <= 0:
                        return f"Produto {p['nome']} sem estoque"

        return "OK"

    def descontar_estoque(self):
        dados = self.produto_obj.leitura()

        for item in self.carrinho.itens:
            for p in dados:
                if p['id'] == item['id']:
                    if p['estoque'] > 0:
                        p['estoque'] -= 1

        self.produto_obj.salvar_dados(dados)

    # ---------------- PAGAMENTO ----------------
    def escolher_pagamento(self):
        print("\nFormas de pagamento:")
        print("1. Cartão")
        print("2. Pix")
        print("3. Dinheiro")

        op = input("Escolha: ")

        if op == "1":
            return "Cartão"
        elif op == "2":
            return "Pix"
        elif op == "3":
            return "Dinheiro"
        else:
            return "Desconhecido"

    # ---------------- TOTAL ----------------
    def calcular_total(self, desconto=0):
        total = sum(item['preco'] for item in self.carrinho.itens)
        return total - (total * desconto / 100)

    # ---------------- RECIBO ----------------
    def emitir_recibo(self, total, desconto, pagamento):
        print("\n===== RECIBO =====")

        for item in self.carrinho.itens:
            print(f"{item['nome']} - R$ {item['preco']}")

        print(f"\nDesconto: {desconto}%")
        print(f"Pagamento: {pagamento}")
        print(f"TOTAL: R$ {total:.2f}")
        print("==================")

    # ---------------- REGISTRAR VENDA ----------------
    def registrar_venda(self):
        for item in self.carrinho.itens:
            produto_id = item['id']
            self.metricas_venda[produto_id] = self.metricas_venda.get(produto_id, 0) + 1

    # ---------------- HISTÓRICO ----------------
    def ler_historico_vendas(self, arquivo="jsons/historico_de_vendas.json"):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def salvar_venda_historico(self, total, desconto, pagamento, cupom_usado=None):
        dados = self.ler_historico_vendas()

        venda = {
            "id_venda": len(dados) + 1,
            "itens": self.carrinho.itens.copy(),
            "desconto": desconto,
            "cupom": cupom_usado,
            "pagamento": pagamento,
            "total": total,
            "data": datetime.now().isoformat()
        }

        dados.append(venda)

        with open("jsons/historico_de_vendas.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    # ---------------- COMPRA ----------------
    def confirmar_compra(self):

        if not self.carrinho.itens:
            return "Carrinho vazio"

        confirmacao = input("Confirmar compra? (S/N): ").upper()

        if confirmacao != "S":
            self.carrinho.abandonar()
            return "Compra cancelada"

        # ---------------- CUPOM ----------------
        desconto = 0
        cupom_usado = None

        usar_cupom = input("Deseja usar cupom? (S/N): ").upper()

        if usar_cupom == "S":

            while True:
                codigo = input("Digite o cupom (ou '0' para sair): ").lower().strip()

                if codigo == "0":
                    print("Saindo da área de cupom...")
                    break

                cupom_obj, status = self.validar_cupom(codigo)

                if status == "ok":
                    desconto = cupom_obj["desconto"]
                    cupom_usado = codigo
                    print("Cupom aplicado com sucesso!")
                    break

                elif status == "descontinuado":
                    print("Este cupom foi descontinuado.")

                elif status == "invalido":
                    print("Cupom inválido.")

        # PAGAMENTO
        pagamento = self.escolher_pagamento()

        # ESTOQUE
        validacao = self.validar_estoque()
        if validacao != "OK":
            return validacao

        # TOTAL
        total = self.calcular_total(desconto)

        # PROCESSAMENTO
        self.descontar_estoque()
        self.registrar_venda()

        # SALVAR HISTÓRICO
        self.salvar_venda_historico(total, desconto, pagamento, cupom_usado)

        # RECIBO
        self.emitir_recibo(total, desconto, pagamento)

        # LIMPAR CARRINHO
        self.carrinho.itens.clear()

        return "Compra realizada com sucesso!"

    # ---------------- RELATÓRIO ----------------
    def relatorio_vendas(self, arquivo="jsons/historico_de_vendas.json"):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except FileNotFoundError:
            print("Nenhuma venda registrada")
            return

        print("\n===== RELATÓRIO DE VENDAS =====")

        total_geral = 0

        for venda in dados:
            print(f"\nVenda ID: {venda['id_venda']}")
            print(f"Data: {venda['data']}")
            print(f"Pagamento: {venda['pagamento']}")
            print(f"Cupom: {venda['cupom']}")
            print(f"Desconto: {venda['desconto']}%")

            print("Itens:")
            for item in venda["itens"]:
                print(f" - {item['nome']} x{item['quantidade']} R$ {item['preco']}")

            print(f"Total: R$ {venda['total']:.2f}")

            total_geral += venda["total"]

        print("\n==============================")
        print(f"FATURAMENTO TOTAL: R$ {total_geral:.2f}")
    
    # ---------------- MENU ADMIN ----------------
    def menu_admin(self):

        while True:
            print("\n===== PAINEL DE VENDAS =====")
            print("1- Relatório de vendas")
            print("2 - Sair")

            op = input("Escolha: ")

            if op == "1":
                self.relatorio_vendas()

            elif op == "2":
                break

            else:
                print("Opção inválida!")


# ---------------- TESTE ----------------
if __name__ == "__main__":

    from Cadastro_de_produtos import ProdutoEletronico
    from carrinho import Carrinho

    produto_obj = ProdutoEletronico(0, "", 0, 0, "", "", "", False, "")
    carrinho = Carrinho()

    vendas = Vendas(produto_obj, carrinho)

    vendas.menu_admin()

#melhorar os cupons

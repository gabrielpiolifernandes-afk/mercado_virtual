import json
from datetime import datetime

arquivo_produto = "eletronicos.json"
arquivo = "cupom.json"
arquivo_vendas = "historico_de_vendas.json"

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

    # ---------------- CUPONS ----------------
    def ler_cupons(self, arquivo="cupom.json"):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def adicionar_cupom(self):
        cupons = self.ler_cupons()

        while True:
            codigo = input("Código do cupom: ").lower().strip()

            existe = False
            for c in cupons:
                if c["codigo"] == codigo:
                    print("Cupom já existe! Tente outro.")
                    existe = True
                    break

            if not existe:
                break

        try:
            desconto = float(input("Desconto (%): "))

            if desconto <= 0 or desconto > 100:
                print("Desconto inválido!")
                return

            novo_id = max([c["id"] for c in cupons], default=0) + 1

            novo_cupom = {
                "id": novo_id,
                "codigo": codigo,  
                "desconto": desconto,
                "ativo": True
            }

            cupons.append(novo_cupom)
            self.salvar_cupons(cupons)

            print(f"Cupom criado: {codigo} → {desconto}%")

        except ValueError:
            print("Valor inválido")
    
    def solicitar_cupom(self):
        resposta = input("Deseja usar um cupom? (S/N): ").upper().strip()

        if resposta != "S":
            return 0, None

        cupom = input("Digite o cupom: ")
        desconto = self.aplicar_cupom(cupom)

        if desconto > 0:
            return desconto, cupom.lower().strip()

        return 0, None

    def aplicar_cupom(self, cupom):
        cupom = cupom.lower().strip()

        cupons = self.ler_cupons()

        for c in cupons:
            if c["codigo"] == cupom:

                if not c.get("ativo", True):
                    print("Este cupom foi descontinuado.")
                    return 0

                print(f"Cupom aplicado: {c['desconto']}%")
                return c["desconto"]

        print("Cupom inválido")
        return 0
    
    def salvar_cupons(self, cupons, arquivo="cupom.json"):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(cupons, f, indent=4, ensure_ascii=False)
    
    def desativar_cupom(self):
        cupons = self.ler_cupons()

        if not cupons:
            print("Nenhum cupom cadastrado.")
            return

        try:
            print("\n===== CUPONS =====")
            for c in cupons:
                status = "ATIVO" if c.get("ativo", True) else "DESATIVADO"
                print(f"ID: {c['id']} | Código: {c['codigo']} | {c['desconto']}% | {status}")

            id_cupom = int(input("\nDigite o ID do cupom para desativar: "))

            for c in cupons:
                if c["id"] == id_cupom:
                    c["ativo"] = False
                    self.salvar_cupons(cupons)
                    print("Cupom desativado com sucesso!")
                    return

            print("Cupom não encontrado!")

        except ValueError:
            print("ID inválido!")
    
    def listar_cupons(self):
        cupons = self.ler_cupons()

        if not cupons:
            print("Nenhum cupom cadastrado.")
            return

        print("\n===== CUPONS =====")
        for c in cupons:
            status = "ATIVO" if c.get("ativo", True) else "DESCONTINUADO"
            print(f"ID: {c['id']} | Código: {c['codigo']} | {c['desconto']}% | {status}")

    def validar_cupom(self, codigo):
        cupons = self.ler_cupons()

        for c in cupons:
            if c["codigo"] == codigo:

                if not c.get("ativo", True):
                    return None, "descontinuado"

                return c, "ok"

        return None, "invalido"
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
    def ler_historico_vendas(self, arquivo="historico_de_vendas.json"):
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

        with open("historico_de_vendas.json", "w", encoding="utf-8") as f:
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
    
    def _mostrar_venda(self, venda):
        print(f"\nVenda ID: {venda['id_venda']}")
        print(f"Data: {venda['data']}")
        print(f"Pagamento: {venda['pagamento']}")
        print(f"Cupom: {venda['cupom']}")
        print(f"Desconto: {venda['desconto']}%")

        print("Itens:")
        for item in venda["itens"]:
            print(f" - {item['nome']} x{item['quantidade']} R$ {item['preco']}")

        print(f"Total: R$ {venda['total']:.2f}")
    
    def relatorio_vendas(self, arquivo="historico_de_vendas.json"):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except FileNotFoundError:
            print("Nenhuma venda registrada")
            return

        if not dados:
            print("Nenhuma venda registrada")
            return

        print("\n===== RELATÓRIO DE VENDAS =====")
        print("1 - Ver venda por ID")
        print("2 - Ver lista (10 por vez)")

        opcao = input("Escolha: ")

        # 🔎 FILTRO POR ID
        if opcao == "1":
            try:
                id_busca = int(input("Digite o ID da venda: "))

                for venda in dados:
                    if venda["id_venda"] == id_busca:
                        self._mostrar_venda(venda)
                        return

                print("Venda não encontrada.")

            except ValueError:
                print("ID inválido")

        elif opcao == "2":
            tamanho = 10
            for i in range(0, len(dados), tamanho):
                bloco = dados[i:i + tamanho]

                print(f"\n===== VENDAS {i+1} até {i+len(bloco)} =====")

                for venda in bloco:
                    print(f"ID: {venda['id_venda']} | Total: R$ {venda['total']:.2f}")

                input("\nPressione ENTER para ver mais...")

        else:
            print("Opção inválida")
    
    # ---------------- MENU ADMIN ----------------
    def menu_admin(self):

        while True:
            print("\n===== PAINEL DE VENDAS =====")
            print("1 - Criar cupom")
            print("2 - Remover cupom")
            print("3 - Listar cupons")
            print("4 - Relatório de vendas")
            print("5 - Sair")

            op = input("Escolha: ")

            if op == "1":
                self.adicionar_cupom()

            elif op == "2":
                self.desativar_cupom()  

            elif op == "3":
                self.listar_cupons()  

            elif op == "4":
                self.relatorio_vendas()

            elif op == "5":
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

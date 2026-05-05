import json

class Cupons:
    def __init__(self):
        self.cupons = []

    def ler_cupons(self, arquivo="jsons/cupom.json"):
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
        
    def salvar_cupons(self, cupons, arquivo="jsons/cupom.json"):
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

                    if not c.get("ativo", True):
                        print("O cupom já está desativado.")
                        return

                    verificacao = input("Deseja realmente desativar este cupom? (S/N): ").upper().strip()

                    if verificacao == "S":
                        c["ativo"] = False
                        self.salvar_cupons(cupons)
                        print("Cupom desativado com sucesso!")
                    else:
                        print("Operação cancelada.")

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
    
    def reativar_cupom(self):
        cupons = self.ler_cupons()

        if not cupons:
            print("Nenhum cupom cadastrado.")
            return

        try:
            print("\n===== CUPONS =====")
            for c in cupons:
                status = "ATIVO" if c.get("ativo", True) else "DESATIVADO"
                print(f"ID: {c['id']} | Código: {c['codigo']} | {c['desconto']}% | {status}")

            id_cupom = int(input("\nDigite o ID do cupom para reativar: "))

            for c in cupons:
                if c["id"] == id_cupom:

                    if c.get("ativo", True):
                        print("O cupom já está ativo.")
                        return

                    resp = input("Deseja reativar este cupom? (S/N): ").upper().strip()

                    if resp == "S":
                        c["ativo"] = True
                        self.salvar_cupons(cupons)
                        print("Cupom reativado com sucesso!")
                    else:
                        print("Operação cancelada.")

                    return

            print("Cupom não encontrado!")

        except ValueError:
            print("ID inválido!")

    def validar_cupom(self, codigo):
            cupons = self.ler_cupons()

            for c in cupons:
                if c["codigo"] == codigo:

                    if not c.get("ativo", True):
                        return None, "descontinuado"

                    return c, "ok"

            return None, "invalido"

    def menu_admin_cupons(self):

            while True:
                print("\n===== PAINEL DE CUPONS =====")
                print("1 - Criar cupom")
                print("2 - Desativar cupom")
                print("3 - Reativar cupom")
                print("4 - Listar cupons")
                print("5 - Sair")

                op = input("Escolha: ")

                if op == "1":
                    self.adicionar_cupom()

                elif op == "2":
                    self.desativar_cupom()

                elif op == "3":
                    self.reativar_cupom()

                elif op == "4":
                    self.listar_cupons()  

                elif op == "5":
                    break

                else:
                    print("Opção inválida!")
            
if __name__ == "__main__":
    c = Cupons()
    c.menu_admin_cupons()
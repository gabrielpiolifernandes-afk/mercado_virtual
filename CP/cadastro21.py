import json
import os

arquivo = "clientes.json"

class Cliente:
    def __init__(self, id, nome, cpf, telefone, cep, senha):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.cep = cep
        self.senha = senha

def Leitura_de_dados():
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def cadastro():
    while True:
        try:
            clientes_existentes = Leitura_de_dados()
            ids_existentes = [c['id'] for c in clientes_existentes]

            # ID
            while True:
                try:
                    id = int(input("ID: "))
                    if id in ids_existentes:
                        print("ID já cadastrado! Digite outro.")
                    else:
                        break
                except ValueError:
                    print("Digite um número válido.")

            nome = input("Nome: ")

            # CPF
            while True:
                cpf = input("CPF (11 dígitos): ")
                if cpf.isdigit() and len(cpf) == 11:
                    break
                print("CPF inválido!")

            # Telefone
            while True:
                telefone = input("Telefone (10 ou 11 dígitos): ")
                if telefone.isdigit() and 10 <= len(telefone) <= 11:
                    break
                print("Telefone inválido!")

            # CEP
            while True:
                cep = input("CEP (8 dígitos): ")
                if cep.isdigit() and len(cep) == 8:
                    break
                print("CEP inválido!")

            # Senha
            senha = input("Senha: ")
            confirmar_senha = input("Confirme a senha: ")

            if senha != confirmar_senha:
                print("As senhas não coincidem!")
                continue

            # Confirmação
            print("\n--- Resumo do Cadastro ---")
            print(f"ID: {id}")
            print(f"Nome: {nome}")
            print(f"CPF: {cpf}")
            print(f"Telefone: {telefone}")
            print(f"CEP: {cep}")

            confirma = input("Confirmar cadastro? (S/N): ").strip().upper()

            if confirma == "S":
                return Cliente(id=id, nome=nome, cpf=cpf, telefone=telefone, cep=cep, senha=senha)
            else:
                print("Reiniciando cadastro...\n")

        except Exception as e:
            print(f"Erro inesperado: {e}")
    
def Salvar_dados(cliente):
    # Se o arquivo não existir, criamos uma lista vazia
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = []
    else:
        dados = []

    # Adiciona o cliente recém-criado
    dados.append(cliente.__dict__)

    # Salva de volta no JSON
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

                
while True:
    print("\n===MENU PRINCIPAL===")  
    print("1. Tela de cadastro")   
    print("2. - Sair")  

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        cliente = cadastro()
        Salvar_dados(cliente)
        print("Cliente cadastrado com sucesso!")    

    elif opcao == "2":
        print("Saindo do sistema...")
        break   

    
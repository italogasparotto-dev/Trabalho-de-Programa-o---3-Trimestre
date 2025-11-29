from services.banco_service import BancoService
from services.autenticacao_service import AutenticacaoService
from utils.validadores import validar_numero_conta, formatar_moeda

class SistemaBancario:
    def __init__(self):
        self.banco_service = BancoService()
        self.auth_service = AutenticacaoService(self.banco_service)
    
    def menu_principal(self):
        while True:
            print("\n" + "="*50)
            print("          SISTEMA BANCÁRIO - POO")
            print("="*50)
            print("1. Cadastrar Cliente")
            print("2. Criar Conta")
            print("3. Login")
            print("4. Listar Contas")
            print("5. Listar Clientes")
            print("6. Estatísticas")
            print("0. Sair")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == '1':
                self.cadastrar_cliente()
            elif opcao == '2':
                self.criar_conta()
            elif opcao == '3':
                self.login()
            elif opcao == '4':
                self.banco_service.listar_contas()
            elif opcao == '5':
                self.banco_service.listar_clientes()
            elif opcao == '6':
                self.mostrar_estatisticas()
            elif opcao == '0':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida!")
    
    def cadastrar_cliente(self):
        print("\n=== CADASTRAR CLIENTE ===")
        nome = input("Nome completo: ")
        cpf = input("CPF: ")
        email = input("Email: ")
        telefone = input("Telefone: ")
        endereco = input("Endereço: ")
        
        self.banco_service.cadastrar_cliente(nome, cpf, email, telefone, endereco)
    
    def criar_conta(self):
        print("\n=== CRIAR CONTA ===")
        cpf = input("CPF do cliente: ")
        cliente = self.banco_service.encontrar_cliente_por_cpf(cpf)
        
        if not cliente:
            print("Cliente não encontrado! Cadastre o cliente primeiro.")
            return
        
        numero = input("Número da conta: ")
        if not validar_numero_conta(numero):
            print("Número da conta inválido! Deve conter apenas números e ter pelo menos 4 dígitos.")
            return
        
        senha = input("Senha: ")
        
        print("\nTipos de conta disponíveis:")
        print("1. Conta Corrente")
        print("2. Conta Poupança")
        print("3. Conta Empresarial")
        
        tipo_opcao = input("Escolha o tipo de conta (1-3): ")
        tipos = {'1': 'corrente', '2': 'poupanca', '3': 'empresarial'}
        
        if tipo_opcao not in tipos:
            print("Opção inválida!")
            return
        
        try:
            saldo = float(input("Saldo inicial: R$"))
        except ValueError:
            print("Valor inválido!")
            return
        
        self.banco_service.criar_conta(cliente, numero, senha, tipos[tipo_opcao], saldo)
    
    def login(self):
        print("\n=== LOGIN ===")
        numero = input("Número da conta: ")
        senha = input("Senha: ")
        
        if self.auth_service.login(numero, senha):
            self.menu_conta()
    
    def menu_conta(self):
        while self.auth_service.esta_logado:
            conta = self.auth_service.conta_logada
            
            print(f"\n" + "="*50)
            print(f"CONTA: {conta.numero} - {conta.cliente.nome}")
            print("="*50)
            print("1. Ver Saldo")
            print("2. Sacar")
            print("3. Depositar")
            print("4. Transferir")
            print("5. Extrato")
            print("6. Alterar Senha")
            
            # Opções específicas por tipo de conta
            if hasattr(conta, 'aplicar_rendimento'):
                print("7. Aplicar Rendimento")
            if hasattr(conta, 'usar_limite_credito'):
                print("8. Usar Limite de Crédito")
            
            print("0. Logout")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == '1':
                print(f"\nSaldo atual: {formatar_moeda(conta.saldo)}")
            elif opcao == '2':
                self.realizar_saque()
            elif opcao == '3':
                self.realizar_deposito()
            elif opcao == '4':
                self.realizar_transferencia()
            elif opcao == '5':
                conta.extrato()
            elif opcao == '6':
                self.alterar_senha()
            elif opcao == '7' and hasattr(conta, 'aplicar_rendimento'):
                conta.aplicar_rendimento()
            elif opcao == '8' and hasattr(conta, 'usar_limite_credito'):
                self.usar_limite_credito()
            elif opcao == '0':
                self.auth_service.logout()
            else:
                print("Opção inválida!")
    
    def realizar_saque(self):
        try:
            valor = float(input("Valor para sacar: R$"))
            self.auth_service.conta_logada.sacar(valor)
        except ValueError:
            print("Valor inválido!")
    
    def realizar_deposito(self):
        try:
            valor = float(input("Valor para depositar: R$"))
            self.auth_service.conta_logada.depositar(valor)
        except ValueError:
            print("Valor inválido!")
    
    def realizar_transferencia(self):
        try:
            numero_destino = input("Número da conta destino: ")
            conta_destino = self.banco_service.encontrar_conta_por_numero(numero_destino)
            
            if not conta_destino:
                print("Conta destino não encontrada!")
                return
            
            if conta_destino.numero == self.auth_service.conta_logada.numero:
                print("Não é possível transferir para a própria conta!")
                return
            
            valor = float(input("Valor para transferir: R$"))
            self.auth_service.conta_logada.transferir(valor, conta_destino)
        except ValueError:
            print("Valor inválido!")
    
    def alterar_senha(self):
        nova_senha = input("Nova senha: ")
        self.auth_service.conta_logada.alterar_senha(nova_senha)
    
    def usar_limite_credito(self):
        if hasattr(self.auth_service.conta_logada, 'usar_limite_credito'):
            try:
                valor = float(input("Valor do limite a utilizar: R$"))
                self.auth_service.conta_logada.usar_limite_credito(valor)
            except ValueError:
                print("Valor inválido!")
        else:
            print("Esta conta não possui limite de crédito!")
    
    def mostrar_estatisticas(self):
        print("\n=== ESTATÍSTICAS DO BANCO ===")
        print(f"Total de clientes: {self.banco_service.total_clientes}")
        print(f"Total de contas: {self.banco_service.total_contas}")


def main():
    sistema = SistemaBancario()
    sistema.menu_principal()


if __name__ == "__main__":
    main()
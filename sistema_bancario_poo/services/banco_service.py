from entities.conta import ContaCorrente, ContaPoupanca, ContaEmpresarial
from entities.cliente import Cliente
from utils.validadores import validar_cpf, validar_email

class BancoService:
    def __init__(self):
        self._clientes = []
        self._contas = []
    
    def cadastrar_cliente(self, nome, cpf, email, telefone, endereco):
        if not validar_cpf(cpf):
            print("CPF inválido!")
            return None
        
        if not validar_email(email):
            print("Email inválido!")
            return None
        
        # Verificar se CPF já existe
        for cliente in self._clientes:
            if cliente.cpf == cpf:
                print("Cliente já cadastrado com este CPF!")
                return None
        
        cliente = Cliente(nome, cpf, email, telefone, endereco)
        self._clientes.append(cliente)
        print(f"Cliente {nome} cadastrado com sucesso!")
        return cliente
    
    def criar_conta(self, cliente, numero_conta, senha, tipo_conta, saldo_inicial=0.0):
        # Verificar se número da conta já existe
        for conta in self._contas:
            if conta.numero == numero_conta:
                print("Número de conta já existe!")
                return None
        
        if tipo_conta == "corrente":
            conta = ContaCorrente(numero_conta, cliente, saldo_inicial, senha)
        elif tipo_conta == "poupanca":
            conta = ContaPoupanca(numero_conta, cliente, saldo_inicial, senha)
        elif tipo_conta == "empresarial":
            conta = ContaEmpresarial(numero_conta, cliente, saldo_inicial, senha)
        else:
            print("Tipo de conta inválido!")
            return None
        
        self._contas.append(conta)
        cliente.adicionar_conta(conta)
        print(f"Conta {tipo_conta} criada com sucesso!")
        return conta
    
    def encontrar_conta_por_numero(self, numero):
        for conta in self._contas:
            if conta.numero == numero:
                return conta
        return None
    
    def encontrar_cliente_por_cpf(self, cpf):
        for cliente in self._clientes:
            if cliente.cpf == cpf:
                return cliente
        return None
    
    def autenticar_conta(self, numero, senha):
        conta = self.encontrar_conta_por_numero(numero)
        if conta and conta.verificar_senha(senha):
            return conta
        return None
    
    def listar_contas(self):
        print("\n=== TODAS AS CONTAS ===")
        for conta in self._contas:
            print(conta)
    
    def listar_clientes(self):
        print("\n=== TODOS OS CLIENTES ===")
        for cliente in self._clientes:
            print(cliente)
            for conta in cliente.listar_contas():
                print(f"  - {conta}")
    
    @property
    def total_contas(self):
        return len(self._contas)
    
    @property
    def total_clientes(self):
        return len(self._clientes)
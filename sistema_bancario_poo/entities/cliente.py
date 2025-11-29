class Cliente:
    def __init__(self, nome, cpf, email, telefone, endereco):
        self._nome = nome
        self._cpf = cpf
        self._email = email
        self._telefone = telefone
        self._endereco = endereco
        self._contas = []
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def email(self):
        return self._email
    
    @property
    def telefone(self):
        return self._telefone
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)
    
    def listar_contas(self):
        return self._contas
    
    def __str__(self):
        return f"Cliente: {self._nome} (CPF: {self._cpf})"
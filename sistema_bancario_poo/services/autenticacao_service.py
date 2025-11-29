class AutenticacaoService:
    def __init__(self, banco_service):
        self._banco_service = banco_service
        self._conta_logada = None
    
    def login(self, numero_conta, senha):
        conta = self._banco_service.autenticar_conta(numero_conta, senha)
        if conta:
            self._conta_logada = conta
            print(f"Login realizado com sucesso! Bem-vindo(a), {conta.cliente.nome}")
            return True
        else:
            print("Número da conta ou senha incorretos!")
            return False
    
    def logout(self):
        if self._conta_logada:
            print(f"Logout realizado. Até logo, {self._conta_logada.cliente.nome}!")
            self._conta_logada = None
        else:
            print("Nenhum usuário logado.")
    
    @property
    def conta_logada(self):
        return self._conta_logada
    
    @property
    def esta_logado(self):
        return self._conta_logada is not None
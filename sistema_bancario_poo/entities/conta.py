from abc import ABC, abstractmethod
from datetime import datetime

class Conta(ABC):
    def __init__(self, numero, cliente, saldo=0.0, senha=""):
        self._numero = numero
        self._cliente = cliente
        self._saldo = saldo
        self._senha = senha
        self._transacoes = []
        self._data_criacao = datetime.now()
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def data_criacao(self):
        return self._data_criacao
    
    def verificar_senha(self, senha):
        return self._senha == senha
    
    def alterar_senha(self, nova_senha):
        self._senha = nova_senha
        print("Senha alterada com sucesso!")
    
    @abstractmethod
    def calcular_taxa(self, valor):
        pass
    
    def depositar(self, valor):
        if valor > 0:
            taxa = self.calcular_taxa(valor)
            valor_liquido = valor - taxa
            self._saldo += valor_liquido
            self._registrar_transacao("DEPÓSITO", valor, taxa)
            print(f"Depósito de R${valor:.2f} realizado. Taxa: R${taxa:.2f}")
            return True
        return False
    
    def sacar(self, valor):
        if valor > 0:
            taxa = self.calcular_taxa(valor)
            total = valor + taxa
            
            if self._saldo >= total:
                self._saldo -= total
                self._registrar_transacao("SAQUE", valor, taxa)
                print(f"Saque de R${valor:.2f} realizado. Taxa: R${taxa:.2f}")
                return True
            else:
                print("Saldo insuficiente.")
        return False
    
    def transferir(self, valor, conta_destino):
        if valor > 0 and conta_destino != self:
            taxa = self.calcular_taxa(valor)
            total = valor + taxa
            
            if self._saldo >= total:
                self._saldo -= total
                conta_destino._saldo += valor
                
                self._registrar_transacao("TRANSFERÊNCIA_ENVIADA", valor, taxa, conta_destino.numero)
                conta_destino._registrar_transacao("TRANSFERÊNCIA_RECEBIDA", valor, 0, self.numero)
                
                print(f"Transferência de R${valor:.2f} realizada para conta {conta_destino.numero}")
                return True
            else:
                print("Saldo insuficiente para transferência.")
        return False
    
    def _registrar_transacao(self, tipo, valor, taxa, conta_relacionada=""):
        transacao = {
            'data': datetime.now(),
            'tipo': tipo,
            'valor': valor,
            'taxa': taxa,
            'conta_relacionada': conta_relacionada,
            'saldo_apos': self._saldo
        }
        self._transacoes.append(transacao)
    
    def extrato(self):
        print(f"\n=== EXTRATO - CONTA {self._numero} ===")
        print(f"Cliente: {self._cliente.nome}")
        print(f"Saldo atual: R${self._saldo:.2f}")
        print(f"Data de abertura: {self._data_criacao.strftime('%d/%m/%Y %H:%M')}")
        print("\nÚltimas transações:")
        
        for transacao in self._transacoes[-10:]:  # Últimas 10 transações
            data = transacao['data'].strftime('%d/%m %H:%M')
            tipo = transacao['tipo']
            valor = transacao['valor']
            taxa = transacao['taxa']
            conta_rel = transacao['conta_relacionada']
            
            if tipo == "DEPÓSITO":
                print(f"{data} | {tipo:20} | +R${valor:8.2f} | Taxa: R${taxa:.2f}")
            elif tipo == "SAQUE":
                print(f"{data} | {tipo:20} | -R${valor:8.2f} | Taxa: R${taxa:.2f}")
            elif tipo == "TRANSFERÊNCIA_ENVIADA":
                print(f"{data} | {tipo:20} | -R${valor:8.2f} | Taxa: R${taxa:.2f} | Para: {conta_rel}")
            elif tipo == "TRANSFERÊNCIA_RECEBIDA":
                print(f"{data} | {tipo:20} | +R${valor:8.2f} | De: {conta_rel}")
    
    def __str__(self):
        return f"Conta {self._numero} - {self._cliente.nome} - Saldo: R${self._saldo:.2f}"


class ContaCorrente(Conta):
    def calcular_taxa(self, valor):
        # Taxa fixa para operações
        if valor <= 100:
            return 1.00
        elif valor <= 1000:
            return 2.50
        else:
            return 5.00


class ContaPoupanca(Conta):
    def __init__(self, numero, cliente, saldo=0.0, senha="", taxa_rendimento=0.005):
        super().__init__(numero, cliente, saldo, senha)
        self._taxa_rendimento = taxa_rendimento
    
    def calcular_taxa(self, valor):
        # Conta poupança tem taxas menores
        return 0.50
    
    def aplicar_rendimento(self):
        rendimento = self._saldo * self._taxa_rendimento
        self._saldo += rendimento
        self._registrar_transacao("RENDIMENTO", rendimento, 0)
        print(f"Rendimento aplicado: R${rendimento:.2f}")
        return rendimento


class ContaEmpresarial(Conta):
    def __init__(self, numero, cliente, saldo=0.0, senha="", limite_credito=5000):
        super().__init__(numero, cliente, saldo, senha)
        self._limite_credito = limite_credito
    
    def calcular_taxa(self, valor):
        # Conta empresarial tem taxas diferenciadas
        return max(10.00, valor * 0.01)  # 1% ou R$10, o que for maior
    
    @property
    def limite_credito(self):
        return self._limite_credito
    
    def usar_limite_credito(self, valor):
        if valor <= self._limite_credito:
            self._saldo += valor
            self._limite_credito -= valor
            self._registrar_transacao("LIMITE_CRÉDITO", valor, 0)
            print(f"Limite de crédito utilizado: R${valor:.2f}")
            return True
        return False
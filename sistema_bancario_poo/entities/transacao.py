from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    def __init__(self, valor, conta):
        self._valor = valor
        self._conta = conta
        self._data = datetime.now()
    
    @property
    def valor(self):
        return self._valor
    
    @property
    def data(self):
        return self._data
    
    @abstractmethod
    def registrar(self):
        pass


class Deposito(Transacao):
    def registrar(self):
        return self._conta.depositar(self._valor)


class Saque(Transacao):
    def registrar(self):
        return self._conta.sacar(self._valor)


class Transferencia(Transacao):
    def __init__(self, valor, conta_origem, conta_destino):
        super().__init__(valor, conta_origem)
        self._conta_destino = conta_destino
    
    def registrar(self):
        return self._conta.transferir(self._valor, self._conta_destino)
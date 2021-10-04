from abc import ABC, abstractmethod
# Manejo de las expresiones
class Expresion(ABC):
#metodo que sobre carga los entornos
    @abstractmethod
    def execute(self, entornos):
        pass
# metodo que llama las expresiones para el ast
    @abstractmethod
    def getAST(self, dot):
        pass
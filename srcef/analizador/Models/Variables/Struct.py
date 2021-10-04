#Importacion de clases abstractas para la implemenacion del acceso
from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *

import random
import graphviz

class Struct(Expresion):
#constructor de la sentencia struct, sobrecarga operadores derecho e izquierdo
    def __init__(self, id, mutable, atributos, fila = None, columna = None):
        self.ID = id
        self.Mutable = mutable
        self.Atributos = atributos
        self.Fila = fila
        self.Columna = columna
#Interfaz para la ejecucion de la sentencia
    def execute(self, entorno):   
        entorno.setStruct(self.ID, self, self.Fila, self.Columna)

    def getAST(self, dot):
        idDecl = str(random.randint(1, 1000000000))
        idMutable = str(random.randint(1, 1000000000))
        idStruct = str(random.randint(1, 1000000000))
        idVariable = str(random.randint(1, 1000000000))
        idAtributos = str(random.randint(1, 1000000000))
        idEnd = str(random.randint(1, 1000000000))

        dot.node(idDecl, "declaracion")
        if self.Mutable: dot.node(idMutable, "mutable")
        dot.node(idStruct, "struct")
        dot.node(idVariable, self.ID)
        dot.node(idAtributos, "atributos")
        dot.node(idEnd, "end;")

        if self.Mutable: dot.edge(idDecl, idMutable)
        dot.edge(idDecl, idStruct)
        dot.edge(idDecl, idVariable)
        dot.edge(idDecl, idAtributos)
        dot.edge(idDecl, idEnd)

        for attr in self.Atributos:
            dot, IDDotAttr = attr.getAST(dot)
            dot.edge(idAtributos, IDDotAttr)

        return dot, idDecl
from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *

import random
import graphviz

class ParamDecl(Expresion):
# Constructor para la declaracion de los parametors
    def __init__(self, idParam, idTipo, fila, columna):
        self.IDParam = idParam
        self.IDTipo = idTipo
        self.Fila = fila
        self.Columna = columna
# Interfaz de ejecucion
    def execute(self, entorno):
        return self
# Manejo del ast
    def getAST(self, dot):
         #memoria para los ids de los nodos del arbol
        idParam = str(random.randint(1, 1000000000))
        idVariable = str(random.randint(1, 1000000000))
        idTipo = str(random.randint(1, 1000000000))
        id2Puntos = str(random.randint(1, 1000000000))
        #nodo tipo y nodo variable
        dot.node(idParam, "Declaracion Parametro")
        dot.node(idVariable, self.IDParam)
        dot.edge(idParam, idVariable)

        if self.IDTipo != "Any":
            dot.node(id2Puntos, ": :")
            dot.node(idTipo, self.IDTipo)
            dot.edge(idParam, id2Puntos)
            dot.edge(idParam, idTipo)

        return dot, idParam
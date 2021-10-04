#Importacion de clases abstractas para la implemenacion del acceso
from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *

import random
import graphviz

class Atributo(Expresion):
#constructor de la sentencia if, sobrecarga operadores derecho e izquierdo
    def __init__(self, id, tipo, fila, columna):
        self.ID = id
        self.Tipo = tipo
        self.Valor = None
        self.TipoOrigen = tipo # Para los datos any
        self.Fila = fila
        self.Columna = columna
#Interfaz para la ejecucion de la sentencia
    def execute(self, entorno):
        return Retorno(self.Valor, self.Tipo)

    def getAST(self, dot):
        idAttr = str(random.randint(1, 1000000000))
        idVariable = str(random.randint(1, 1000000000))
        idTipo = str(random.randint(1, 1000000000))
        id2Puntos = str(random.randint(1, 1000000000))
        idPtComa = str(random.randint(1, 1000000000))

        dot.node(idAttr, "atributo")
        dot.node(idVariable, self.ID)
        dot.edge(idAttr, idVariable)

        if self.Tipo != "Any":
            dot.node(id2Puntos, ": :")
            dot.node(idTipo, self.Tipo)
            dot.edge(idAttr, id2Puntos)
            dot.edge(idAttr, idTipo)

        dot.node(idPtComa, ";")
        dot.edge(idAttr, idPtComa)

        return dot, idAttr






#Importacion de clases abstractas para la implemenacion del arreglo
from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *
from ...Abstractos import Globales

import random
import graphviz

class Arreglo(Expresion):
#constructor de la sentencia if, sobrecarga operadores derecho e izquierdo
    def __init__(self, array, tipo, indices, fila, columna):
        self.Array = array
        self.Tipo = tipo       # Si es declaracion o acceso
        self.Indices = indices
        self.Fila = fila
        self.Columna = columna
#Interfaz para la ejecucion de la sentencia
    def execute(self, entorno):
        if self.Tipo == "declaracion":
            arrayIndices = []
            
            # Verificacion array
            for exp in self.Array:
                valorExp = exp.execute(entorno)
                if valorExp.Valor == "ERROR":
                    return Retorno("ERROR", "array")

                arrayIndices.append(valorExp)

            # Crear objeto arreglo
            nuevoArray = Arreglo(arrayIndices, "array", None, self.Fila, self.Columna)
            return Retorno(nuevoArray, "array")

    def getAST(self, dot):
        if self.Tipo == "Declaracion":
            idDecl = str(random.randint(1, 1000000000))
            idCorIzq = str(random.randint(1, 1000000000))
            idIndices = str(random.randint(1, 1000000000))
            idCorDer = str(random.randint(1, 1000000000))

            dot.node(idDecl, "declaracion")
            dot.node(idCorIzq, "[")
            dot.node(idIndices, "indices")

            for i, exp in enumerate(self.Array):
                dot, IDDotExp = exp.getAST(dot)
                dot.edge(idIndices, IDDotExp)

                if i < len(self.Array) - 1:
                    idComa = str(random.randint(1, 1000000000))
                    dot.node(idComa, ",")
                    dot.edge(idIndices, idComa)
            
            dot.node(idCorDer, "]")

            dot.edge(idDecl, idCorIzq)
            dot.edge(idDecl, idIndices)
            dot.edge(idDecl, idCorDer)

            return dot, idDecl
        
        elif self.Tipo == "acceso":
            idIndices = str(random.randint(1, 1000000000))
            idVariable = str(random.randint(1, 1000000000))

            dot.node(idIndices, "dimensional")
            dot.node(idVariable, str(self.Array))

            dot.edge(idIndices, idVariable)

            for indice in self.Indices:
                idDimension = str(random.randint(1, 1000000000))
                idExp = str(random.randint(1, 1000000000))
                idCorIzq = str(random.randint(1, 1000000000))
                idCorDer = str(random.randint(1, 1000000000))

                dot.node(idDimension, "dimension")
                dot.node(idCorIzq, "[")
                dot.node(idExp, "expresion")
                dot.node(idCorDer, "]")

                dot.edge(idDimension, idCorIzq)
                dot.edge(idDimension, idExp)
                dot.edge(idDimension, idCorDer)

                dot, IDDotExp = indice.getAST(dot)
                dot.edge(idExp, IDDotExp)

                dot.edge(idIndices, idDimension)

            return dot, idIndices                
                


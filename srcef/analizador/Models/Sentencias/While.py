#Importacion de clases abstractas para la implemenacion del if
from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *
from ...Abstractos import Globales

import random
import graphviz

class While(Expresion):
#constructor de la sentencia whlile, sobrecarga operadores derecho e izquierdo
    def __init__(self, condicion, instrucciones, fila, columna):
        self.Condicion = condicion
        self.Instrucciones = instrucciones
        self.Fila = fila
        self.Columna = columna
    #Interfaz para la ejecucion de la sentencia
    def execute(self, entorno):
        while True:
            valorCondicion = self.Condicion.execute(entorno)
            
            if valorCondicion.Tipo != "Bool":
                Globales.tablaErrores.append(Error(f"La condicion no resulta en boolean: {valorCondicion.Tipo}", self.Fila, self.Columna))
                return
            
            if valorCondicion.Valor:
                resultCorrida = self.Instrucciones.execute(entorno)

                # Sentencias de transferencia
                if resultCorrida != None:
                    if resultCorrida.Tipo == "continue":
                        continue
                    elif resultCorrida.Tipo == "break":
                        return
                    elif resultCorrida.Tipo == "return":
                        return resultCorrida
            else:
                return

    def getAST(self, dot):
        idCiclo = str(random.randint(1, 1000000000))
        idWhile = str(random.randint(1, 1000000000))
        idExp = str(random.randint(1, 1000000000))
        idBloque = str(random.randint(1, 1000000000))
        idEND = str(random.randint(1, 1000000000))

        dot.node(idCiclo, "Sentencia")
        dot.node(idWhile, "while")
        dot.node(idExp, "Expresion")
        dot.node(idBloque, "Bloque")
        dot.node(idEND, "end;")

        dot.edge(idCiclo, idWhile)
        dot.edge(idCiclo, idExp)
        dot.edge(idCiclo, idBloque)
        dot.edge(idCiclo, idEND)

        # Expresion
        dot, IDDotExp = self.Condicion.getAST(dot)
        dot.edge(idExp, IDDotExp)

        # Bloque
        dot, IDDotBloque = self.Instrucciones.getAST(dot)
        dot.edge(idBloque, IDDotBloque)

        return dot, idCiclo
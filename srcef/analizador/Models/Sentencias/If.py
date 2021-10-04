#Importacion de clases abstractas para la implemenacion del if
from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *
from ...Abstractos import Globales

import random
import graphviz

class If(Expresion):
#constructor de la sentencia if, sobrecarga operadores derecho e izquierdo
    def __init__(self, condicion, instrucciones, elseInst, fila, columna):
        self.Condicion = condicion
        self.Instrucciones = instrucciones
        self.ElseInst = elseInst
        self.Fila = fila
        self.Columna = columna
#Interfaz para la ejecucion de la sentencia
    def execute(self, entorno):
        valorCondicion = self.Condicion.execute(entorno)

        if valorCondicion.Tipo != "Bool":
            Globales.tablaErrores.append(Error(f"La condicion no resulta en boolean: {valorCondicion.Tipo}", self.Fila, self.Columna))
            return
        
        if valorCondicion.Valor:
            return self.Instrucciones.execute(entorno)
        elif self.ElseInst != None:
            return self.ElseInst.execute(entorno)

    def getAST(self, dot):
        idSentencia = str(random.randint(1, 1000000000))
        idIf = str(random.randint(1, 1000000000))
        idExp = str(random.randint(1, 1000000000))
        idBloque = str(random.randint(1, 1000000000))
        idElseInst = str(random.randint(1, 1000000000))

        dot.node(idSentencia, "sentencia")
        dot.node(idIf, "if")
        dot.node(idExp, "condicion")
        dot.node(idBloque, "bloque")

        if self.ElseInst: dot.node(idElseInst, "else")
        
        dot.edge(idSentencia, idIf)
        dot.edge(idSentencia, idExp)
        dot.edge(idSentencia, idBloque)

        if self.ElseInst: dot.edge(idSentencia, idElseInst)

        # Expresion
        dot, IDDotExp = self.Condicion.getAST(dot)
        dot.edge(idExp, IDDotExp)

        # Bloque
        dot, IDDotBloque = self.Instrucciones.getAST(dot)
        dot.edge(idBloque, IDDotBloque)

        # ElseIFs
        if self.ElseInst:
            dot, IDDotIfs = self.ElseInst.getAST(dot)
            dot.edge(idElseInst, IDDotIfs)

            # Validacion si es un else poner end;
            if not hasattr(self.ElseInst, "Condicion"):
                idEND = str(random.randint(1, 1000000000))
                dot.node(idEND, "end;")
                dot.edge(idSentencia, idEND)

        else:
            idEND = str(random.randint(1, 1000000000))
            dot.node(idEND, "end;")
            dot.edge(idSentencia, idEND)

        return dot, idSentencia

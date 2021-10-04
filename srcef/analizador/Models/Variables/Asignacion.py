#Importacion de clases abstractas para la implemenacion del asignacion
from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *
from ...Abstractos import Globales

import random
import graphviz

class Asignacion(Expresion):
#constructor de la sentencia if, sobrecarga operadores derecho e izquierdo
    def __init__(self, id, expresion, tipo, fila, columna):
        self.ID = id
        self.Expresion = expresion
        self.Tipo = tipo
        self.Fila = fila
        self.Columna = columna
    #Interfaz para la ejecucion de la sentencia
    def execute(self, entorno):
        valorExp = self.Expresion.execute(entorno)

        if valorExp.Valor != "ERROR":

            # Para variables, arreglos - Verificar tipo si viene
            if self.Tipo != None:
                if valorExp.Tipo != self.Tipo:

                    if valorExp.Tipo == "struct":
                        objStruct = valorExp.Valor
                        if objStruct.ID != self.Tipo:
                            Globales.tablaErrores.append(Error(f"Asignacion invalida: {self.Tipo} con {objStruct.ID}", self.Fila, self.Columna))
                            return
                    else:
                        Globales.tablaErrores.append(Error(f"Asignacion invalida: {self.Tipo} con {valorExp.Tipo}", self.Fila, self.Columna))
                        return

            # Agregar a la tabla de simbolos
            entorno.setSimbolo(self.ID, valorExp, valorExp.Tipo, self.Fila, self.Columna)

    def getAST(self, dot):
        idAsignacion = str(random.randint(1, 1000000000))
        idVariable = str(random.randint(1, 1000000000))
        idIgual = str(random.randint(1, 1000000000))
        idExp = str(random.randint(1, 1000000000))

        dot.node(idAsignacion, "Asignacion")
        dot.node(idVariable, self.ID)
        dot.node(idIgual, "=")
        dot.node(idExp, "expresion")

        dot.edge(idAsignacion, idVariable)
        dot.edge(idAsignacion, idIgual)
        dot.edge(idAsignacion, idExp)

        dot, IDDotExp = self.Expresion.getAST(dot)
        dot.edge(idExp, IDDotExp)

        if self.Tipo != None:
            id2Puntos = str(random.randint(1, 1000000000))
            idTipo = str(random.randint(1, 1000000000))
            
            dot.node(id2Puntos, ": :")
            dot.node(idTipo, self.Tipo)

            dot.edge(idAsignacion, id2Puntos)
            dot.edge(idAsignacion, idTipo)

        idPTComa = str(random.randint(1, 1000000000))
        dot.node(idPTComa, ";")
        dot.edge(idAsignacion, idPTComa)

        return dot, idAsignacion

                

            


#Importacion de clases abstractas para la implemenacion del acceso
from ..Abstractos.Expresion import *
from ..Abstractos.Retorno import *
from ..Abstractos.Error import *
from ..Abstractos import Globales

import graphviz
import random

class Simbolo(Expresion):

#constructor de la sentencia acceso, sobrecarga operadores derecho e izquierdo
    def __init__(self, valor, tipo, id, fila = None, columna = None):
        self.Valor = valor
        self.Tipo = tipo
        self.ID = id
        self.Fila = fila
        self.Columna = columna
#Interfaz para la ejecucion de la sentencia
    def execute(self, entorno):
        
        # Acceso de variables normales
        if self.Tipo == "ID":
            simbolo = entorno.getSimbolo(self.ID)
            if simbolo == None:
                Globales.tablaErrores.append(Error(f"No existe la variable: {self.ID}", self.Fila, self.Columna))
                return Retorno("ERROR", "Variable")
            return Retorno(simbolo.Valor, simbolo.Tipo)
        
        # Acceso a atributos Ej: Objeto.nombre
        elif self.Tipo == "struct":
            simbolo = entorno.getSimbolo(self.ID)
            if simbolo == None:
                Globales.tablaErrores.append(Error(f"No existe el struct: {self.ID}", self.Fila, self.Columna))
                return Retorno("ERROR", "Struct")
            
            objStruct = simbolo.Valor
            for attr in objStruct.Atributos:
                if attr.ID == self.Valor:

                    # Si son structs o arreglos obtener ref
                    if attr.Tipo == "ID":
                        objRef = attr.Valor.execute(entorno)
                        self.Valor = self.ID
                        return Retorno(objRef.Valor, objRef.Tipo)
                  
                    return Retorno(attr.Valor, attr.Tipo)
            
            Globales.tablaErrores.append(Error(f"Atributo no existe", self.Fila, self.Columna))
            return Retorno("ERROR", "Atributo")

        elif self.Tipo == "return":
            expResult = self.Valor.execute(entorno)
            return Retorno(expResult, "return")
            # expResult = self.Valor.execute(entorno)
            # return Retorno(expResult.Valor, expResult.Tipo)


        return Retorno(self.Valor, self.Tipo)

    def getAST(self, dot):
        idTipo = str(random.randint(1, 1000000000))
        idValor = str(random.randint(1, 1000000000))

        if self.Tipo == "Rango":
            id2Puntos = str(random.randint(1, 1000000000))
            idExpIzq = str(random.randint(1, 1000000000))
            idExpDer = str(random.randint(1, 1000000000))

            dot.node(idTipo, self.Tipo)
            dot.node(idExpIzq, "expresion")
            dot.node(id2Puntos, ":")
            dot.node(idExpDer, "expresion")

            dot.edge(idTipo, idExpIzq)
            dot.edge(idTipo, id2Puntos)
            dot.edge(idTipo, idExpDer)

            dot, IDDotExpIzq = self.Valor[0].getAST(dot)
            dot.edge(idExpIzq, IDDotExpIzq)

            dot, IDDotExpDer = self.Valor[1].getAST(dot)
            dot.edge(idExpDer, IDDotExpDer) 

        elif self.Tipo == "continue":
            idSentencia = str(random.randint(1, 1000000000))
            dot.node(idSentencia, "sentencia")
            dot.node(idTipo, self.Tipo)
            dot.edge(idSentencia, idTipo)
            return dot, idSentencia

        elif self.Tipo == "break":
            idSentencia = str(random.randint(1, 1000000000))
            dot.node(idSentencia, "sentencia")
            dot.node(idTipo, self.Tipo)
            dot.edge(idSentencia, idTipo)
            return dot, idSentencia

        elif self.Tipo == "return":
            idSentencia = str(random.randint(1, 1000000000))
            idExp = str(random.randint(1, 1000000000))
            dot.node(idSentencia, "sentencia")
            dot.node(idTipo, self.Tipo)
            dot.node(idExp, "expresion")

            dot.edge(idSentencia, idTipo)
            dot.edge(idSentencia, idExp)

            dot, IDDotExp = self.Valor.getAST(dot)
            dot.edge(idExp, IDDotExp)

            return dot, idSentencia

        else:
            dot.node(idTipo, self.Tipo)
            dot.node(idValor, str(self.Valor))
            dot.edge(idTipo, idValor)

        return dot, idTipo
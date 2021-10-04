from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *
from ...Abstractos import Globales

import random
import graphviz

class Parse(Expresion):
# Constructor para la conversion
    def __init__(self, tipoConv, expresion, fila, columna):
        self.TipoConversion = tipoConv
        self.Expresion = expresion
        self.Fila = fila
        self.Columna = columna
# Interfaz para la ejecucion
    def execute(self, entorno):
        exp = self.Expresion.execute(entorno)

        if exp.Valor != "ERROR":
# tipo del valor y la conversion
#
            if exp.Tipo == "struct" or exp.Tipo == "array":
                # Error si es tipo struct o array
                Globales.tablaErrores.append(Error(f"La conversión no es posible, el valor no es correcto", self.Fila, self.Columna))
                return Retorno("ERROR", "Parse")
                #
            try:
                # almacena el tipo de conversion
                if self.TipoConversion == "Int64":
                    return Retorno(int(exp.Valor), "Int64")
                # almacena el tipo de conversion Int64
                elif self.TipoConversion == "Float64":
                    return Retorno(float(exp.Valor), "Float64")
                # almacena el tipo de conversion Float64
                elif self.TipoConversion == "String":
                    return Retorno(str(exp.Valor), "String")
                else:
                    # Error
                    Globales.tablaErrores.append(Error(f"El tipo {self.TipoConversion} no es permitido en Parse, solo String y Numericos", self.Fila, self.Columna))
                    return Retorno("ERROR", "Parse")
            except:
                Globales.tablaErrores.append(Error(f"La conversión no es posible, el valor no es correcto", self.Fila, self.Columna))
                return Retorno("ERROR", "Parse")
        else:
            return Retorno("ERROR", "Parse")
# Manejo de AST
    def getAST(self, dot):
        #Memoria de almacenaje
        idFuncion = str(random.randint(1, 1000000000))
        idParse = str(random.randint(1, 1000000000))
        idParIzq = str(random.randint(1, 1000000000))
        idTipo = str(random.randint(1, 1000000000))
        idComa = str(random.randint(1, 1000000000))
        idParDer = str(random.randint(1, 1000000000))
        idExpresion = str(random.randint(1, 1000000000))
      #nodo tipo y nodo variable
        dot.node(idFuncion, "Funcion")
        dot.node(idParse, "Parse")
        dot.node(idParIzq, "(")
        dot.node(idTipo, self.TipoConversion)
        dot.node(idComa, ",")
        dot.node(idExpresion, "Expresion")
        dot.node(idParDer, ")")

        dot.edge(idFuncion, idParse)
        dot.edge(idFuncion, idParIzq)
        dot.edge(idFuncion, idTipo)
        dot.edge(idFuncion, idComa)
        dot.edge(idFuncion, idExpresion)
        dot.edge(idFuncion, idParDer)

        dot, IDDotExp = self.Expresion.getAST(dot)
        dot.edge(idExpresion, IDDotExp)

        return dot, idFuncion

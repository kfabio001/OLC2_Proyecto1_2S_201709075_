from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *
from ...Abstractos import Globales

import random
import graphviz

class Trunc(Expresion):
#Constructor de la funcion nativa trunc, sobrecarga la expresion, fila y columna
    def __init__(self, tipoConv, expresion, fila, columna):
        self.TipoConversion = tipoConv
        self.Expresion = expresion
        self.Fila = fila
        self.Columna = columna
     #Funcion que ejecuta el modo trunc
    def execute(self, entorno):
        exp = self.Expresion.execute(entorno)
    #Variable que contiene la expresion final
        if exp.Valor != "ERROR":
            if exp.Tipo == "Float64": 
                try:
                    #Vierifica el tipo para convertir
                    if self.TipoConversion == "Int64":
                        #Concatena la salida
                        return Retorno(int(exp.Valor), "Int64")
                    else:
                        Globales.tablaErrores.append(Error(f"El tipo {self.TipoConversion} no es permitido en Trunc, solo Int64", self.Fila, self.Columna))
                        return Retorno("ERROR", "Trunc")
                except:
                    #Vierifica el tipo para convertir
                    Globales.tablaErrores.append(Error(f"Realizar trunc no es posible, el valor no es correcto", self.Fila, self.Columna))
                    return Retorno("ERROR", "Trunc")
            else:
                Globales.tablaErrores.append(Error(f"El tipo de la expresion {exp.Tipo} no es permitido en Trunc, solo Float64", self.Fila, self.Columna))
                return Retorno("ERROR", "Trunc")
        else:
            return Retorno("ERROR", "Trunc")

    def getAST(self, dot):
          #memoria para los ids de los nodos del arbol
        idFuncion = str(random.randint(1, 1000000000))
        idTrunc = str(random.randint(1, 1000000000))
        idParIzq = str(random.randint(1, 1000000000))
        idTipo = str(random.randint(1, 1000000000))
        idComa = str(random.randint(1, 1000000000))
        idParDer = str(random.randint(1, 1000000000))
        idExpresion = str(random.randint(1, 1000000000))
      #formacion de los nodos para toda la informacion
        dot.node(idFuncion, "Funcion")
        dot.node(idTrunc, "Trunc")
        dot.node(idParIzq, "(")
        dot.node(idTipo, self.TipoConversion)
        dot.node(idComa, ",")
        dot.node(idExpresion, "Expresion")
        dot.node(idParDer, ")")
#generacion de las aristas de los nodoas
        dot.edge(idFuncion, idTrunc)
        dot.edge(idFuncion, idParIzq)
        dot.edge(idFuncion, idTipo)
        dot.edge(idFuncion, idComa)
        dot.edge(idFuncion, idExpresion)
        dot.edge(idFuncion, idParDer)

        dot, IDDotExp = self.Expresion.getAST(dot)
        dot.edge(idExpresion, IDDotExp)
#rentorno del codigo dot
        return dot, idFuncion
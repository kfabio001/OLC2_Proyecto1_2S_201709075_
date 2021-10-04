from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *

import random
import graphviz
#
class Funcion(Expresion):
#Inicializacion sobre carga identificador, parametros, instruccion, fila, columna
    def __init__(self, idFuncion, parametros, instrucciones, fila, columna):
        self.IDFuncion = idFuncion
        self.Parametros = parametros
        self.Instrucciones = instrucciones
        self.Fila = fila
        self.Columna = columna
# ejecucion de la funcion con sobre carga
    def execute(self, entorno):
        entorno.setFuncion(self.IDFuncion, self, self.Fila, self.Columna)
# otencion de funcion para ast con memoria selecconada
    def getAST(self, dot):
        # declaracion de la funcion
        idDecl = str(random.randint(1, 1000000000))
        idFunction = str(random.randint(1, 1000000000))
        idVariable = str(random.randint(1, 1000000000))
        idParIzq = str(random.randint(1, 1000000000))
        idParametros = str(random.randint(1, 1000000000))
        idParDer = str(random.randint(1, 1000000000))
        idBloque = str(random.randint(1, 1000000000))
        idEnd = str(random.randint(1, 1000000000))
# Obtencion de los datos de cada nodo
        dot.node(idDecl, "Declaracion")
        dot.node(idFunction, "Funcion")
        dot.node(idVariable, self.IDFuncion)
        dot.node(idParIzq, "(")
# Obtencion de los datos de cada edge
        dot.edge(idDecl, idFunction)
        dot.edge(idDecl, idVariable)
        dot.edge(idDecl, idParIzq)
        
# Sobre carga de los parametros de la funcion
        if self.Parametros:
            dot.node(idParametros, "Parametros")
            dot.edge(idDecl, idParametros)
#Recorrido de cada parametro enlistado en el
            for i, param in enumerate(self.Parametros):
                dot, IDDotParam = param.getAST(dot)
                dot.edge(idParametros, IDDotParam)
#Listado de parametros sobrecargados
                if i < len(self.Parametros) - 1:
                    idComa = str(random.randint(1, 1000000000))
                    dot.node(idComa, ",")
                    dot.edge(idParametros, idComa)
#       
        dot.node(idParDer, ")")
        dot.edge(idDecl, idParDer)
#Bloque de parametros si no es vacio
        dot.node(idBloque, "Bloque")
        dot.edge(idDecl, idBloque)
        dot, IDDotBloque = self.Instrucciones.getAST(dot)
        dot.edge(idBloque, IDDotBloque)
#Reservada end
        dot.node(idEnd, "End;")
        dot.edge(idDecl, idEnd)

        return dot, idDecl

        
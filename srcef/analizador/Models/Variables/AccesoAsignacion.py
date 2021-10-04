#Importacion de clases abstractas para la implemenacion del if
from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *
from ...Models.Variables.Acceso import *
from ...Abstractos import Globales

import random
import graphviz

class AccesoAsignacion(Expresion):
#constructor de la sentencia if, sobrecarga operadores derecho e izquierdo
    def __init__(self, acceso, expresion, tipo, fila, columna):
        self.AccesoSimbolo = acceso
        self.Expresion = expresion
        self.Tipo = tipo
        self.Fila = fila
        self.Columna = columna
#Interfaz para la ejecucion de la sentencia
    def execute(self, entorno):
        valorExp = self.Expresion.execute(entorno)
        if valorExp.Valor != "ERROR":
            if self.AccesoSimbolo.Tipo == "mix":
                
                pilaAcceso = Acceso.getPila(self.AccesoSimbolo.Objeto)
                simboloActual = None
                simboloAnterior = None

                for i, acceso in enumerate(pilaAcceso):
                    if i == len(pilaAcceso) - 1:
                        # Cambiar el valor objetivo
                        # attr.id
                        if simboloActual.Tipo == "struct" and type(acceso.Objeto) == str:
                            AccesoAsignacion.setValorAttr(simboloActual, acceso.Objeto, self.Tipo, valorExp)
                        # attr.id[]
                        if simboloActual.Tipo == "struct" and acceso.Tipo == "array":
                            idAttr = acceso.Objeto.Array
                            atributo = Acceso.getValorAttr(simboloActual, idAttr, entorno)
                            AccesoAsignacion.setValorIndice(acceso.Objeto, atributo, valorExp, self.Tipo, entorno)
                        return
                    else:
                        # Acceder a los objetos
                        if simboloActual == None:
                            # Primer ID o arreglo
                            simboloActual = acceso.execute(entorno)
                        else:
                            # Caso obj.attributo
                            if simboloActual.Tipo == "struct" and type(acceso.Objeto) == str:
                                simboloActual = Acceso.getValorAttr(simboloActual, acceso.Objeto, entorno)       
                            # Caso obj.array[1]
                            if simboloActual.Tipo == "struct" and acceso.Tipo == "array":
                                idAttr = acceso.Objeto.Array
                                atributo = Acceso.getValorAttr(simboloActual, idAttr, entorno)
                                valorIndice = Acceso.getValorIndice(acceso.Objeto, atributo, entorno)
                                simboloActual = valorIndice

            else:
                # Acceso simple array[][][]
                arrayObj = self.AccesoSimbolo.Objeto
                simboloArray = entorno.getSimbolo(arrayObj.Array)
                AccesoAsignacion.setValorIndice(arrayObj, simboloArray, valorExp, self.Tipo, entorno)
        
    def setValorAttr(simbolo, id, tipo, expresion):
        objStruct = simbolo.Valor
        for attr in objStruct.Atributos:
            if attr.ID == id:
                # Se cambia por referencia
                attr.Valor = expresion.Valor
                attr.Tipo = expresion.Tipo

    def setValorIndice(array, simbolo, expresion, tipo, entorno):
        arreglo = simbolo.Valor
        indicesAcceso = []
        for indice in array.Indices:
            exp = indice.execute(entorno)
            if exp.Valor == "ERROR" or exp.Tipo != "Int64" or exp.Valor == 0:
                Globales.tablaErrores.append(Error(f"El indice no es Int64, es 0 o antecede un error", array.Fila, array.Columna))
                return Retorno("ERROR", "indice")
            else:
                indicesAcceso.append(exp.Valor)

        while len(indicesAcceso) > 0: # Iterar hasta completar los indices
            indiceActual = indicesAcceso[0]
            try:

                if len(indicesAcceso) == 1:
                    # Ultimo indice hacer cambio
                    arreglo.Array[indiceActual-1].Valor = expresion.Valor
                    arreglo.Array[indiceActual-1].Tipo = expresion.Tipo
                    return

                objIndice = arreglo.Array[indiceActual-1]

                del indicesAcceso[0] # Borra el indice ya procesado
                arreglo = objIndice.Valor # Nuevo valor a iterar
            except:
                Globales.tablaErrores.append(Error(f"Error al acceder al indice", array.Fila, array.Columna))
                return Retorno("ERROR", "indice")

    def getAST(self, dot):
        idAsignacion = str(random.randint(1, 1000000000))
        idIgual = str(random.randint(1, 1000000000))
        idExp = str(random.randint(1, 1000000000))

        dot.node(idAsignacion, "Asignacion")

        dot, IDDotAcceso = self.AccesoSimbolo.getAST(dot)
        dot.edge(idAsignacion, IDDotAcceso)

        dot.node(idIgual, "=")
        dot.node(idExp, "expresion")

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

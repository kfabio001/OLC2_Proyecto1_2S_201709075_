#Importacion de clases abstractas para la implemenacion del acceso
from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *
from ...Models.Variables.Arreglo import *
from ...Abstractos import Globales

import random
import graphviz

class Acceso(Expresion):
#constructor de la sentencia acceso, sobrecarga operadores derecho e izquierdo
    def __init__(self, objeto, tipo, fila, columna):
        self.Objeto = objeto
        self.Tipo = tipo
        self.Fila = fila
        self.Columna = columna
#Interfaz para la ejecucion de la sentencia
    def execute(self, entorno):
        
        if self.Tipo == "ID":
            # Acceso singular - id
            simbolo = entorno.getSimbolo(self.Objeto)
            if simbolo == None:
                Globales.tablaErrores.append(Error(f"No existe la variable: {self.Objeto}", self.Fila, self.Columna))
                return Retorno("ERROR", "Variable")
            return Retorno(simbolo.Valor, simbolo.Tipo)

        elif self.Tipo == "array":
            # Acceso singular - arreglo
            if not isinstance(self.Objeto.Array, list):
                # Caso ID[1][2]
                objArray = entorno.getSimbolo(self.Objeto.Array)
                valorIndice = Acceso.getValorIndice(self.Objeto, objArray, entorno)
                return valorIndice
            else:
                # Declaracion dentro
                return self.Objeto.execute(entorno)

        elif self.Tipo == "mix":
            # Obtener pila de acceso
            pilaAcceso = Acceso.getPila(self.Objeto)
            simboloActual = None

            for acceso in pilaAcceso:
                #print(acceso.Objeto)
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

            return simboloActual

    # Obtener el valor del atributo
    def getValorAttr(simbolo, id, entorno):
        objStruct = simbolo.Valor
        for attr in objStruct.Atributos:
            if attr.ID == id:
                if attr.Tipo == "ID":
                    objRef = attr.Valor.execute(entorno)
                    return Retorno(objRef.Valor, objRef.Tipo)
                else:
                    return Retorno(attr.Valor, attr.Tipo)

    def getValorIndice(array, simbolo, entorno):
        arreglo = simbolo.Valor
        indicesAcceso = []
        for indice in array.Indices:
            exp = indice.execute(entorno)
            
            if exp.Valor == "ERROR" or (exp.Tipo != "Int64" and exp.Tipo != "Rango") or exp.Valor == 0:
                Globales.tablaErrores.append(Error(f"El indice no es Int64 ni Rango, es 0 o antecede un error", array.Fila, array.Columna))
                return Retorno("ERROR", "indice")
            else:
                indicesAcceso.append(exp.Valor)

        valorIndice = None
        while len(indicesAcceso) > 0: # Iterar hasta completar los indices
            indiceActual = indicesAcceso[0]   

            if isinstance(indiceActual, list):
                # Acceso rango [2:4]
                inicio = indiceActual[0]
                fin = indiceActual[1]

                if inicio != 'begin' and inicio != 'end': 
                    inicio = inicio.execute(entorno)
                    inicio.Valor -= 1
                else: inicio = Retorno(0, 'Int64')

                if fin != 'begin' and fin != 'end' : 
                    fin = fin.execute(entorno)
                else: fin = Retorno(len(arreglo.Array), 'Int64')
                
                arrayResultante = arreglo.Array[inicio.Valor:fin.Valor]
                nuevoArray = Arreglo(arrayResultante, "array", None, arreglo.Fila, arreglo.Columna)
                return Retorno(nuevoArray, "array")
            else:
                # Acceso numerico [3]
                try:
                    objIndice = arreglo.Array[indiceActual-1]
                    valorIndice = objIndice
                    
                    del indicesAcceso[0] # Borra el indice ya procesado
                    arreglo = valorIndice.Valor # Nuevo valor a iterar
                except:
                    Globales.tablaErrores.append(Error(f"Error al acceder al indice", array.Fila, array.Columna))
                    return Retorno("ERROR", "indice")

        return Retorno(valorIndice.Valor, valorIndice.Tipo)

    def getPila(accesos):
        pila = []
        if not isinstance(accesos,list):
            pila.append(accesos)
            return pila
        for acceso in accesos:
            if acceso.Tipo == "mix":
                pila.extend(Acceso.getPila(acceso.Objeto)) 
            else:
                pila.append(acceso)
        return pila

    def getAST(self, dot):
        idAcceso = str(random.randint(1, 1000000000))
        dot.node(idAcceso, "Acceso")

        if self.Tipo == "ID":
            idVariable = str(random.randint(1, 1000000000))
            dot.node(idVariable, self.Objeto)
            dot.edge(idAcceso, idVariable)
        
        elif self.Tipo == "array":
            idArreglo = str(random.randint(1, 1000000000))
            dot.node(idArreglo, "arreglo")
            dot.edge(idAcceso, idArreglo)

            dot, IDDotArreglo = self.Objeto.getAST(dot)
            dot.edge(idArreglo, IDDotArreglo)
        
        elif self.Tipo == "mix":
            idMix = str(random.randint(1, 1000000000))
            dot.node(idMix, "mix")
            dot.edge(idAcceso, idMix)

            dot, IDDotAcc1 = self.Objeto[0].getAST(dot)
            dot.edge(idMix, IDDotAcc1)

            idPunto = str(random.randint(1, 1000000000))
            dot.node(idPunto, ".")
            dot.edge(idMix, idPunto)

            dot, IDDotAcc2 = self.Objeto[1].getAST(dot)
            dot.edge(idMix, IDDotAcc2)

        return dot, idAcceso
            

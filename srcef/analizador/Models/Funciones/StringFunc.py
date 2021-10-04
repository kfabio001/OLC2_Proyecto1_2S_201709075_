from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *
from ...Abstractos import Globales

import random
import graphviz

class StringFunc(Expresion):
#Constructor de la funcion nativa string, sobrecarga la expresion, fila y columna
    def __init__(self, expresion, fila, columna):
        self.Expresion = expresion
        self.Fila = fila
        self.Columna = columna
    #Funcion que ejecuta para parsear el contendido
    def execute(self, entorno):
        exp = self.Expresion.execute(entorno)
        stringConv = ""
        #Variable que contiene la expresion final
        if exp.Valor == "ERROR":
            return Retorno("ERROR", "stringFunc")
        else:
            #Vierifica el tipo para convertir
            if exp.Tipo == "Nulo": stringConv += "nothing"
            elif exp.Tipo == "Bool": stringConv += "true" if (exp.Valor == True) else "false"
            elif exp.Tipo == "struct": stringConv += self.stringStruct(exp, self.Expresion, entorno)
            elif exp.Tipo == "array": stringConv += self.stringArreglo(exp, entorno)
            else: stringConv += str(exp.Valor)
            #Concatena la salida
        return Retorno(stringConv, "String")
    # Verifica el struct y lo recorre
    def stringStruct(self, objeto, simbolo, entorno = None):
        #Almacena el valor del objeto
        objStruct = objeto.Valor   
        # Concatenacion de la salida
        salida = objStruct.ID + "("
        for i, attr in enumerate(objStruct.Atributos):
            #Si es array se recorre recursivamente
            if attr.Tipo == "array": salida += self.stringArreglo(attr, entorno)
            #SI es struct se recorre recursivamente
            elif attr.Tipo == "struct": salida += self.stringStruct(attr, simbolo, entorno)
            #
            else: salida += str(attr.Valor)
            if i < len(objStruct.Atributos) - 1: salida += ","
        salida += ")"
        #retorno de la salida a concatenar
        return salida
    # String a convertir desde un arreglo
    def stringArreglo(self, objeto, entorno = None):
        arreglo = objeto.Valor.Array

        salida = "["
    #Recorrido del arreglo por cada objeto
        for i, item in enumerate(arreglo):
            #Si es array se recorre recursivamente
            if item.Tipo == "array": salida += self.stringArreglo(item, entorno)
              #SI es struct se recorre recursivamente
            elif item.Tipo == "struct": salida += self.stringStruct(item, objeto, entorno)
            else: salida += str(item.Valor)
            if i < len(arreglo) - 1: salida += ","
        salida += "]" 
# String a convertir desde un struct
        return salida
    
    def getAST(self, dot):
        #memoria para los ids de los nodos del arbol
        idFuncion = str(random.randint(1, 1000000000))
        idParse = str(random.randint(1, 1000000000))
        idParIzq = str(random.randint(1, 1000000000))
        idParDer = str(random.randint(1, 1000000000))
        idExpresion = str(random.randint(1, 1000000000))
        #formacion de los nodos para toda la informacion
        dot.node(idFuncion, "Funcion")
        dot.node(idParse, "String")
        dot.node(idParIzq, "(")
        dot.node(idExpresion, "Expresion")
        dot.node(idParDer, ")")
      #generacion de las aristas de los nodoas
        dot.edge(idFuncion, idParse)
        dot.edge(idFuncion, idParIzq)
        dot.edge(idFuncion, idExpresion)
        dot.edge(idFuncion, idParDer)

        dot, IDDotExp = self.Expresion.getAST(dot)
        dot.edge(idExpresion, IDDotExp)
        #rentorno del codigo dot
        return dot, idFuncion
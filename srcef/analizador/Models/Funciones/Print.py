from ...Abstractos.Expresion import *
from ...Abstractos import Globales

import random
import graphviz

class Print(Expresion):
# Constructor para el manejo de expresiones
    def __init__(self, expresion, tipo):
        self.Expresiones = expresion
        self.Tipo = tipo
    #Metodo nativo para ejecutar
    def execute(self, entorno):
    #Recorre para obtener el valor en el entorno
        salida = ""
        error = False
    # Recorrido
        for exp in self.Expresiones:  
            #Variable que lleva el valor de la expresion          
            valorExp = exp.execute(entorno)
            #Si es error continua is guarda el error
            if valorExp.Valor == "ERROR":
                error = True
                break
            #Si no Verigica el Tipo de la expresion y concatena el valor si es nulo o booleano
            else:
                if valorExp.Tipo == "Nulo": salida += "nothing"
                elif valorExp.Tipo == "Bool": salida += "true" if (valorExp.Valor == True) else "false"
                #Si es estruc llama a la funcion que imprimira
                elif valorExp.Tipo == "struct": salida += Print.printStruct(valorExp, exp, entorno)
                elif valorExp.Tipo == "array": salida += Print.printArreglo(valorExp, entorno)                
                else: salida += str(valorExp.Valor)
    #concatenacion de la salida
        if not error:
            if self.Tipo == "nl": 
                Globales.salidaPrints += salida + "\n"  
            else:
                Globales.salidaPrints += salida
    #Funcion que concatena el struc a imprimir
    def printStruct(objeto, simbolo, entorno = None):
        #Guarda el valor en la funcion objeto
        objStruct = objeto.Valor
    #Concatena la salida recorriendo el struct
        salida = objStruct.ID + "("
    # Recorrido de los atributos del struct
        for i, attr in enumerate(objStruct.Atributos):
            if attr.Tipo == "array": salida += Print.printArreglo(attr, entorno)
            elif attr.Tipo == "struct": salida += Print.printStruct(attr, simbolo, entorno)
            else: salida += str(attr.Valor)
            if i < len(objStruct.Atributos) - 1: salida += ","
        salida += ")"

        return salida
#Funcion que recorre el arreglo a imprimir
    def printArreglo(objeto, entorno = None):
        #Almacena el objeto en el arreglo
        arreglo = objeto.Valor.Array

        salida = "["
        # Recorrido de los objetos en el arrreglo
        for i, item in enumerate(arreglo):
            if item.Tipo == "array": salida += Print.printArreglo(item, entorno)
            elif item.Tipo == "struct": salida += Print.printStruct(item, objeto, entorno)
            else: salida += str(item.Valor)
            if i < len(arreglo) - 1: salida += ","
        salida += "]" 
#Retorno de la salida al terminar el recorrido
        return salida
# Funcion para obtener ast de la funcion
    def getAST(self, dot):
        idFuncion = str(random.randint(1, 1000000000))
        idPrint = str(random.randint(1, 1000000000))
        idParIzq = str(random.randint(1, 1000000000))
        idParDer = str(random.randint(1, 1000000000))
        idExpresiones = str(random.randint(1, 1000000000))
        idPtComa = str(random.randint(1, 1000000000))
#nodo tipo y nodo variable
        dot.node(idFuncion, "Funcion")
        dot.node(idPrint, "println" if self.Tipo == "nl" else "print")
        dot.node(idParIzq, "(")
        dot.node(idExpresiones, "Expresiones")
        dot.node(idParDer, ")")
        dot.node(idPtComa, ";")
        
        dot.edge(idFuncion, idPrint)
        dot.edge(idFuncion, idParIzq)
        dot.edge(idFuncion, idExpresiones)

        for exp in self.Expresiones:
            idExp = str(random.randint(1, 1000000000))
            dot.node(idExp, "Expresion")
            dot.edge(idExpresiones, idExp)

            dot, IDDotExp = exp.getAST(dot)
            dot.edge(idExp, IDDotExp)

        dot.edge(idFuncion, idParDer)
        dot.edge(idFuncion, idPtComa)
        
        return dot, idFuncion
       
        
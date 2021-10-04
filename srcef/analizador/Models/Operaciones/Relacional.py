from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *
from ...Abstractos import Globales

import random
import graphviz

class Relacional(Expresion):
#constructor de las expresiones relacionales, sobrecarga operadores derecho e izquierdo
    def __init__(self, opIzq, opDer, operacion, fila, columna):
        self.OpIzq = opIzq
        self.OpDer = opDer
        self.Operacion = operacion
        self.Fila = fila
        self.Columna = columna
#Interfaz para la ejecucion
    def execute(self, entorno):
        valorIzq = self.OpIzq.execute(entorno)
        valorDer = self.OpDer.execute(entorno)
        resultado = Retorno(False, "Bool")
        # Verificacin de  errores en la expresion
        if valorIzq.Valor == "ERROR" or valorDer.Valor == "ERROR":
            return Retorno("ERROR", "Expresion") 
        # >
        if self.Operacion == ">":
            #Verificacion de dos operadosres
            try:
                #Almacena booleano
                resultado.Valor = valorIzq.Valor > valorDer.Valor
            except:
                resultado = Retorno("ERROR", ">")
                print(valorIzq.Valor, valorDer.Valor)
                #Guarda el error
                Globales.tablaErrores.append(Error(f"Mayor '>' invalido: {valorIzq.Tipo} con {valorDer.Tipo}", self.Fila, self.Columna))

        # <
        elif self.Operacion == "<":
            #almacena el booleano
            try:
                #Verificacion de dos operadosres
                resultado.Valor = valorIzq.Valor < valorDer.Valor
            except:
                resultado = Retorno("ERROR", "<")
                #Guarda el error
                Globales.tablaErrores.append(Error(f"Menor '<' invalido: {valorIzq.Tipo} con {valorDer.Tipo}", self.Fila, self.Columna))

        # >=
        elif self.Operacion == ">=":
#Verificacion de dos operadosres
            try:
                #almacena el booleano
                resultado.Valor = valorIzq.Valor >= valorDer.Valor
            except:
                resultado = Retorno("ERROR", ">=")
                #Guarda el error
                Globales.tablaErrores.append(Error(f"Mayor igual '>=' invalido: {valorIzq.Tipo} con {valorDer.Tipo}", self.Fila, self.Columna))

        # <=
        elif self.Operacion == "<=":
        #Verificacion de dos operadosres
            try:
                #almacena el booleano
                resultado.Valor = valorIzq.Valor <= valorDer.Valor
            except:
                resultado = Retorno("ERROR", "<=")
                #Guarda el error
                Globales.tablaErrores.append(Error(f"Menor igual '<=' invalido: {valorIzq.Tipo} con {valorDer.Tipo}", self.Fila, self.Columna))

        # =
        elif self.Operacion == "==":
            #Verificacion de dos operadosres
            try:
                #almacena el booleano
                resultado.Valor = valorIzq.Valor == valorDer.Valor
            except:
                resultado = Retorno("ERROR", "==")
                #Guarda el error
                Globales.tablaErrores.append(Error(f"Igualdad '==' invalida: {valorIzq.Tipo} con {valorDer.Tipo}", self.Fila, self.Columna))

        # !=
        elif self.Operacion == "!=":
            #Verificacion de dos operadosres
            try:
                #almacena el booleano
                resultado.Valor = valorIzq.Valor != valorDer.Valor
            except:
                resultado = Retorno("ERROR", "!=")
                #Guarda el error
                Globales.tablaErrores.append(Error(f"Igualdad '!=' invalida: {valorIzq.Tipo} con {valorDer.Tipo}", self.Fila, self.Columna))
        #Retorna el booleano
        return resultado

    def getAST(self, dot):
        idRelacional = str(random.randint(1, 1000000000))
        idOperacion = str(random.randint(1, 1000000000))
 
        dot.node(idRelacional, "ExpresionR")
        
        dot, IDDotIzq = self.OpIzq.getAST(dot)
        dot.edge(idRelacional, IDDotIzq)

        dot.node(idOperacion, self.Operacion)
        dot.edge(idRelacional, idOperacion)

        if self.OpDer:
            dot, IDDotDer = self.OpDer.getAST(dot)
            dot.edge(idRelacional, IDDotDer)

        return dot, idRelacional
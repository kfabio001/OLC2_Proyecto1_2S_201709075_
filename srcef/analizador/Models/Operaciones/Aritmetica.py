from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *
from ...Abstractos import Globales

import random
import graphviz

class Aritmetica(Expresion):
#constructor de las expresiones aritmenticas, sobrecarga operadores derecho e izquierdo
    def __init__(self, opIzq, opDer, operacion, fila, columna):
        self.OpIzq = opIzq
        self.OpDer = opDer
        self.Operacion = operacion
        self.Fila = fila
        self.Columna = columna
#Interfaz para la ejecucion
    def execute(self, entorno):
        valorIzq = self.OpIzq.execute(entorno)
        valorDer = None
        
        #Validacion de dos operadores correctos
        if self.OpDer:
            valorDer = self.OpDer.execute(entorno)
            if valorDer.Valor == "ERROR":
                return Retorno("ERROR", "Expresion") 
        if valorIzq.Valor == "ERROR":
            return Retorno("ERROR", "Expresion") 
        resultado = Retorno(0, "")

        # +
        if self.Operacion == "+":

            try:
                #Caso suma de dos numeros
                resultado.Valor = valorIzq.Valor + valorDer.Valor
            except:
                pass
                # Tipo de datos y parseo entre operadores derecho e izquierdo
            if (valorIzq.Tipo != "Int64" and valorIzq.Tipo != "Float64") or (valorDer.Tipo != "Int64" and valorDer.Tipo != "Float64"):
                resultado = Retorno("ERROR", "+")
                Globales.tablaErrores.append(Error(f"Suma invalida: {valorIzq.Tipo} con {valorDer.Tipo}", self.Fila, self.Columna))
                #Caso dos float
            else:
                if valorIzq.Tipo == "Float64" or valorDer.Tipo == "Float64":
                    resultado.Tipo = "Float64"
                else:
                    #Caso de dos int
                    resultado.Tipo = "Int64"

        # -
        elif self.Operacion == "-":
    
            try:
                #Caso resta de dos numeros
                resultado.Valor = valorIzq.Valor - valorDer.Valor
            except:
                pass
                #Verficacion tipo de dato y parseo
            if (valorIzq.Tipo != "Int64" and valorIzq.Tipo != "Float64") or (valorDer.Tipo != "Int64" and valorDer.Tipo != "Float64"):
                resultado = Retorno("ERROR", "-")
                Globales.tablaErrores.append(Error(f"Resta invalida: {valorIzq.Tipo} con {valorDer.Tipo}", self.Fila, self.Columna))
            else:
                #Caso dos float
                if valorIzq.Tipo == "Float64" or valorDer.Tipo == "Float64":
                    resultado.Tipo = "Float64"
                else:
                    #Caso dos int
                    resultado.Tipo = "Int64"

        # *
        elif self.Operacion == "*":

            #Caso en que se envien dos strings
            if valorIzq.Tipo == "String" and valorDer.Tipo == "String":
                resultado.Valor = valorIzq.Valor + valorDer.Valor
                resultado.Tipo = "String"
            else:
                # Caso que se envien dos enteros
                try:
                    resultado.Valor = valorIzq.Valor * valorDer.Valor
                except:
                    pass
                    # Tipo de datos y parseo entre operadores derecho e izquierdo
                if (valorIzq.Tipo != "Int64" and valorIzq.Tipo != "Float64") or (valorDer.Tipo != "Int64" and valorDer.Tipo != "Float64"):
                    resultado = Retorno("ERROR", "*")
                    Globales.tablaErrores.append(Error(f"Multiplicacion invalida: {valorIzq.Tipo} con {valorDer.Tipo}", self.Fila, self.Columna))
                else:
                    #Caso dos float
                    if valorIzq.Tipo == "Float64" or valorDer.Tipo == "Float64":
                        resultado.Tipo = "Float64"
                    else:
                        #Caso dos int
                        resultado.Tipo = "Int64"

        # /
        elif self.Operacion == "/":

            try:
                #Caso en que se dividan dos enteros
                resultado.Valor = valorIzq.Valor / valorDer.Valor
                #parseo a float
                resultado.Tipo = "Float64"
            except:
                pass
                # Tipo de datos y parseo entre operadores derecho e izquierdo
            if (valorIzq.Tipo != "Int64" and valorIzq.Tipo != "Float64") or (valorDer.Tipo != "Int64" and valorDer.Tipo != "Float64"):
                resultado = Retorno("ERROR", "/")
                Globales.tablaErrores.append(Error(f"Division invalida: {valorIzq.Tipo} con {valorDer.Tipo}", self.Fila, self.Columna))

        # --
        elif self.Operacion == "umenos":
            # Caso expresion negativo
            try:
                #numero multiplicado por -1
                resultado.Valor = valorIzq.Valor * -1
                resultado.Tipo = valorIzq.Tipo
            except:
                pass
                #Verificacion de tipo y parseo
            if valorIzq.Tipo != "Int64" and valorIzq.Tipo != "Float64":
                resultado = Retorno("ERROR", "umenos")
                Globales.tablaErrores.append(Error(f"Negacion numerica invalida: {valorIzq.Tipo}", self.Fila, self.Columna))

        # ``^
        elif self.Operacion == "^":
            
            # Caso que se ele ve un string
            if valorIzq.Tipo == "String" and valorDer.Tipo == "Int64":
                #Concatenacion de la variable
                resultado.Valor = ""
                resultado.Tipo = "String"
                for x in range(int(valorDer.Valor)):
                    resultado.Valor += valorIzq.Valor
            else:
                # Caso que se eleven numeros
                try:
                    
                    resultado.Valor = valorIzq.Valor ** valorDer.Valor
                except:
                    pass
# Tipo de datos y parseo entre operadores derecho e izquierdo
                if (valorIzq.Tipo != "Int64" and valorIzq.Tipo != "Float64") or (valorDer.Tipo != "Int64" and valorDer.Tipo != "Float64"):
                    resultado = Retorno("ERROR", "^")
                    Globales.tablaErrores.append(Error(f"Potencia invalida: {valorIzq.Tipo} con {valorDer.Tipo}", self.Fila, self.Columna))
                else:
                     #Caso dos float
                    if valorIzq.Tipo == "Float64" or valorDer.Tipo == "Float64":
                        resultado.Tipo = "Float64"
                         #Caso dos int
                    else:
                        resultado.Tipo = "Int64"

        # %
        elif self.Operacion == "%":
#Caso modulo de la division de dos numeros
            try:
                resultado.Valor = valorIzq.Valor % valorDer.Valor
            except:
                pass
 # Tipo de datos y parseo entre operadores derecho e izquierdo
            if (valorIzq.Tipo != "Int64" and valorIzq.Tipo != "Float64") or (valorDer.Tipo != "Int64" and valorDer.Tipo != "Float64"):
                resultado = Retorno("ERROR", "%")
                Globales.tablaErrores.append(Error(f"Modulo invalido: {valorIzq.Tipo} con {valorDer.Tipo}", self.Fila, self.Columna))
            else:
                #Caso dos float
                if valorIzq.Tipo == "Float64" or valorDer.Tipo == "Float64":
                    resultado.Tipo = "Float64"
                else:
                    #Caso dos int
                    resultado.Tipo = "Int64"

        return resultado
#retorno de la operacion aritmentica
    def getAST(self, dot):
        #memoria para los ids de los nodos del arbol
        idAritmetica = str(random.randint(1, 1000000000))
        idOperacion = str(random.randint(1, 1000000000))
 #formacion de los nodos para toda la informacion
        dot.node(idAritmetica, "ExpresionA")
        
        dot, IDDotIzq = self.OpIzq.getAST(dot)
        dot.edge(idAritmetica, IDDotIzq)
 #generacion de las aristas de los nodoas
        dot.node(idOperacion, self.Operacion)
        dot.edge(idAritmetica, idOperacion)

        if self.OpDer:
            dot, IDDotDer = self.OpDer.getAST(dot)
            dot.edge(idAritmetica, IDDotDer)
#rentorno del codigo dot
        return dot, idAritmetica
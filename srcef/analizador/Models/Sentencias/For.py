#Importacion de clases abstractas para la implementacion
from ...Abstractos.Expresion import *
from ...Abstractos.Retorno import *
from ...Abstractos.Error import *
from ...Models.Entorno import *
from ...Abstractos import Globales

import random
import graphviz

class For(Expresion):
#constructor de la funcion for, sobrecarga expresiones derecho e izquierdo
    def __init__(self, variable, expresion, instrucciones, fila, columna):
        self.Variable = variable
        self.Expresion = expresion
        self.Instrucciones = instrucciones
        self.Fila = fila
        self.Columna = columna
    #Interfaz para la ejecucion
    def execute(self, entorno):
        valorExp = self.Expresion.execute(entorno)
        if valorExp.Tipo != "Rango" and valorExp.Tipo != "String" and valorExp.Tipo != "array":
            Globales.tablaErrores.append(Error(f"La expresion del for no es valida: {valorExp.Tipo}", self.Fila, self.Columna))
            return
        if valorExp.Tipo == "String":
            # Declarar objeto
            indice = 0
            letra = Retorno(valorExp.Valor[indice], valorExp.Tipo)
            entornoFor = Entorno(entorno, "")
            entornoFor.setSimbolo(self.Variable, letra, letra.Tipo, self.Fila, self.Columna)
            
            while True:
                resultCorrida = self.Instrucciones.execute(entornoFor)
                
                # Sentencias de transferencia
                if resultCorrida != None:
                    if resultCorrida.Tipo == "continue":
                        # Actualizar iterador
                        iterador = entornoFor.getSimbolo(self.Variable)
                        if indice < len(valorExp.Valor)-1:
                            indice = indice + 1
                            iterador.Valor = valorExp.Valor[indice]
                        else: return
                        continue
                    elif resultCorrida.Tipo == "break":
                        return
                    elif resultCorrida.Tipo == "return":
                        return resultCorrida
                        
                # Actualizar iterador
                iterador = entornoFor.getSimbolo(self.Variable)
                if indice < len(valorExp.Valor)-1:
                    indice = indice + 1
                    iterador.Valor = valorExp.Valor[indice]
                else:
                    return
        
        # Para arreglo
        if valorExp.Tipo == "array":
            # Declarar objeto
            indice = 0
            item = valorExp.Valor.Array[indice]
            entornoFor = Entorno(entorno, "")
            entornoFor.setSimbolo(self.Variable, item, item.Tipo, self.Fila, self.Columna)
            
            while True:
                resultCorrida = self.Instrucciones.execute(entornoFor)

                # Sentencias de transferencia
                if resultCorrida != None:
                    if resultCorrida.Tipo == "continue":
                        # Actualizar iterador
                        iterador = entornoFor.getSimbolo(self.Variable)
                        if indice < len(valorExp.Valor.Array)-1:
                            indice = indice + 1
                            iterador = valorExp.Valor.Array[indice]
                            entornoFor.setSimbolo(self.Variable, iterador, iterador.Tipo, self.Fila, self.Columna)          
                        else: return
                        continue
                    elif resultCorrida.Tipo == "break":
                        return
                    elif resultCorrida.Tipo == "return":
                        return resultCorrida

                # Actualizar iterador
                iterador = entornoFor.getSimbolo(self.Variable)
                if indice < len(valorExp.Valor.Array)-1:
                    indice = indice + 1
                    iterador = valorExp.Valor.Array[indice]
                    entornoFor.setSimbolo(self.Variable, iterador, iterador.Tipo, self.Fila, self.Columna)          
                else:
                    return
            
        # Para rango
        if valorExp.Tipo == "Rango":
            inicio = valorExp.Valor[0]
            fin = valorExp.Valor[1]

            # Validacion palabras reservadas
            if inicio == 'begin' or inicio == 'end' or fin == 'begin' or fin == 'end' :
                Globales.tablaErrores.append(Error(f"Rango sin arreglo no acepta begin-end", self.Fila, self.Columna))
                return

            inicio = inicio.execute(entorno)
            fin = fin.execute(entorno)

            # Validacion tipos int
            if inicio.Tipo != "Int64" or fin.Tipo != "Int64":
                Globales.tablaErrores.append(Error(f"Rango solo acepta Int64", self.Fila, self.Columna))
                return
            elif fin.Valor < inicio.Valor:
                Globales.tablaErrores.append(Error(f"For unicamente ascendente", self.Fila, self.Columna))
                return
            
            entornoFor = Entorno(entorno, "")
            entornoFor.setSimbolo(self.Variable, inicio, inicio.Tipo, self.Fila, self.Columna)

            while True:    
                resultCorrida = self.Instrucciones.execute(entornoFor)

                # Sentencias de transferencia
                if resultCorrida != None:
                    if resultCorrida.Tipo == "continue":
                        # Actualizar iterador
                        iterador = entornoFor.getSimbolo(self.Variable)
                        if iterador.Valor < fin.Valor:
                            iterador.Valor = iterador.Valor + 1
                        else: return
                        continue
                    elif resultCorrida.Tipo == "break":
                        return
                    elif resultCorrida.Tipo == "return":
                        return resultCorrida

                # Actualizar iterador
                iterador = entornoFor.getSimbolo(self.Variable)
                if iterador.Valor < fin.Valor:
                    iterador.Valor = iterador.Valor + 1
                else:
                    return

    def getAST(self, dot):
        idCiclo = str(random.randint(1, 1000000000))
        idFor = str(random.randint(1, 1000000000))
        idVar = str(random.randint(1, 1000000000))
        idIN = str(random.randint(1, 1000000000))
        idExp = str(random.randint(1, 1000000000))
        idBloque = str(random.randint(1, 1000000000))
        idEND = str(random.randint(1, 1000000000))

        dot.node(idCiclo, "Sentencia")
        dot.node(idFor, "for")
        dot.node(idVar, self.Variable)
        dot.node(idIN, "in")
        dot.node(idExp, "Expresion")
        dot.node(idBloque, "Bloque")
        dot.node(idEND, "end;")

        dot.edge(idCiclo, idFor)
        dot.edge(idCiclo, idVar)
        dot.edge(idCiclo, idIN)
        dot.edge(idCiclo, idExp)
        dot.edge(idCiclo, idBloque)
        dot.edge(idCiclo, idEND)

        # Expresion
        dot, IDDotExp = self.Expresion.getAST(dot)
        dot.edge(idExp, IDDotExp)

        # Bloque
        dot, IDDotBloque = self.Instrucciones.getAST(dot)
        dot.edge(idBloque, IDDotBloque)

        return dot, idCiclo

                

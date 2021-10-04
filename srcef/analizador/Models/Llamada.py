#Importacion de clases abstractas para la implemenacion del acceso
from ..Abstractos.Expresion import *
from ..Abstractos.Retorno import *
from ..Abstractos.Error import *

from ..Models.Entorno import *
from ..Models.Variables.Struct import *

from ..Abstractos import Globales

from copy import copy, deepcopy
import math

class Llamada(Expresion):
#constructor de la sentencia acceso, sobrecarga operadores derecho e izquierdo
    def __init__(self, id, params, fila, columna):
        self.ID = id
        self.Params = params
        self.Fila = fila
        self.Columna = columna
    #Interfaz para la ejecucion de la sentencia
    def execute(self, entorno):
        llamada = entorno.getSimbolo(self.ID)

        if llamada != None:

            # Para structs
            if llamada.Tipo == "struct":
                structBase = llamada.Valor
                objeto = Struct(self.ID, structBase.Mutable, deepcopy(structBase.Atributos))
                
                for i in range(len(self.Params)):
                    valorParam = self.Params[i].execute(entorno)
                    
                    if objeto.Atributos[i].Tipo == "Any" or valorParam.Tipo == objeto.Atributos[i].Tipo or objeto.Atributos[i].TipoOrigen == "Any":
                        objeto.Atributos[i].Valor = valorParam.Valor
                        objeto.Atributos[i].Tipo = valorParam.Tipo
                    else:
                        
                        # Validacion pa structs
                        if valorParam.Tipo == "struct":
                            objStruct = valorParam.Valor
                            if objStruct.ID == objeto.Atributos[i].Tipo:
                                objeto.Atributos[i].Valor = valorParam.Valor
                                objeto.Atributos[i].Tipo = valorParam.Tipo
                        else:
                            Globales.tablaErrores.append(Error(f"El tipo del atributo no coincide: {objeto.Atributos[i].ID} con {valorParam.Tipo}", self.Fila, self.Columna))
                            return Retorno("ERROR", "struct")

                return Retorno(objeto, "struct")

            # Para funciones
            elif llamada.Tipo == "funcion":

                objFuncion = llamada.Valor
                entGlobal = entorno.getEntornoGlobal()

                if self.Params == None and objFuncion.Parametros == None:
                    resultado = objFuncion.Instrucciones.execute(entGlobal)
                    if resultado == None: return Retorno(None, "Nulo")
                    else: return resultado
                else:
                    if self.Params == None or objFuncion.Parametros == None or len(self.Params) != len(objFuncion.Parametros):
                        Globales.tablaErrores.append(Error(f"Parametros no coinciden", self.Fila, self.Columna))
                        return Retorno("ERROR", "indice")
                    else:      
                        
                        entornoFuncion = Entorno(entGlobal, "funcion")
                        indiceParam = 0

                        for paramExp in self.Params:
                            exp = paramExp.execute(entorno)
       
                            if exp.Tipo == "struct" or exp.Tipo == "array":
                                # Pasar ref
                                # struct
                                if exp.Tipo == "struct":
                                    paramFuncion = objFuncion.Parametros[indiceParam]
                                    if exp.Valor.ID == paramFuncion.IDTipo or paramFuncion.IDTipo == "Any":
                                        entornoFuncion.setSimbolo(paramFuncion.IDParam, exp, "struct", paramFuncion.Fila, paramFuncion.Columna)
                                        indiceParam += 1
                                    else:
                                        Globales.tablaErrores.append(Error(f"Tipos no coinciden", paramFuncion.Fila, paramFuncion.Columna))
                                        return Retorno("ERROR", "indice")
                                # array
                                elif exp.Tipo == "array":
                                    paramFuncion = objFuncion.Parametros[indiceParam]
                                    if paramFuncion.IDTipo == "Any":
                                        entornoFuncion.setSimbolo(paramFuncion.IDParam, exp, "array", paramFuncion.Fila, paramFuncion.Columna)
                                        indiceParam += 1
                                    else:
                                        Globales.tablaErrores.append(Error(f"Tipos no coinciden", paramFuncion.Fila, paramFuncion.Columna))
                                        return Retorno("ERROR", "indice")

                            else:
                                # Pasar valor
                                paramFuncion = objFuncion.Parametros[indiceParam]
                                if paramFuncion.IDTipo == exp.Tipo or paramFuncion.IDTipo == "Any":
                                    entornoFuncion.setSimbolo(paramFuncion.IDParam, exp, exp.Tipo, paramFuncion.Fila, paramFuncion.Columna)
                                    indiceParam += 1
                                else:
                                    Globales.tablaErrores.append(Error(f"Tipos no coinciden", paramFuncion.Fila, paramFuncion.Columna))
                                    return Retorno("ERROR", "indice")

                        # Ejecutar bloque funcion
                        resultado = objFuncion.Instrucciones.execute(entornoFuncion)
                        if resultado == None: return Retorno(None, "Nulo")
                        else:
                            if resultado.Tipo == "return":
                                objRetorno = resultado.Valor
                                return objRetorno
                            
        else:
            funcionesPrimitivas = ["lowercase","uppercase","log10","log","sin","cos","tan","sqrt","float","typeof","length","push!","pop!"]

            if self.ID in funcionesPrimitivas:

                if self.ID == "uppercase":

                    if len(self.Params) == 1:
                        valorParam = self.Params[0].execute(entorno)
                        if valorParam.Tipo == "String":
                            return Retorno(valorParam.Valor.upper(), "String")
                        else: 
                            Globales.tablaErrores.append(Error(f"El tipo no es String", self.Fila, self.Columna))
                            return Retorno("ERROR", "upper")
                    else: 
                        Globales.tablaErrores.append(Error(f"Uppercase solo acepta un parametro", self.Fila, self.Columna))
                        return Retorno("ERROR", "upper")

                elif self.ID == "lowercase":
                    
                    if len(self.Params) == 1:
                        valorParam = self.Params[0].execute(entorno)
                        if valorParam.Tipo == "String":
                            return Retorno(valorParam.Valor.lower(), "String")
                        else: 
                            Globales.tablaErrores.append(Error(f"El tipo no es String", self.Fila, self.Columna))
                            return Retorno("ERROR", "upper")
                    else: 
                        Globales.tablaErrores.append(Error(f"Lowercase solo acepta un parametro", self.Fila, self.Columna))
                        return Retorno("ERROR", "upper")

                elif self.ID == "log10":

                    if len(self.Params) == 1:
                        valorParam = self.Params[0].execute(entorno)
                        if (valorParam.Tipo == "Int64" or valorParam.Tipo == "Float64") and valorParam.Valor > 0:
                            logRes = math.log10(valorParam.Valor)
                            return Retorno(logRes, "Float64")
                        else: 
                            Globales.tablaErrores.append(Error(f"El valor de log10 no es numerico o es negativo", self.Fila, self.Columna))
                            return Retorno("ERROR", "log10")
                    else: 
                        Globales.tablaErrores.append(Error(f"Log10 solo acepta un parametro", self.Fila, self.Columna))
                        return Retorno("ERROR", "log10")

                elif self.ID == "log":
                    
                    if len(self.Params) == 2:
                        base = self.Params[0].execute(entorno)
                        num = self.Params[1].execute(entorno)

                        if (base.Tipo == "Int64" or base.Tipo == "Float64") and (num.Tipo == "Int64" or num.Tipo == "Float64") and (num.Valor > 0 and base.Valor > 0):
                            logRes = math.log(num.Valor, base.Valor)
                            return Retorno(logRes, "Float64")
                        else: 
                            Globales.tablaErrores.append(Error(f"Los valores de log no son numericos o son negativos", self.Fila, self.Columna))
                            return Retorno("ERROR", "log")
                    else: 
                        Globales.tablaErrores.append(Error(f"Log acepta solo acepta dos parametros", self.Fila, self.Columna))
                        return Retorno("ERROR", "log")

                elif self.ID == "sin":

                    if len(self.Params) == 1:
                        valorParam = self.Params[0].execute(entorno)
                        if valorParam.Tipo == "Int64" or valorParam.Tipo == "Float64":
                            return Retorno(math.sin(valorParam.Valor), "Float64")
                        else: 
                            Globales.tablaErrores.append(Error(f"El tipo no es numerico", self.Fila, self.Columna))
                            return Retorno("ERROR", "sin")
                    else: 
                        Globales.tablaErrores.append(Error(f"Sin solo acepta un parametro", self.Fila, self.Columna))
                        return Retorno("ERROR", "sin")

                elif self.ID == "cos":
                    
                    if len(self.Params) == 1:
                        valorParam = self.Params[0].execute(entorno)
                        if valorParam.Tipo == "Int64" or valorParam.Tipo == "Float64":
                            return Retorno(math.cos(valorParam.Valor), "Float64")
                        else: 
                            Globales.tablaErrores.append(Error(f"El tipo no es numerico", self.Fila, self.Columna))
                            return Retorno("ERROR", "cos")
                    else: 
                        Globales.tablaErrores.append(Error(f"Cos solo acepta un parametro", self.Fila, self.Columna))
                        return Retorno("ERROR", "cos")

                elif self.ID == "tan":

                    if len(self.Params) == 1:
                        valorParam = self.Params[0].execute(entorno)
                        if valorParam.Tipo == "Int64" or valorParam.Tipo == "Float64":
                            return Retorno(math.tan(valorParam.Valor), "Float64")
                        else: 
                            Globales.tablaErrores.append(Error(f"El tipo no es numerico", self.Fila, self.Columna))
                            return Retorno("ERROR", "tan")
                    else: 
                        Globales.tablaErrores.append(Error(f"Cos solo acepta un parametro", self.Fila, self.Columna))
                        return Retorno("ERROR", "tan")

                elif self.ID == "sqrt":

                    if len(self.Params) == 1:
                        valorParam = self.Params[0].execute(entorno)
                        if (valorParam.Tipo == "Int64" or valorParam.Tipo == "Float64") and valorParam.Valor > 0:
                            return Retorno(math.sqrt(valorParam.Valor), "Float64")
                        else: 
                            Globales.tablaErrores.append(Error(f"El tipo no es numerico o es negativo", self.Fila, self.Columna))
                            return Retorno("ERROR", "tan")
                    else: 
                        Globales.tablaErrores.append(Error(f"Sqrt solo acepta un parametro", self.Fila, self.Columna))
                        return Retorno("ERROR", "tan")

                elif self.ID == "float":
                    
                    if len(self.Params) == 1:
                        valorParam = self.Params[0].execute(entorno)
                        if valorParam.Tipo == "Int64":
                            return Retorno(float(valorParam.Valor), "Float64")
                        else: 
                            Globales.tablaErrores.append(Error(f"El tipo no es Int64", self.Fila, self.Columna))
                            return Retorno("ERROR", "float")
                    else: 
                        Globales.tablaErrores.append(Error(f"Float solo acepta un parametro", self.Fila, self.Columna))
                        return Retorno("ERROR", "float")

                elif self.ID == "typeof":

                    if len(self.Params) == 1:
                        valorParam = self.Params[0].execute(entorno)
                        if valorParam.Valor != "ERROR":
                            return Retorno(valorParam.Tipo, "String")
                        else:
                            return Retorno("ERROR", "typeof")
                    else: 
                        Globales.tablaErrores.append(Error(f"TypeOf solo acepta un parametro", self.Fila, self.Columna))
                        return Retorno("ERROR", "typeof")

                elif self.ID == "length":

                    if len(self.Params) == 1:
                        valorParam = self.Params[0].execute(entorno)

                        if valorParam.Valor != "ERROR" and valorParam.Tipo == "array":
                            return Retorno(len(valorParam.Valor.Array), "Int64")
                        else:
                            Globales.tablaErrores.append(Error(f"Length solo acepta array", self.Fila, self.Columna))
                            return Retorno("ERROR", "length")
                    else:
                        Globales.tablaErrores.append(Error(f"Length solo acepta un parametro", self.Fila, self.Columna))
                        return Retorno("ERROR", "length")
                
                elif self.ID == "push!":

                    if len(self.Params) == 2:
                        arreglo = self.Params[0].execute(entorno)
                        expresion = self.Params[1].execute(entorno)

                        if arreglo.Tipo == "array" and expresion.Valor != "ERROR":  
                            arreglo.Valor.Array.append(expresion)          
                            return arreglo
                        else:
                            Globales.tablaErrores.append(Error(f"Push! el dato no es array o es incorrecto", self.Fila, self.Columna))
                            return Retorno("ERROR", "push")
                    else:
                        Globales.tablaErrores.append(Error(f"Push! solo acepta dos parametros", self.Fila, self.Columna))
                        return Retorno("ERROR", "push")

                elif self.ID == "pop!":

                    if len(self.Params) == 1:
                        arreglo = self.Params[0].execute(entorno)
                        if arreglo.Tipo == "array":
                            if len(arreglo.Valor.Array) > 0:
                                objPop = arreglo.Valor.Array.pop()
                                if not hasattr(objPop, "Valor"):
                                    return objPop.execute(entorno)
                                else:
                                    return objPop
                            else:
                                Globales.tablaErrores.append(Error(f"Pop! el arreglo ya no tiene indices", self.Fila, self.Columna))
                                return Retorno("ERROR", "pop")
                        else:
                            Globales.tablaErrores.append(Error(f"Pop! el dato no es array o es incorrecto", self.Fila, self.Columna))
                            return Retorno("ERROR", "pop")
                    else:
                        Globales.tablaErrores.append(Error(f"Pop! solo acepta un parametro", self.Fila, self.Columna))
                        return Retorno("ERROR", "pop")

            else:
                Globales.tablaErrores.append(Error(f"La funcion o struct no existe: {self.ID}", self.Fila, self.Columna))
                return Retorno("ERROR", "llamada")

    def getAST(self, dot):
        idFuncion = str(random.randint(1, 1000000000))
        idNombreFunc = str(random.randint(1, 1000000000))
        idParIzq = str(random.randint(1, 1000000000))
        idParDer = str(random.randint(1, 1000000000))
        idExpresiones = str(random.randint(1, 1000000000))
        idPtComa = str(random.randint(1, 1000000000))

        dot.node(idFuncion, "Funcion")
        dot.node(idNombreFunc, self.ID)
        dot.node(idParIzq, "(")
        dot.node(idExpresiones, "Expresiones")
        dot.node(idParDer, ")")
        dot.node(idPtComa, ";")
        
        dot.edge(idFuncion, idNombreFunc)
        dot.edge(idFuncion, idParIzq)
        dot.edge(idFuncion, idExpresiones)

        if self.Params != None:
            for exp in self.Params:
                idExp = str(random.randint(1, 1000000000))
                dot.node(idExp, "Expresion")
                dot.edge(idExpresiones, idExp)

                dot, IDDotExp = exp.getAST(dot)
                dot.edge(idExp, IDDotExp)

        dot.edge(idFuncion, idParDer)
        dot.edge(idFuncion, idPtComa)
        
        return dot, idFuncion
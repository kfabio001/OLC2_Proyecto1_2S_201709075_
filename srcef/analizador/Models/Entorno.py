#Importacion de clases abstractas para la implemenacion del acceso
from ..Models.Simbolo import *
from ..Abstractos.Error import *

from ..Abstractos import Globales

class Entorno:
#constructor de la sentencia acceso, sobrecarga operadores derecho e izquierdo
    def __init__(self, padre, nombre):
        self.Padre = padre
        self.Nombre = nombre
        self.TablaSimbolos = {}
        self.PilaSentencias = {} # Controlar break, continue
        self.PilaFunciones = {} # Controlar funciones, metodos

    # Para variables normales
    def setSimbolo(self, id, exp, tipo, fila=None, columna=None):
        nuevoSimbolo = Simbolo(exp.Valor, tipo, id, fila, columna)

        entorno = self
        # Actualizar si ya existe
        while entorno != None:
            if id in entorno.TablaSimbolos.keys():
                entorno.TablaSimbolos[id] = nuevoSimbolo
                return
            entorno = entorno.Padre
        # Setear si no esta agregado
        self.TablaSimbolos[id] = nuevoSimbolo
        Globales.tablaSimbolos[id] = nuevoSimbolo
    
    # Para structs
    def setStruct(self, id, struct, fila, columna):
        nuevoStruct = Simbolo(struct, "struct", id, fila, columna)

        entorno = self
        # Verificar que no exista
        while entorno != None:
            if id in entorno.TablaSimbolos.keys():
                Globales.tablaErrores.append(Error(f"Struct ya declarado: {id}", fila, columna))
                return
            entorno = entorno.Padre
        # Setear si no esta agregado
        self.TablaSimbolos[id] = nuevoStruct
        Globales.tablaSimbolos[id] = nuevoStruct

    def setFuncion(self, id, funcion, fila, columna):
        nuevaFuncion = Simbolo(funcion, "funcion", id, fila, columna)

        entorno = self
        # Verificar que no exista
        while entorno != None:
            if id in entorno.TablaSimbolos.keys():
                Globales.tablaErrores.append(Error(f"Funcion ya declarada: {id}", fila, columna))
                return
            entorno = entorno.Padre
        # Setear si no esta agregado
        self.TablaSimbolos[id] = nuevaFuncion
        Globales.tablaSimbolos[id] = nuevaFuncion

    def getSimbolo(self, id):
        entorno = self
        while entorno != None:
            if id in entorno.TablaSimbolos.keys():
                return entorno.TablaSimbolos[id]
            entorno = entorno.Padre
        return None

    def getEntornoGlobal(self):
        entorno = self
        while entorno.Padre != None:
            entorno = entorno.Padre
        return entorno

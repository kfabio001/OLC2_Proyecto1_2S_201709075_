import os
def inicializar():
    #Varialbles globales
    #Variable tabla de errores global
    global tablaErrores
    # tabla de simbolos
    global tablaSimbolos
    # String de salida
    global salidaPrints
    # Entrada de texto en el editor
    global entradaTxt 
# tabla de errores
    tablaErrores = []
    tablaSimbolos = {}
    #consola de salida
    salidaPrints = ""
    entradaTxt = ""
    
def escribir(): 
    file = open("filename.txt", "w")
    file.write(salidaPrints)
    file.close()
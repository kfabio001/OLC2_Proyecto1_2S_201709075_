import random
import graphviz

class Grafo:
#inicializacion del objeto Graphviz
    def __init__(self):
        self.Dot = graphviz.Digraph(comment='AST JOLC')
#Doto Global para el manejo del arbol
    def getGlobalDot(self, instrucciones):
        # Memoria del dot
        idPadre = str(random.randint(1, 1000000000))
        #In
        idInstrucciones = str(random.randint(1, 1000000000))
        # Se guarda el padre
        self.Dot.node(idPadre, "AST")
        # Se mandan los nodos instrucciones
        self.Dot.node(idInstrucciones, "Instrucciones")
        self.Dot.edge(idPadre, idInstrucciones)
        #Ciclo para todas las instrucciones
        for instr in instrucciones:
            # Memoria para el arbol
            # recorre las instrucciones dentro del listado de instruccion
            idInstr = str(random.randint(1, 1000000000))
            self.Dot.node(idInstr, "Instruccion")
            self.Dot.edge(idInstrucciones, idInstr)
            # Dot para formar el ast
            self.Dot, idDotInst = instr.getAST(self.Dot) 
            self.Dot.edge(idInstr, idDotInst)

        return self.Dot



    

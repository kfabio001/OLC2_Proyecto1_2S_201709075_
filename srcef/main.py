from flask import Flask, request, render_template
from flask_cors import CORS
import json

from analizador.gramatica import parse #Gramatica  - falta arrays :S
from analizador.Models.Entorno import * # arreglo en le cambio de entorno

from analizador.Abstractos import Globales # Globales terminado
from analizador.Abstractos.Grafo import * # Reportes t erminado

import graphviz
sal='sds'
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route("/execute", methods=['POST']) #ruta para ejecutar la entrada

    
def home(): #Home llamado en la navegacion
    try:
        Globales.inicializar()#inicializan variables globales

        entrada = request.json['input']#Guarda en varible entrada el texto de entrada
        Globales.entradaTxt = entrada# se guarda la entrada en la variable global para su analisis
        print(request.json['input'])
        if entrada != "":#si esta vacia no entra
            entornoGlobal = Entorno(None, "global")#Se almacena el entorno global
            ast = parse(entrada)#se manda a analizar
            dotAST = Grafo().getGlobalDot(ast)# Si no hay error se manda a graficar
            dotAST.attr(style='filled', color='lightgrey')
            dotAST.node_attr['style'] = 'filled'
            dotAST.format = "png"# el formato de salida
            dotAST.render('./static/ASTDOT.gv')#nomb re del archivo donde esta la info del grafo
    
            for instruccion in ast:
                valor = instruccion.execute(entornoGlobal)#se ejecuta cada instruccion almacenada en el arbol

            res = {"salida": Globales.salidaPrints}#Se guarda la salida de las instrucciones
            
            print(Globales.salidaPrints)
        #with open('filename', 'w') as f:
         #   f.write('Hola mundo\n')

            return { 'msg': json.dumps(res), 'code': 200 }#codigo envio satisfactorio
            
    except Exception as e:# si existe error se envia el mensjaje
        print("Error al ejecutar")
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return { 'msg': 'ERROR', 'code': 500 }# mensaje de error
'''
dfasdfasdfasdfa
'''

@app.route("/getDataRes", methods=['GET'])#Ruta reportes
def getDataRes():
    try:

        jsonErrores = None #limpia los errores
        if len(Globales.tablaErrores) > 0:
            jsonErrores = json.dumps([ob.__dict__ for ob in Globales.tablaErrores])#Respuesta en json de los errores encontrados
        else:
            jsonErrores = json.dumps([])#limpia los errores

        listSimbolos = []#reporte tabla de simbolos
        for ids in Globales.tablaSimbolos:#lee la tabla de simbolos guardada y almacena los simbolos en una lista
            objSimbolo = Globales.tablaSimbolos[ids]
            listSimbolos.append({'ID':ids,'Tipo':objSimbolo.Tipo,'Fila':objSimbolo.Fila,'Columna':objSimbolo.Columna})
            
        res = {"tablaErrores": jsonErrores, "tablaSimbolos": listSimbolos}#envia la tabla de erroes y de simbolos

        return { 'msg': json.dumps(res), 'code': 200 }# request satisfactorio
    except:
        return { 'msg': 'ERROR', 'code': 500 }#error de respuesta



@app.route("/getTree", methods=['GET'])#ruta para el reporte del arbol
def getTree():
    try:
        return { 'msg': 'tree', 'code': 200 }
    except:
        return { 'msg': 'ERROR', 'code': 500 }

@app.route("/", methods=['GET'])#ruta para mostrar el home
def home_view():
    return render_template('home.html')

@app.route("/analisis", methods=['GET'])#ruta para mostrar la pantalla de analisis
def parse_view():
    return render_template('analisis.html')

@app.route("/reportes", methods=['GET'])#ruta para mostrar los errores
def report_view():
    return render_template('reportes.html')


#if __name__ == "__main__":# inicializacion del servicio web
  #  app.run(debug=True)  

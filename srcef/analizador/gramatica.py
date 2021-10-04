from .Abstractos.Error import *

from .Models.Operaciones.Aritmetica import *
from .Models.Operaciones.Relacional import *
from .Models.Operaciones.Logico import *

from .Models.Simbolo import *
from .Models.Bloque import *
from .Models.Llamada import *

from .Models.Funciones.Funcion import *
from .Models.Funciones.ParamDecl import *
from .Models.Funciones.Print import *
from .Models.Funciones.Parse import *
from .Models.Funciones.Trunc import *
from .Models.Funciones.StringFunc import *

from .Models.Variables.Asignacion import *
from .Models.Variables.Atributo import *
from .Models.Variables.Struct import *
from .Models.Variables.Arreglo import *
from .Models.Variables.Acceso import *
from .Models.Variables.AccesoAsignacion import *

from .Models.Sentencias.If import *
from .Models.Sentencias.While import *
from .Models.Sentencias.For import *

from .Abstractos import Globales

rw = {
    "true": "TRUE",
    "false": "FALSE",
    "nothing": "NOTHING",

    "println": "PRINTLN",
    "print": "PRINT",
    "parse": "PARSE",
    "trunc": "TRUNC",
    "string": "STRINGFUNC",

    "Int64": "TINT64",
    "Float64": "TFLOAT64",
    "String": "TSTRING",
    "Bool": "TBOOL",
    "Char": "TCHAR",
    "Nulo": "TNULO",

    "begin": "BEGIN",
    "end": "END",
    
    "if" : "IF",
    "else": "ELSE",
    "elseif": "ELSEIF",

    "while": "WHILE",

    "for": "FOR",
    "in": "IN",

    "break": "BREAK",
    "continue": "CONTINUE",
    "return": "RETURN",

    "function" : "FUNCTION",

    "struct": "STRUCT",
    "mutable": "MUTABLE",
}

tokens  = [
    "ID",

    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',

    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'POTENCIA',
    'MODULO',

    'MAYOR',
    'MENOR',
    'MAYIGUAL',
    'MENIGUAL',
    'IGUALDAD',
    'DISTINTO',

    'OR',
    'AND',
    'NOT',

    'DECIMAL',
    'ENTERO',
    'STRING',
    'CHAR',

    'IGUAL',

    'PTCOMA',
    'DOSPUNTOS',
    'COMA',
    'PUNTO',

] + list(rw.values())

# Tokens
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'

t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_POTENCIA  = r'\^'
t_MODULO    = r'%'

t_MAYOR     = r'>'
t_MENOR     = r'<'
t_MAYIGUAL  = r'>='
t_MENIGUAL  = r'<='
t_IGUALDAD  = r'=='
t_DISTINTO  = r'!='

t_OR        = r'\|\|'
t_AND       = r'&&'
t_NOT       = r'!'

t_PTCOMA    = r';'
t_COMA      = r','
t_DOSPUNTOS = r':'
t_PUNTO     = r'\.'

t_IGUAL     = r'='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9!]*'
    #t.type = rw.get(t.value.upper(), 'ID')
    t.type = rw.get(t.value,'ID')
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error al parsear float %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Error al parsear int %d", t.value)
        t.value = 0
    return t

def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t

def t_CHAR(t):
    r'\'.?\''
    t.value = t.value[1:-1]
    return t

# Caracteres ignorados
t_ignore = " \t"

def t_MLCOMMENT(t):
    r'\#=(.|\n)*?=\#'
    t.lexer.lineno += t.value.count("\n")

def t_OLCOMMENT(t):
    r'\#.*\n'
    t.lexer.lineno += 1
    
def t_newline(t):
    r'\n+'
    #t.lexer.lineno += t.value.count("\n")
    t.lexer.lineno += len(t.value)
    
def getCol(token):
    line_start = Globales.entradaTxt.rfind('\n', 0, token) + 1
    return (token - line_start) + 1

def t_error(t):
    #print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','IGUALDAD','DISTINTO'),
    ('left','MAYOR','MENOR','MAYIGUAL','MENIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('left','POTENCIA'),
    ('left','MODULO'),
    ('right','NOT'),
    ('right','UMENOS'),
)

# Definición de la gramática
def p_inicio(t):
    'start : instrucciones'
    t[0] = t[1]
    t.lexer.lineno = 1 # Reiniciar conteo lineas
    return t[0]

def p_instrucciones(t):
    '''instrucciones    : instrucciones instruccion 
                        | instruccion '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]

def p_instruccion(t):
    '''instruccion  : printInst PTCOMA
                    | asignacion PTCOMA
                    | accesoAsignacion PTCOMA
                    | structs PTCOMA
                    | ifInst PTCOMA
                    | whileInst PTCOMA
                    | forInst PTCOMA
                    | continueInst PTCOMA
                    | breakInst PTCOMA
                    | funcionDecl PTCOMA
                    | llamadaExp PTCOMA
                    | returnInst PTCOMA'''
    t[0] = t[1]

# LLAMADAS -----------------------------------------------
def p_llamada(t):
    '''llamadaExp   : ID PARIZQ paramExp PARDER
                    | ID PARIZQ PARDER
                    | PARSE PARIZQ tipo COMA expresion PARDER
                    | TRUNC PARIZQ tipo COMA expresion PARDER
                    | STRINGFUNC PARIZQ expresion PARDER'''
    if len(t) == 5:
        if t.slice[1].type == "ID":
            t[0] = Llamada(t[1], t[3], t.lineno(1), getCol(t.lexpos(1)))
        else:
            t[0] = StringFunc(t[3], t.lineno(1), getCol(t.lexpos(1))) 

    elif len(t) == 4:
        t[0] = Llamada(t[1], None, t.lineno(1), getCol(t.lexpos(1)))

    elif len(t) == 7:
        fun = t.slice[1].type
        if fun == "PARSE":
            t[0] = Parse(t[3], t[5], t.lineno(1), getCol(t.lexpos(1)))
        elif fun == "TRUNC":
            t[0] = Trunc(t[3], t[5], t.lineno(1), getCol(t.lexpos(1)))

def p_param_expresion(t):
    '''paramExp     : paramExp COMA expresion
                    | expresion'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]

# FUNCIONES --------------------------------------------------
def p_funcion(t):
    '''funcionDecl  : FUNCTION ID PARIZQ paramsDecl PARDER bloque END
                    | FUNCTION ID PARIZQ PARDER bloque END'''
    if len(t) == 7:
        t[0] = Funcion(t[2], None, t[5], t.lineno(1), getCol(t.lexpos(1)))
    else:
        t[0] = Funcion(t[2], t[4], t[6], t.lineno(1), getCol(t.lexpos(1)))
    
def p_params_declaracion_list(t):
    '''paramsDecl   : paramsDecl COMA paramDl
                    | paramDl'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]

def p_param_declaracion(t):
    '''paramDl  : ID DOSPUNTOS DOSPUNTOS tipo
                | ID'''
    if len(t) == 2:
        t[0] = ParamDecl(t[1], "Any", t.lineno(1), getCol(t.lexpos(1)))
    else:
        t[0] = ParamDecl(t[1], t[4], t.lineno(1), getCol(t.lexpos(1)))

def p_returnInst(t):
    'returnInst : RETURN expresion'
    t[0] = Simbolo(t[2], "return", None, t.lineno(1), getCol(t.lexpos(1)))

# FUNCIONES PRIMITIVAS PRINT  -----------------------------------------------
def p_instruccion_print(t):
    'printInst : PRINT PARIZQ paramExp PARDER'
    t[0] = Print(t[3], "l")

def p_instruccion_println(t):
    'printInst : PRINTLN PARIZQ paramExp PARDER'
    t[0] = Print(t[3], "nl")

# ASIGNACION -----------------------------------------------
def p_asignacion(t):
    '''asignacion   : ID IGUAL expresion DOSPUNTOS DOSPUNTOS tipo
                    | ID IGUAL expresion'''
    if len(t) == 4:
        t[0] = Asignacion(t[1], t[3], None, t.lineno(1), getCol(t.lexpos(1)))
    else:
        t[0] = Asignacion(t[1], t[3], t[6], t.lineno(1), getCol(t.lexpos(1)))

def p_accesoAsignacion(t):
    '''accesoAsignacion : acceso IGUAL expresion DOSPUNTOS DOSPUNTOS tipo
                        | acceso IGUAL expresion'''
    if len(t) == 4:
        t[0] = AccesoAsignacion(t[1], t[3], None, t.lineno(1), getCol(t.lexpos(1)))
    else:
        t[0] = AccesoAsignacion(t[1], t[3], t[6], t.lineno(1), getCol(t.lexpos(1)))

def p_tipo(t):
    '''tipo : TINT64
            | TFLOAT64
            | TSTRING
            | TBOOL
            | TCHAR
            | TNULO
            | ID'''
    t[0] = t[1]

# STRUCTS -----------------------------------------------
def p_structs(t):
    '''structs  : MUTABLE STRUCT ID atributos END
                | STRUCT ID atributos END'''
    if len(t) == 5:
        t[0] = Struct(t[2], False, t[3], t.lineno(1), getCol(t.lexpos(1)))
    else:
        t[0] = Struct(t[3], True, t[4], t.lineno(1), getCol(t.lexpos(1)))
    
def p_atributos(t):
    '''atributos    : atributos atributo
                    | atributo'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]            

def p_atributo(t):
    '''atributo : ID DOSPUNTOS DOSPUNTOS tipo PTCOMA
                | ID PTCOMA'''
    if len(t) == 3:
        t[0] = Atributo(t[1], "Any", t.lineno(1), getCol(t.lexpos(1)))
    else:
        t[0] = Atributo(t[1], t[4], t.lineno(1), getCol(t.lexpos(1)))

# ARREGLOS --------------------------------------------------------------
def p_arreglo(t):
    '''arreglo  : CORIZQ paramExp CORDER
                | ID listaIndices'''
    if len(t) == 4:
        t[0] = Arreglo(t[2], "declaracion", None, t.lineno(2), getCol(t.lexpos(2)))
    else:
        t[0] = Arreglo(t[1], "acceso", t[2], t.lineno(1), getCol(t.lexpos(1)))

def p_listaIndices(t):
    '''listaIndices : listaIndices indice
                    | indice'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]  

def p_indice(t):
    '''indice   : CORIZQ expresion CORDER'''
    t[0] = t[2] 

# TIPO RANGO ------------------------------------------------------------
def p_rango(t):
    '''rango    : expresion DOSPUNTOS expresion
                | BEGIN DOSPUNTOS expresion
                | expresion DOSPUNTOS END
                | BEGIN DOSPUNTOS END'''
    t[0] = Simbolo([t[1], t[3]], "Rango", None, t.lineno(1), getCol(t.lexpos(1)))


# ACCESO -------------------------------------------------------
def p_acceso(t):
    '''acceso   : acceso PUNTO acceso
                | ID PUNTO ID
                | arreglo PUNTO arreglo
                | arreglo PUNTO ID
                | ID PUNTO arreglo
                | ID
                | arreglo'''
    
    if t.slice[1].type == "acceso" and t.slice[3].type == "acceso":
        # Acceso multiple
        t[0] = Acceso([t[1], t[3]], "mix", t.lineno(1), getCol(t.lexpos(1)))
  
    else:
        if len(t) == 2:
            # Acceso singular
            tipo = t.slice[1].type
            if tipo == "arreglo":
                t[0] = Acceso(t[1], "array", t.lineno(1), getCol(t.lexpos(1)))
            elif tipo == "ID":
                t[0] = Acceso(t[1], "ID", t.lineno(1), getCol(t.lexpos(1)))
        else: 
            # Acceso con atributo
            tipoUno = "array" if t.slice[1].type == "arreglo" else "ID"
            tipoDos = "array" if t.slice[3].type == "arreglo" else "ID"
    
            accUno = Acceso(t[1], tipoUno, t.lineno(1), getCol(t.lexpos(1)))
            accDos = Acceso(t[3], tipoDos, t.lineno(1), getCol(t.lexpos(1)))

            t[0] = Acceso([accUno, accDos], "mix", t.lineno(1), getCol(t.lexpos(1)))


# BLOQUE DE INSTRUCCIONES -----------------------------------------------
def p_bloque(t):
    'bloque : instrucciones'
    t[0] = Bloque(t[1])

# SENTENCIA IF -----------------------------------------------
def p_ifInst(t):
    '''ifInst   : IF expresion bloque END
                | IF expresion bloque ELSE bloque END
                | IF expresion bloque elseIfInst END'''
    if len(t) == 5:
        t[0] = If(t[2], t[3], None, t.lineno(1), getCol(t.lexpos(1)))
    elif len(t) == 7:
        t[0] = If(t[2], t[3], t[5], t.lineno(1), getCol(t.lexpos(1)))
    elif len(t) == 6:
        t[0] = If(t[2], t[3], t[4], t.lineno(1), getCol(t.lexpos(1)))

def p_elseIfInst(t):
    '''elseIfInst   : ELSEIF expresion bloque
                    | ELSEIF expresion bloque ELSE bloque
                    | ELSEIF expresion bloque elseIfInst'''
    if len(t) == 4:
        t[0] = If(t[2], t[3], None, t.lineno(1), getCol(t.lexpos(1)))
    elif len(t) == 6:
        t[0] = If(t[2], t[3], t[5], t.lineno(1), getCol(t.lexpos(1)))
    elif len(t) == 5:
        t[0] = If(t[2], t[3], t[4], t.lineno(1), getCol(t.lexpos(1)))

# SENTENCIA WHILE -----------------------------------------------------
def p_whileInst(t):
    '''whileInst    : WHILE expresion bloque END'''
    t[0] = While(t[2], t[3], t.lineno(1), getCol(t.lexpos(1)))

# SENTENCIA FOR -----------------------------------------------------
def p_forInst(t):
    '''forInst    : FOR ID IN expresion bloque END'''
    t[0] = For(t[2], t[4], t[5], t.lineno(1), getCol(t.lexpos(1)))

# SENTENCIAS DE LOOPS
def p_continueInst(t):
    'continueInst : CONTINUE'
    t[0] = Simbolo(None, "continue", None, t.lineno(1), getCol(t.lexpos(1)))
    
def p_breakInst(t):
    'breakInst : BREAK '
    t[0] = Simbolo(None, "break", None, t.lineno(1), getCol(t.lexpos(1)))

# EXPRESIONES -----------------------------------------------------
def p_expresion_binaria(t):
    '''expresion    : expresion MAS expresion
                    | expresion MENOS expresion
                    | expresion POR expresion
                    | expresion DIVIDIDO expresion
                    | expresion POTENCIA expresion
                    | expresion MODULO expresion
                    
                    | expresion MAYOR expresion
                    | expresion MENOR expresion
                    | expresion MAYIGUAL expresion
                    | expresion MENIGUAL expresion
                    | expresion IGUALDAD expresion
                    | expresion DISTINTO expresion
                    
                    | expresion AND expresion
                    | expresion OR expresion'''
        
    if t[2] == '+': 
        t[0] = Aritmetica(t[1], t[3], "+", t.lineno(2), getCol(t.lexpos(2)))
    elif t[2] == '-':
        t[0] = Aritmetica(t[1], t[3], "-", t.lineno(2), getCol(t.lexpos(2)))
    elif t[2] == '*': 
        t[0] = Aritmetica(t[1], t[3], "*", t.lineno(2), getCol(t.lexpos(2)))
    elif t[2] == '/': 
        t[0] = Aritmetica(t[1], t[3], "/", t.lineno(2), getCol(t.lexpos(2)))
    elif t[2] == '^': 
        t[0] = Aritmetica(t[1], t[3], "^", t.lineno(2), getCol(t.lexpos(2)))
    elif t[2] == '%': 
        t[0] = Aritmetica(t[1], t[3], "%", t.lineno(2), getCol(t.lexpos(2)))
    
    elif t[2] == '>': 
        t[0] = Relacional(t[1], t[3], ">", t.lineno(2), getCol(t.lexpos(2)))
    elif t[2] == '<': 
        t[0] = Relacional(t[1], t[3], "<", t.lineno(2), getCol(t.lexpos(2)))
    elif t[2] == '>=': 
        t[0] = Relacional(t[1], t[3], ">=", t.lineno(2), getCol(t.lexpos(2)))
    elif t[2] == '<=': 
        t[0] = Relacional(t[1], t[3], "<=", t.lineno(2), getCol(t.lexpos(2)))
    elif t[2] == '==': 
        t[0] = Relacional(t[1], t[3], "==", t.lineno(2), getCol(t.lexpos(2)))
    elif t[2] == '!=': 
        t[0] = Relacional(t[1], t[3], "!=", t.lineno(2), getCol(t.lexpos(2)))
    
    elif t[2] == '&&': 
        t[0] = Logico(t[1], t[3], "and", t.lineno(2), getCol(t.lexpos(2)))
    elif t[2] == '||': 
        t[0] = Logico(t[1], t[3], "or", t.lineno(2), getCol(t.lexpos(2)))

def p_expresion_unaria(t):
    '''expresion    : MENOS expresion %prec UMENOS
                    | NOT expresion %prec UMENOS'''

    if t[1] == "-":
        t[0] = Aritmetica(t[2], None, "umenos", t.lineno(1), getCol(t.lexpos(1)))
    else:
        t[0] = Logico(t[2], None, "not", t.lineno(1), getCol(t.lexpos(1)))

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_basica(t):
    '''expresion    : ENTERO
                    | DECIMAL
                    | STRING
                    | CHAR
                    | TRUE
                    | FALSE
                    | NOTHING
                    | rango
                    | acceso
                    | llamadaExp'''

    #| ID PUNTO ID                    

    tipo = t.slice[1].type

    if tipo == "ENTERO":
        t[0] = Simbolo(t[1], "Int64", None, t.lineno(1), getCol(t.lexpos(1)))
    elif tipo == "DECIMAL":
        t[0] = Simbolo(t[1], "Float64", None, t.lineno(1), getCol(t.lexpos(1)))
    elif tipo == "STRING":
        t[0] = Simbolo(t[1], "String", None, t.lineno(1), getCol(t.lexpos(1)))
    elif tipo == "CHAR":
        t[0] = Simbolo(t[1], "Char", None, t.lineno(1), getCol(t.lexpos(1)))
    elif tipo == "rango":
        t[0] = t[1]
    elif tipo == "llamadaExp":
        t[0] = t[1]
    elif tipo == "acceso":
        t[0] = t[1]
    elif isinstance(t[1], str):
        value = str(t[1])
        if "true" in value:
            t[0] = Simbolo(True, "Bool", None, t.lineno(1), getCol(t.lexpos(1)))
        elif "false" in value:
            t[0] = Simbolo(False, "Bool", None, t.lineno(1), getCol(t.lexpos(1)))
        elif "nothing" in value:
            t[0] = Simbolo(None, "Nulo", None, t.lineno(1), getCol(t.lexpos(1))) 
            
def p_error(t):
    Globales.tablaErrores.append(Error(f"Error sintáctico en '{t.value}'", t.lineno, t.lexpos))

import ply.yacc as yacc
parser = yacc.yacc()

def parse(input):
    return parser.parse(input)

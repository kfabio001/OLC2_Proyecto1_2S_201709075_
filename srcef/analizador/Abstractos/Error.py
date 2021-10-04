from datetime import datetime
# clase que maneja los errores
class Error:
# Parametros mensaje, fecha, fila y columna
    def __init__(self, mensaje, fila, columna):
        now = datetime.now()

        self.Mensaje = mensaje
        self.Fila = fila
        self.Columna = columna
        # modelo dia / mes / año  hora:minuto:segundo
        self.Fecha = now.strftime("%d/%m/%Y %H:%M:%S")

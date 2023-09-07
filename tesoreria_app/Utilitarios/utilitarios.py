from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal, ROUND_HALF_DOWN
import pytz
import pandas as pd
from enum import Enum
from django.http.response import JsonResponse
import math


### Métodos ###

# Create a function that converts all dataframe columns to string:
def dataframeColumnsToString(df):
    # print the column types
    # print(df.dtypes)
    
    for col,datos in df.iteritems():
        # Se cambia a string las fechas pero con el formato.
        # Change datetime columns to string
        if df[col].dtype == 'datetime64[ns]':
            df[col] = df[col].apply(lambda x: datetime.strftime(x, '%d/%m/%Y'))
            continue

        df[col] = df[col].astype(str)
   
    return df

# Parametros
# param1: una lista (varias filas de consulta) con los valores, o una tupla (1 fila de consulta.)
# param2: lista con los nombre de las columnas


def crearDataFrame(valores: list | tuple, columnas: list):
    if type(valores) == list:
        return pd.DataFrame(valores, columns=columnas)
    elif type(valores) == tuple:
        return pd.DataFrame([valores], columns=columnas)

    return pd.DataFrame()


def realizarComparacionDatraframes(titulo: str, df1: pd.DataFrame, df2: pd.DataFrame):
    # Se comparan los excel
    # Se imprime el resultado
    print(f'\n*****{titulo}*****')
    print(f'Df1: {df1.shape[0]} filas y {df1.shape[1]} columnas')
    print(f'Df2: {df2.shape[0]} filas y {df2.shape[1]} columnas')
    print(f'Columnas de df1: {df1.columns}')
    print(f'Columnas de df2: {df2.columns}')

    print(df1 == df2)

    print("Filas que no concuerdan")
    dfFilasFaltantes = df1[(df1 == df2).all(axis=1) == False]
    print(dfFilasFaltantes)
    if dfFilasFaltantes.empty:
        print("**Todas las filas son iguales**")

    # Itera sobre las celdas del dataframe
    for index, row in df1.iterrows():
        # Itera sobre las columnas del row actual
        for column in df1.columns:
            # Si el valor de la celda actual es diferente del valor de la celda de la misma posición del otro dataframe
            if row[column] != df2.loc[index, column]:
                # Se imprime el error
                print("Error en la fila ", index, " columna ", column, "\nvalor ",
                      row[column], " | valor2 ", df2.loc[index, column], "\n")


# Para representar la presentación en los JSON.
class Representacion(Enum):
    INDEX = 'index'
    DICT = 'dict'
    SPLIT = 'split'
    LIST = 'list'


# Enviar JSON con mensaje y código de respuesta
def enviarDictComoJson(miDicc: dict, codigo: int):
    return JsonResponse(
        data=miDicc,
        status=codigo,
    )


def enviarJSONMensaje(mensaje: str, codigo: int):
    return JsonResponse(
        {
            "mensaje": mensaje,
            "codigo": codigo
        },
        status=codigo,
    )





def unificarEnviarDataframeComoJson(arreglosDF, codigo: int, representacion: Representacion = Representacion.INDEX):
    titulos = ['ACTIVOS','INGRESOS','PASIVOS','GASTOS','PATRIMONIO','FUERA_DE_BALANCE','BRECHA_DE_LIQUIDEZ','BRECHA_ACUMULADA_DE_LIQUIDEZ','ACTIVO_LIQUIDO_NETO','POSICION_DE_LIQUIDEZ_EN_RIESGO']
    diccionario = {}
    for i in range(0,10):
        dicc = arreglosDF[i].to_dict(orient=representacion.value)
        diccionario[titulos[i]] = dicc
    
    return JsonResponse(
        diccionario,
        status=codigo,)
    
def unificarEnviarDataframeComoJsonR1(arreglosDF, codigo: int, representacion: Representacion = Representacion.INDEX):
    titulos = ["FACTOR_DE_SENSIBILIDAD","ACTIVOS_SENSIBLES","PASIVOS_SENSIBLES","BRECHA","SENSIBILIDAD_DE_BRECHA"]
    diccionario = {}
    for i in range(0,5):
        dicc = arreglosDF[i].to_dict(orient=representacion.value)
        diccionario[titulos[i]] = dicc
    
    return JsonResponse(
        diccionario,
        status=codigo,)
    
    
    
def unificarEnviarDataframeComoJsonR2(arreglosDF, codigo: int, representacion: Representacion = Representacion.INDEX):
    titulos = ["ACTIVOS_SENSIBLES","PASIVOS_SENSIBLES","FUERA_DE_BALANCE","GAP","PATRIMONIO","POSICION"]
    diccionario = {}
    for i in range(0,6):
        dicc = arreglosDF[i].to_dict(orient=representacion.value)
        diccionario[titulos[i]] = dicc
    
    return JsonResponse(
        diccionario,
        status=codigo,)

def unificarEnviarDataframeComoJsonR3(arreglosDF, codigo: int, representacion: Representacion = Representacion.INDEX):
    titulos = ["ACTIVOS_SENSIBLES","PASIVOS_SENSIBLES","FUERA_DE_BALANCE","RECURSOS_PATRIMONIALES","SENSIBILIDAD","PATRIMONIO"]
    diccionario = {}
    for i in range(0,6):
        dicc = arreglosDF[i].to_dict(orient=representacion.value)
        diccionario[titulos[i]] = dicc
    
    return JsonResponse(
        diccionario,
        status=codigo,)



def enviarDataframeComoJson(miDataframe: pd.DataFrame, codigo: int, representacion: Representacion = Representacion.INDEX):
    return JsonResponse(
        miDataframe.to_dict(orient=representacion.value),
        status=codigo,)
    


# Enviar JSON con mensaje y código de respuesta
def enviarDictComoJson(miDicc: dict, codigo: int):
    return JsonResponse(
        data=miDicc,
        status=codigo,
    )


    
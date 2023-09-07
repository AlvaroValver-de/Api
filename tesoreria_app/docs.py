from drf_yasg import openapi
from drf_yasg.openapi import Response
from .serializers import  MensajeSerializer, RespuestaSerializer, RespuestaL10Serializer, RespuestaL11Serializer
from rest_framework import status

def getRespuestas():
    return {
        200: Response('OK', RespuestaSerializer),
        
        400: Response('Varios posibles errores', MensajeSerializer, examples={
            'application/json': {
                'mensaje': 'La fecha solicitada (31/03/2040) no puede ser mayor a la fecha máxima de los balances encontrados (31/01/2023)',
                'codigo': status.HTTP_400_BAD_REQUEST
            }
        }),
        
        406: openapi.Response('Parámetros de entrada no válidos', MensajeSerializer, examples={
            'application/json': {
                'mensaje': "Hubo un problema con los parámetros de entrada",
                'codigo': status.HTTP_406_NOT_ACCEPTABLE
            }
        })
    }



def getRespuestasL10():
        return {
        200: Response('OK', RespuestaL10Serializer),
        
        400: Response('Varios posibles errores', MensajeSerializer, examples={
            'application/json': {
                'mensaje': 'La fecha solicitada (31/03/2040) no puede ser mayor a la fecha máxima de los balances encontrados (31/01/2023)',
                'codigo': status.HTTP_400_BAD_REQUEST
            }
        }),
        
        406: openapi.Response('Parámetros de entrada no válidos', MensajeSerializer, examples={
            'application/json': {
                'mensaje': "Hubo un problema con los parámetros de entrada",
                'codigo': status.HTTP_406_NOT_ACCEPTABLE
            }
        })
    }


def getRespuestasL11():
        return {
        200: Response('OK', RespuestaL11Serializer),
        
        400: Response('Varios posibles errores', MensajeSerializer, examples={
            'application/json': {
                'mensaje': 'La fecha solicitada (31/03/2040) no puede ser mayor a la fecha máxima de los balances encontrados (31/01/2023)',
                'codigo': status.HTTP_400_BAD_REQUEST
            }
        }),
        
        406: openapi.Response('Parámetros de entrada no válidos', MensajeSerializer, examples={
            'application/json': {
                'mensaje': "Hubo un problema con los parámetros de entrada",
                'codigo': status.HTTP_406_NOT_ACCEPTABLE
            }
        })
    }

from rest_framework import serializers
from django.db import models


class TesoreriaSerializer(serializers.Serializer):
    fecha = serializers.CharField(max_length=10)
    
    oficina = serializers.IntegerField()
    entidad = serializers.CharField(max_length=15)
    
    class Meta:
        pass


class MensajeSerializer(serializers.Serializer):
    mensaje = serializers.CharField()
    codigo= serializers.IntegerField()
    class Meta:
        pass


class RespuestaSerializer(serializers.Serializer):    
    ACTIVOS=serializers.JSONField()
    INGRESOS=serializers.JSONField()
    PASIVOS=serializers.JSONField()
    GASTOS=serializers.JSONField()
    PATRIMONIO=serializers.JSONField()
    FUERA_DE_BALANCE=serializers.JSONField()
    BRECHA_DE_LIQUIDEZ=serializers.JSONField()
    BRECHA_ACUMULADA_DE_LIQUIDEZ=serializers.JSONField()
    ACTIVO_LIQUIDO_NETO=serializers.JSONField()
    POSICION_DE_LIQUIDEZ_EN_RIESGO=serializers.JSONField()
                 
    #respuesta = serializers.JSONField()
    class Meta:
        pass
    




#Modelo L10

class auxResL10(serializers.Serializer):
    _1 = serializers.CharField()
    _2 = serializers.CharField()
    _3 = serializers.CharField()
    _4 = serializers.CharField()
    _5 = serializers.CharField()
class RespuestaL10Serializer(serializers.Serializer):
    _1 = auxResL10()
    _337 = auxResL10()



#Modelo L11
class auxResL11(serializers.Serializer):
    _1 = serializers.CharField()
    _2 = serializers.CharField()
    _3 = serializers.CharField()
    _4 = serializers.CharField()
    _5 = serializers.CharField()
    _6 = serializers.CharField()
    _7 = serializers.CharField()
    _8 = serializers.CharField()
class RespuestaL11Serializer(serializers.Serializer):
    _1 = auxResL11()
    _43 = auxResL11()
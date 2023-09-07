from rest_framework.views import APIView
from .serializers import TesoreriaSerializer
from rest_framework import status
from .Utilitarios.Logs import Logs
from .Utilitarios.Errores import CustomError
from .Utilitarios.utilitarios import dataframeColumnsToString,enviarDataframeComoJson,enviarJSONMensaje,unificarEnviarDataframeComoJson,unificarEnviarDataframeComoJsonR1,unificarEnviarDataframeComoJsonR2,unificarEnviarDataframeComoJsonR3
from .docs import getRespuestas
import json

from drf_yasg.utils import swagger_auto_schema

from .docs import getRespuestas
from .Negocios.Estructuras.Limites_Inversion.Limites_Tipo_Inversion import Limites_De_Tipo_Inversion

# Create your views here.


class LimitesTipoInversionView(APIView):
    @ swagger_auto_schema(
        operation_description="Administracion de Riesgos de Tesoreria",
        request_body=TesoreriaSerializer,
        responses=getRespuestas(),
        # security=[{'Basic': []}],
    )
    def post(self, request):
        jdata = json.loads(request.body)
        serializer = TesoreriaSerializer(data=jdata)
        clienteIP = request.META.get('REMOTE_ADDR')

        if serializer.is_valid():
            Logs.registrarLog(
                f"Se realiza el cálculo de Limites de Tipo Inversion con los parametros {serializer.data} y la IP {clienteIP}")
            try:
                reporteLimitesTipoInversion = Limites_De_Tipo_Inversion(**serializer.data)
                ReporteLimitesTipoInversion = reporteLimitesTipoInversion.getReporte()
                ReporteLimitesTipoInversion = dataframeColumnsToString(ReporteLimitesTipoInversion )
                
                
                Logs.registrarLog(f"Se obtuvo el reporte Limites por Tipo de Inversion")
               
            
                #return enviarDataframeComoJson(dfR7, status.HTTP_200_OK)
                return enviarDataframeComoJson(ReporteLimitesTipoInversion, status.HTTP_200_OK)

            except CustomError as e:
                mensaje = str(e.message)
                Logs.registrarLog(mensaje)
             
                return enviarJSONMensaje(mensaje, status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                mensaje = "Hubo un error al obtener el reporte"
                Logs.registrarLog(mensaje)
                return enviarJSONMensaje(mensaje, status.HTTP_400_BAD_REQUEST)

        else:
            mensaje = "Hubo un problema con los parámetros de entrada"
            Logs.registrarLog(
                f'Parámetros de entrada: {serializer.initial_data} Errores: {serializer.errors}')
            return enviarJSONMensaje(mensaje, status.HTTP_406_NOT_ACCEPTABLE)




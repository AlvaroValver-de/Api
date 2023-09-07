import pandas as pd
from django.db import connection
from ..Utilitarios.Logs import Logs


class BD_Calificaciones:
    
    @staticmethod
    def consultaCalificacioneceb() -> pd.DataFrame:
        try:
            CONSULTA = """ SELECT eceb.ECX_FECHA,eceb.RUC_ENTIDAD,ef.ENTIDAD_NOMBRE,eceb.ECX_FIRMA_CAL_RIESGO,
                eceb.ECX_CALIFICACION,eceb.ECX_TIPO  FROM ENTIDAD_CAL_EXT_BCO eceb 
                INNER JOIN ENTIDAD_FINANCIERA ef on eceb.RUC_ENTIDAD = ef.RUC_ENTIDAD """
                        
                        
            with connection.cursor() as cursor:
                cursor.execute("SET NOCOUNT ON")
                cursor.execute(CONSULTA)
                resultado = cursor.fetchall()
                columnas = [col[0] for col in cursor.description]
                df = pd.DataFrame(resultado, columns=columnas)
                cursor.execute("SET NOCOUNT OFF")
                return df
        except Exception:
            mensaje = "Error al consultar Calificacion eceb"
            Logs.registrarLog(mensaje)
            raise Exception(mensaje)
        
        
    @staticmethod
    def consultaCalificacionesecic() -> pd.DataFrame:
        try:
            CONSULTA = """ SELECT ecic.ECI_FECHA,ecic.RUC_ENTIDAD,ef.ENTIDAD_NOMBRE ,ecic.ECI_PUNTAJE,
                ecic.ECI_CALIFICACION,ecic.ECI_TIPO FROM ENTIDAD_CAL_INT_COAC ecic 
                INNER JOIN ENTIDAD_FINANCIERA ef on ecic.RUC_ENTIDAD = ef.RUC_ENTIDAD """
                        
                        
            with connection.cursor() as cursor:
                cursor.execute("SET NOCOUNT ON")
                cursor.execute(CONSULTA)
                resultado = cursor.fetchall()
                columnas = [col[0] for col in cursor.description]
                df = pd.DataFrame(resultado, columns=columnas)
                cursor.execute("SET NOCOUNT OFF")
                return df
        except Exception:
            mensaje = "Error al consultar Calificacion ecic"
            Logs.registrarLog(mensaje)
            raise Exception(mensaje)



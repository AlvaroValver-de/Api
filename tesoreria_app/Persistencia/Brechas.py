import pandas as pd
from django.db import connection
from ..Utilitarios.Logs import Logs


class BD_DataBrechas:
    @staticmethod
    def consultaDataBrechas(ruc:str,fmes:str) -> pd.DataFrame:
        try:
            CONSULTA = """select tl.INFO_ESTRUCTURA, e.RUC_ENTIDAD,e.ENTIDAD_CODIGO,e.ENTIDAD_NOMBRE,
                    b.BAL_FECHA  from TABLA_L02 tl
                    inner join BALANCE b on tl.ID_BALANCE = b.ID_BALANCE 
                    inner join ENTIDAD e on b.BAL_CODIGO_ENTIDAD = e.ENTIDAD_CODIGO 
                    where e.RUC_ENTIDAD = %s
                    and b.BAL_FECHA = %s"""
                        
                        
            with connection.cursor() as cursor:
                cursor.execute("SET NOCOUNT ON")
                cursor.execute(CONSULTA,[ruc,fmes])
                resultado = cursor.fetchall()
                columnas = [col[0] for col in cursor.description]
                df = pd.DataFrame(resultado, columns=columnas)
                cursor.execute("SET NOCOUNT OFF")
                return df
        except Exception:
            mensaje = "Error al consultar LimTesoreria con fecha: "+fmes+",codigo entidad: "+ruc
            Logs.registrarLog(mensaje)
            raise Exception(mensaje)
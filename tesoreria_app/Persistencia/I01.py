import pandas as pd
from django.db import connection
from ..Utilitarios.Logs import Logs


class BD_I01:
    @staticmethod
    def consultaI01(ruc:str,fmes:str) -> pd.DataFrame:
        try:
            CONSULTA = """SELECT ti.TI01_NUMERO_IDENTIFICACION_DEPOSITO, ti.TI01_TIPO_IDENTIFICACION_DEPOSITARIO,
                        ti.TI01_IDENTIFICACION_EMISOR_DEPOSITARIO, ti.TI01_FECHA_EMISION, ti.TI01_FECHA_COMPRA,
                        ti.TI01_TIPO_INSTRUMENTO, ti.TI01_PAIS_EMISION_DEPOSITARIO, ti.TI01_VALOR_NOMINAL,
                        ti.TI01_VALOR_COMPRA, ti.TI01_PERIODICIDAD_PAGO_CUPON, ti.TI01_CLASIFICACION_EMISOR_DEPOSITARIO,
                        b.BAL_FECHA FROM TABLA_I01 ti 
                        INNER JOIN BALANCE b on ti.ID_BALANCE = b.ID_BALANCE
                        INNER JOIN OFICINA o on b.ID_OFICINA = o.ID_OFICINA 
                        WHERE b.BAL_FECHA = %s
                        AND o.RUC_ENTIDAD = %s"""
                        
                        
            with connection.cursor() as cursor:
                cursor.execute("SET NOCOUNT ON")
                cursor.execute(CONSULTA,[fmes,ruc])
                resultado = cursor.fetchall()
                columnas = [col[0] for col in cursor.description]
                df = pd.DataFrame(resultado, columns=columnas)
                cursor.execute("SET NOCOUNT OFF")
                return df
        except Exception:
            mensaje = "Error al consultar I01 con fecha: "+fmes+",codigo entidad: "+ruc
            Logs.registrarLog(mensaje)
            raise Exception(mensaje)


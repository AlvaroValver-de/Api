import pandas as pd
from django.db import connection
from ..Utilitarios.Logs import Logs


class BD_I02:
    @staticmethod
    def consultaI02(ruc:str,fmes:str) -> pd.DataFrame:
        try:
            CONSULTA = """SELECT ti.TI02_NUMERO_IDENTIFICACION_DEPOSITO,ti.TI02_TIPO_IDENTIFICACION_DEPOSITARIO,
                        ti.TI02_IDENTIFICACION_EMISOR_DEPOSITARIO, ti.TI02_FECHA_EMISION, ti.TI02_FECHA_COMPRA,
                        ti.TI02_FECHA_VENCIMIENTO,ti.TI02_CALIFICACION_RIESGO, ti.TI02_CALIFICADORA_RIESGO,
                        ti.TI02_FECHA_ULTIMA_CALIFICACION, ti.TI02_CUENTA_CONTABLE, ti.TI02_VALOR_LIBROS,
                        ti.TI02_ESTADO_TITULO, ti.TI02_TASA_INTERES_NOMINAL, ti.TI02_MONTO_INTERES_GENERADO,
                        ti.TI02_PROVISION_CONSTITUIDA,b.BAL_FECHA FROM TABLA_I02 ti
                        INNER JOIN BALANCE b ON ti.ID_BALANCE = b.ID_BALANCE 
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
            mensaje = "Error al consultar I02 con fecha: "+str(fmes)+",codigo entidad: "+ruc
            Logs.registrarLog(mensaje)
            raise Exception(mensaje)


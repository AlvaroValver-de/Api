import pandas as pd
from django.db import connection
from ..Utilitarios.Logs import Logs


class BD_SP_balance_fm:
    @staticmethod
    def consultaSPbalanceFm(fecha,id_oficina,RUC) :
        try:
            CONSULTA = """
                exec [dbo].[sp_obt_balance_fmes]
                    @p_fecha = %s,
                    @p_meses =%s,
                    @p_oficina=%s,
                    @p_entidad=%s,
                    @p_baltipo=%s,
                    @p_balidtipo=%s
            """
            with connection.cursor() as cursor:
                cursor.execute("SET NOCOUNT ON")
                cursor.execute(CONSULTA, (fecha,24,id_oficina,RUC,'PRI',1))
                columnas = (col[0] for col in cursor.description)
                resultado = cursor.fetchall()
                
            return [resultado,columnas]
        
        except Exception:
            mensaje = "Error al consultar el sp_obt_balance_fmes con fecha: "+str(fecha)+", Oficina: "+str(id_oficina)+"y RUC: "+str(RUC)
            Logs.registrarLog(mensaje)
            raise Exception(mensaje)
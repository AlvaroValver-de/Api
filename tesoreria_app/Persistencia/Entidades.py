import pandas as pd
from django.db import connection
from ..Utilitarios.Logs import Logs


class BD_Entidades:
    
    @staticmethod
    def consultaEntidadCodigo(entidad) -> str:
        try:
            CONSULTA = """
                SELECT e.ENTIDAD_CODIGO from ENTIDAD e WHERE RUC_ENTIDAD = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(CONSULTA,[str(entidad)])
                resultado = cursor.fetchone()[0]
                cod_ent = str(resultado)
                
                return cod_ent
        
        except Exception:
            mensaje = "Error al consultar el codigo de la entidad: "+entidad
            Logs.registrarLog(mensaje)
            raise Exception(mensaje)
        
        
    @staticmethod
    def consultaBalanceEntidad(fmes:str) -> pd.DataFrame:
        try:
            CONSULTA = """ SELECT bf.RUC_ENTIDAD, bf.BFI_FECHA_BALANCE, bdf.BDF_DATO_NUMERO_CTA,
                    bdf.BDF_DATO_TOTAL FROM BALANCE_FINANCIERO bf 
                    INNER JOIN BALANCE_DAT_FINANCIERO bdf on bf.ID_BALANCE = bdf.ID_BALANCE
                    WHERE bf.ID_TIPO_BALANCE = '99'
                    AND bf.BFI_FECHA_BALANCE = %s """
                        
                        
            with connection.cursor() as cursor:
                cursor.execute("SET NOCOUNT ON")
                cursor.execute(CONSULTA,[fmes])
                resultado = cursor.fetchall()
                columnas = [col[0] for col in cursor.description]
                df = pd.DataFrame(resultado, columns=columnas)
                cursor.execute("SET NOCOUNT OFF")
                return df
        except Exception:
            mensaje = "Error al consultar I01 con fecha: "+fmes+",codigo entidad: "
            Logs.registrarLog(mensaje)
            raise Exception(mensaje)
        

    
    @staticmethod
    def consultaDataEntidades(fmes:str) -> pd.DataFrame:
        try:
            CONSULTA = """ SELECT ef.RUC_ENTIDAD, ef.ENTIDAD_NOMBRE, ef.ENTIDAD_SEGMENTO, edf.EDF_FECHA FROM ENTIDAD_FINANCIERA ef
                    inner join ENTIDAD_DAT_FINANCIERA edf on ef.RUC_ENTIDAD = edf.RUC_ENTIDAD
                    where edf.EDF_FECHA = %s """
                        
                        
            with connection.cursor() as cursor:
                cursor.execute("SET NOCOUNT ON")
                cursor.execute(CONSULTA,[fmes])
                resultado = cursor.fetchall()
                columnas = [col[0] for col in cursor.description]
                df = pd.DataFrame(resultado, columns=columnas)
                cursor.execute("SET NOCOUNT OFF")
                return df
        except Exception:
            mensaje = "Error al consultar datos de las entidades con fecha: "+str(fmes)
            Logs.registrarLog(mensaje)
            raise Exception(mensaje)
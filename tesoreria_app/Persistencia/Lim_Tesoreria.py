import pandas as pd
from django.db import connection
from ..Utilitarios.Logs import Logs


class BD_LimTesoreria:
    @staticmethod
    def consultaLimTesoreria(ruc:str,id_oficina:str,fmes:str) -> pd.DataFrame:
        try:
            CONSULTA = """SELECT JSON_VALUE(tc.LT_LIMITES, '$."LI1301"') 'LI1301',
                        JSON_VALUE(tc.LT_LIMITES, '$."LI1302"') 'LI1302',
                        JSON_VALUE(tc.LT_LIMITES, '$."LI1303"') 'LI1303',
                        JSON_VALUE(tc.LT_LIMITES, '$."LI1304"') 'LI1304',
                        JSON_VALUE(tc.LT_LIMITES, '$."LI1305"') 'LI1305',
                        JSON_VALUE(tc.LT_LIMITES, '$."LI1306"') 'LI1306',
                        JSON_VALUE(tc.LT_LIMITES, '$."LI1307"') 'LI1307',
                        JSON_VALUE(tc.LT_LIMITES, '$."LI1103"') 'LI1103',
                        JSON_VALUE(tc.LT_LIMITES, '$."LIBP"') 'LIBP',
                        JSON_VALUE(tc.LT_LIMITES, '$."LIBPB"') 'LIBPB',
                        JSON_VALUE(tc.LT_LIMITES, '$."LIS1"') 'LIS1',
                        JSON_VALUE(tc.LT_LIMITES, '$."LIS2"') 'LIS2',
                        JSON_VALUE(tc.LT_LIMITES, '$."LIS3"') 'LIS3',
                        JSON_VALUE(tc.LT_LIMITES, '$."LIS4"') 'LIS4',
                        JSON_VALUE(tc.LT_LIMITES, '$."LIS5"') 'LIS5',
                        JSON_VALUE(tc.LT_LIMITES, '$."LISO"') 'LISO',
                        JSON_VALUE(tc.LT_LIMITES, '$."LIBV"') 'LIBV',
                        JSON_VALUE(tc.LT_LIMITES, '$."LIO"') 'LIO',
                        JSON_VALUE(tc.LT_LIMITES, '$."LIEMISOR"') 'LIEMISOR',
                        JSON_VALUE(tc.LT_LIMITES, '$."LICALEX"') 'LICALEX',
                        JSON_VALUE(tc.LT_LIMITES, '$."LICALIN"') 'LICALIN',
                        JSON_VALUE(tc.LT_LIMITES, '$."LISCAL"') 'LISCAL',
                        JSON_VALUE(tc.LT_LIMITES, '$."CALMB"') 'CALMB',
                        JSON_VALUE(tc.LT_LIMITES, '$."CALMBP"') 'CALMBP',
                        JSON_VALUE(tc.LT_LIMITES, '$."CALMCEX"') 'CALMCEX',
                        JSON_VALUE(tc.LT_LIMITES, '$."CALMCIN"') 'CALMCIN',
                        JSON_VALUE(tc.LT_LIMITES, '$."CALMMB"') 'CALMMB',
                        JSON_VALUE(tc.LT_LIMITES, '$."LIBCALM"') 'LIBCALM',
                        JSON_VALUE(tc.LT_LIMITES, '$."LICOACECALM"') 'LICOACECALM',
                        JSON_VALUE(tc.LT_LIMITES, '$."LICOACICALM"') 'LICOACICALM',
                        JSON_VALUE(tc.LT_LIMITES, '$."LIMVCALM"') 'LIMVCALM',
                        JSON_VALUE(tc.LT_LIMITES, '$."LTIPP"') 'LTIPP',
                        JSON_VALUE(tc.LT_LIMITES, '$."LPPP"') 'LPPP',
                        JSON_VALUE(tc.LT_LIMITES, '$."LD"') 'LD',
                        JSON_VALUE(tc.LT_LIMITES, '$."LV"') 'LV',
                        JSON_VALUE(tc.LT_LIMITES, '$."LSVP"') 'LSVP',
                        JSON_VALUE(tc.LT_LIMITES, '$."LSP"') 'LSP'
                        from TABLA_LT tc 
                        inner join BALANCE b  on tc.ID_BALANCE = b.ID_BALANCE                
                        inner join ENTIDAD e on b.BAL_CODIGO_ENTIDAD = e.ENTIDAD_CODIGO 
                        where b.ID_TIPO_BALANCE = 95 --LT
                        and e.RUC_ENTIDAD = %s
                        and b.ID_OFICINA = %s
                        and b.BAL_FECHA = %s """
                        
                        
            with connection.cursor() as cursor:
                cursor.execute("SET NOCOUNT ON")
                cursor.execute(CONSULTA,[ruc,id_oficina,fmes])
                resultado = cursor.fetchall()
                columnas = [col[0] for col in cursor.description]
                df = pd.DataFrame(resultado, columns=columnas)
                cursor.execute("SET NOCOUNT OFF")
                return df
        except Exception:
            mensaje = "Error al consultar LimTesoreria con fecha: "+str(fmes)+",codigo entidad: "+ruc+" y la ofician: "+id_oficina
            Logs.registrarLog(mensaje)
            raise Exception(mensaje)
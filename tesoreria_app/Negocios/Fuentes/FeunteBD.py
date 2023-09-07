from .IFuente import IFuente
import pandas as pd
import numpy as np

from ...Utilitarios.Logs import Logs
from ...Persistencia.Lim_Tesoreria import BD_LimTesoreria
from ...Persistencia.Brechas import BD_DataBrechas
from ...Persistencia.I01 import BD_I01
from ...Persistencia.I02 import BD_I02
from ...Persistencia.Entidades import BD_Entidades
from ...Persistencia.Calificaciones import BD_Calificaciones
from ...Persistencia.SP_Balance_FinMes import BD_SP_balance_fm
from ...Utilitarios.Errores import CustomError


class FuentesBD(IFuente):
    def __init__(self, fecha: str, oficina: int, entidad: str):
        self.fecha = fecha
       
        self.oficina = oficina
        self.entidad = entidad
       
        
        
    def obtenerLimTesoreria(self,ruc) -> pd.DataFrame:
        Logs.registrarLog("Inicio obtencion de LimTesoreria", True)
        df = BD_LimTesoreria.consultaLimTesoreria(ruc,self.oficina,self.fecha)
        Logs.registrarLog("Fin obtencion de LimTesoreria", True)
        if df.empty:
            raise CustomError("No existen LimTesoreria para la fecha: "+str(self.fecha)+", entidad= "+ruc)
        return df
    
    def obtenerDataBrechas(self,ruc) -> pd.DataFrame:
        Logs.registrarLog("Inicio obtencion de Brechas", True)
        df = BD_DataBrechas.consultaDataBrechas(ruc,self.fecha)
        Logs.registrarLog("Fin obtencion de Brechas", True)
        if df.empty:
            raise CustomError("No existen Brechas para la fecha: "+str(self.fecha)+", entidad= "+ruc)
        return df
    
    def obtenerI01(self,ruc) -> pd.DataFrame:
        Logs.registrarLog("Inicio obtencion de I01", True)
        df = BD_I01.consultaI01(ruc,self.fecha)
        Logs.registrarLog("Fin obtencion de I01", True)
        if df.empty:
            raise CustomError("No existen I01 para la fecha: "+str(self.fecha)+", entidad= "+ruc)
        return df
    
    
    def obtenerI02(self,ruc) -> pd.DataFrame:
        Logs.registrarLog("Inicio obtencion de I02", True)
        df = BD_I02.consultaI02(ruc,self.fecha)
        Logs.registrarLog("Fin obtencion de I02", True)
        if df.empty:
            raise CustomError("No existen I02 para la fecha: "+str(self.fecha)+", entidad= "+ruc)
        return df
    
    
    def obtenerBalanceEntidad(self) -> pd.DataFrame:
        Logs.registrarLog("Inicio obtencion de Balance Entidad", True)
        df = BD_Entidades.consultaBalanceEntidad(self.fecha)
        Logs.registrarLog("Fin obtencion de Balance Entidad", True)
        if df.empty:
            raise CustomError("No existen Balance entidades para la fecha: "+str(self.fecha))
        return df
    
    
    def obtenerCalificacioneseceb(self) -> pd.DataFrame:
        Logs.registrarLog("Inicio obtencion de Calificaciones eceb", True)
        df = BD_Calificaciones.consultaCalificacioneceb()
        Logs.registrarLog("Fin obtencion de Calificaciones eceb", True)
        if df.empty:
            raise CustomError("No existen Califificaciones eceb")
        return df
    
    
    def obtenerCalificacionesecic(self) -> pd.DataFrame:
        Logs.registrarLog("Inicio obtencion de Calificaciones ecic", True)
        df = BD_Calificaciones.consultaCalificacionesecic
        Logs.registrarLog("Fin obtencion de Calificaciones ecic", True)
        if df.empty:
            raise CustomError("No existen Califificaciones ecic")
        return df
    
    
    def obtenerDataEntidades(self) -> pd.DataFrame:
        Logs.registrarLog("Inicio obtencion de Datos de las entidades", True)
        df = BD_Entidades.consultaDataEntidades(self.fecha)
        Logs.registrarLog("Fin obtencion de Datos de las entidades", True)
        if df.empty:
            raise CustomError("No existen Datos de entidades para la fecha: "+str(self.fecha))
        return df
    
    
    def obtenerSPFmes(self,ruc) :
        Logs.registrarLog("Inicio ejecucion de sp_balances_fmes", True)
        array = BD_SP_balance_fm.consultaSPbalanceFm(self.fecha,self.oficina,ruc)
        Logs.registrarLog("Fin ejecucion de sp_balances_fmes", True)
        return array
    
    
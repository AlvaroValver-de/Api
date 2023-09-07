from abc import ABC, abstractmethod
import pandas as pd

class IFuente(ABC):
    
    @abstractmethod
    def obtenerLimTesoreria(self,ruc:str) -> pd.DataFrame:
         pass
     
     
    @abstractmethod
    def obtenerDataBrechas(self,ruc:str) -> pd.DataFrame:
         pass
    
    
    @abstractmethod
    def obtenerI01(self,ruc:str) -> pd.DataFrame:
         pass
    
    
    @abstractmethod
    def obtenerI02(self,ruc:str) -> pd.DataFrame:
         pass
    
    
    @abstractmethod
    def obtenerBalanceEntidad(self) -> pd.DataFrame:
         pass
    
    @abstractmethod
    def obtenerCalificacioneseceb(self) -> pd.DataFrame:
         pass
    
    @abstractmethod
    def obtenerCalificacionesecic(self) -> pd.DataFrame:
         pass
    
    @abstractmethod
    def obtenerDataEntidades(self) -> pd.DataFrame:
         pass
    
    @abstractmethod
    def obtenerSPFmes(self,ruc:str) :
         pass
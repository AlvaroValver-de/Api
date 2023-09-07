from abc import ABC,abstractmethod
import pandas as pd
import numpy as np
import math
from datetime import date, timedelta, datetime
from functools import reduce
from decimal import *
from dateutil.relativedelta import FR, relativedelta
import itertools
import statistics
import re 
import warnings
from ...Utilitarios.Errores import CustomError
from ..Fuentes.FeunteBD import FuentesBD
import calendar
from ...Utilitarios.Logs import Logs
from ...Utilitarios.Errores import CustomError



class TesoreriaAwm(ABC):
    def __init__(self, fecha: str, oficina: int, entidad: str):
    
        self.fecha = pd.to_datetime(fecha.replace('/','-'))
        
        
        self.oficina = oficina
        self.entidad = entidad
      
        self.fuentes =  FuentesBD(self.fecha, self.oficina, self.entidad)
    
    def verifica_fin_de_mes(self,fecha):
        ultimo_dia_del_mes = calendar.monthrange(fecha.year, fecha.month)[1]

        if fecha.day == ultimo_dia_del_mes:
            Logs.registrarLog("La fecha es el último día del mes.",True)
        else:
            raise CustomError("La fecha "+str(fecha)+" no corresponde a fin de mes.")
    
    
    def get_balances(self):
        RUC = self.entidad
        array = self.fuentes.obtenerSPFmes(RUC)
        resultado = array[0]
        columnas =  array[1]
        tuplas = [tuple(arreglo) for arreglo in resultado] 
        balance = pd.DataFrame(tuplas,columns=columnas) 
        balance.BAL_DATO_NUMERO_CTA=balance.BAL_DATO_NUMERO_CTA.astype('str') 
        balance.BAL_DATO_TOTAL=balance.BAL_DATO_TOTAL.astype(np.float64)
        return balance
    
    def get_data_entidades(self):
        df = self.fuentes.obtenerDataEntidades()
        
        return df 
    
    
    
    def get_data_calificaciones(self):
        df = self.fuentes.obtenerCalificacioneseceb()
        
        df_ =self.fuentes.obtenerCalificacionesecic()
        
        return df,df_ 
    
    
    def get_balance_entidades(self):
        df = self.fuentes.obtenerBalanceEntidad()
        
        return df 
    
    
    def getI02(self):
        ruc= self.entidad
        #df = self.fuentes.obtenerI01(ruc)
        
        df_ = self.fuentes.obtenerI02(ruc)
        
        
        return df_ 
    
    def get_data_brechas(self):
        ruc= self.entidad
        df = self.fuentes.obtenerDataBrechas(ruc)
        
        return df
    
    
    
    def get_lim_tesoreria(self):
        ruc= self.entidad
        df =  self.fuentes.obtenerLimTesoreria(ruc)
        df = df.T
        df = df.rename(columns = {0:'VALOR'})
        return df
    
    
    def tratam_I02(self,df):
        if '1760002600001' == df['TI02_IDENTIFICACION_EMISOR_DEPOSITARIO'][0]:
            df_ = df.drop(index=0)
        else:
            df_ = df.copy()
        df_.index = [i for i in range(len(df_))]
        if 'TI02_FECHA_VENCIMIENTO' not in df_.columns:
            df_['TI02_FECHA_VENCIMIENTO'] = ''
        df_['TI02_FECHA_VENCIMIENTO'] = pd.to_datetime(df_['TI02_FECHA_VENCIMIENTO'], format='%Y-%m-%d')
        return df_
    
    
    def obt_bandas(self,df):
        l = []
        for i in range(len(df)):
            if df['TI02_PLAZO'][i]<=7:
                l.append('1 a 7 dias')
            elif df['TI02_PLAZO'][i]<=15:
                l.append('8 a 15 dias')
            elif df['TI02_PLAZO'][i]<=30:
                l.append('16 a 30 dias')
            elif df['TI02_PLAZO'][i]<=60:
                l.append('31 a 60 dias')
            elif df['TI02_PLAZO'][i]<=90:
                l.append('61 a 90 dias')
            elif df['TI02_PLAZO'][i]<=180:
                l.append('91 a 180 dias')
            elif df['TI02_PLAZO'][i]<=360:
                l.append('181 a 360 dias')
            elif df['TI02_PLAZO'][i]>360:
                l.append('Más de dias')
            else:
                l.append('')
        return l
    
    
    def obtener_tasa_ponderada(self,base,cuenta):
        df = base[base['TI02_CUENTA_CONTABLE_4D'] == cuenta]
        tasa_pon = (df['TI02_TASA_INTERES_NOMINAL']*df['PART_PORTAFOLIO']).sum()/100
        return tasa_pon
    
    def obtener_plazo_ponderado(self,base,cuenta):
        df = base[base['TI02_CUENTA_CONTABLE_4D'] == cuenta]
        plazo_pon = (df['TI02_TASA_INTERES_NOMINAL']*df['PART_PORTAFOLIO']).sum()
        return plazo_pon
    
    def get_brec_pler(self,brechas,letra):
        df = pd.read_json(brechas['INFO_ESTRUCTURA'][0]).T
        df = df.rename(columns = {1:'ESCENARIO',2:'CODIGO',3:'BANDA',4:'SALDO',5:'SALDO INTERES'})
        df = df[df['ESCENARIO']==letra]
        x = df[(df['CODIGO']=='ALN')|(df['CODIGO']=='PLER')]
        df = df[(df['CODIGO']!='ALN')&(df['CODIGO']!='PLER')]
        df['TIPO_CTA'] = [i[0:1] for i in df['CODIGO']]
        df['SALDO'] = df['SALDO'].astype(np.float64)
        df['SALDO INTERES'] = df['SALDO INTERES'].astype(np.float64)
        df = df.groupby(['TIPO_CTA','BANDA'])['SALDO'].sum().unstack(level=0)
        df.eval('BRECHA=A+O-P-G+M-C',inplace=True)
        df['BREC_ACUM'] = df['BRECHA'].cumsum()
        x=pd.pivot(x,index=['CODIGO'],columns=['BANDA'],values=['SALDO']).T
        df['ALN']=x['ALN'].to_list()
        df['PLER']=x['PLER'].to_list()
        df['FECHA'] = brechas['BAL_FECHA'][0]
        df = df[['FECHA','BRECHA', 'BREC_ACUM', 'ALN','PLER']]
        df['BRECHA']    = df['BRECHA'].astype(np.float64)
        df['BREC_ACUM'] = df['BREC_ACUM'].astype(np.float64)
        df['ALN']       = df['ALN'].astype(np.float64)
        df['PLER']      = df['PLER'].astype(np.float64)
        return df
    
    
    def get_calificacion(self,df,calif_externa,calif_interna):
        l = []
        for i in range(len(df.index)):
            try:
                l.append(calif_externa.loc[calif_externa['RUC_ENTIDAD']==df['Identificación Emisor'][i],['ECX_CALIFICACION']].iloc[0,0])
            except:
                l.append('SIN CALIFICACIÓN')
        df['Ultima Calificación'] = l
        ruc = [df.loc[df['Ultima Calificación']=='SIN CALIFICACIÓN',['Identificación Emisor']].iloc[i,0] for i in range(len(df[df['Ultima Calificación']=='SIN CALIFICACIÓN']))]
        l=[]
        for i in range(len(ruc)):
            try:
                l.append(calif_interna.loc[calif_interna['RUC_ENTIDAD']==ruc[i],['ECI_CALIFICACION']].iloc[0,0])
            except:
                l.append('SIN CALIFICACIÓN')
        df.loc[df['Ultima Calificación']=='SIN CALIFICACIÓN',['Ultima Calificación']] = l
        
        l = []
        for i in range(len(df.index)):
            try:
                l.append(calif_externa.loc[calif_externa['RUC_ENTIDAD']==df['Identificación Emisor'][i],['ECX_FIRMA_CAL_RIESGO']].iloc[0,0])
            except:
                l.append('CALIFICACIÓN INTERNA')
        df['Entidad Calificadora'] = l
        df.loc[df['Ultima Calificación']=='SIN CALIFICACIÓN',['Entidad Calificadora']] = 'SIN CALIFICACIÓN'
        l = [(df['Ultima Calificación'][i])[:2] for i in range(len(df))]
        for i in range(len(l)):
            if l[i][1:2]== 'A':
                l[i] = l[i][:1]
            elif l[i][1:2]== 'B':
                l[i] = l[i][:1]
            elif l[i][1:2]== 'I':
                l[i] = l[i][:1]
            elif l[i][1:2]== '+':
                l[i] = l[i][:1]
        df['Guia de Calificación'] = l
        return df
    
    
    
    def get_activo_patrimonio(self,df,bal):
        df['Activo'] = 0
        df['Patrimonio'] = 0
        for i in range(len(df.index)):
            if (df['Identificación Emisor'][i]) in bal['RUC_ENTIDAD'].unique():
                try:
                    df['Activo'][i] = bal.loc[(bal['BDF_DATO_NUMERO_CTA']=='1')&(bal['RUC_ENTIDAD'] == df['Identificación Emisor'][i]),['BDF_DATO_TOTAL']].iloc[0,0]
                    df['Patrimonio'][i] = bal.loc[(bal['BDF_DATO_NUMERO_CTA']=='3')&(bal['RUC_ENTIDAD'] == df['Identificación Emisor'][i]),['BDF_DATO_TOTAL']].iloc[0,0]
                except:
                    df['Activo'][i] = ''
                    df['Patrimonio'][i] = ''
        return df
    
    
    def get_cumple(self,df):
        df['Cumple (1) o no (0) la calificación mínima'] = ''
        for i in range(len(df)):
            if (df['Guia de Calificación'][i] == 'A' and (df['Tipo Emisor'][i] == 'BANCOS PRIVADOS' or df['Tipo Emisor'][i] == 'BANCOS PÚBLICOS')) or (df['Guia de Calificación'][i] == 'A' and (df['Tipo Emisor'][i] == 'SEGMENTO 1' or df['Tipo Emisor'][i] == 'SEGMENTO 2' or df['Tipo Emisor'][i] == 'SEGMENTO 3' or df['Tipo Emisor'][i] == 'SEGMENTO 4') and df['Entidad Calificadora'][i] == 'CALIFICACIÓN INTERNA') or (( df['Guia de Calificación'][i] == 'A-' or df['Guia de Calificación'][i] == 'A') and (df['Tipo Emisor'][i] == 'SEGMENTO 1' or df['Tipo Emisor'][i] == 'SEGMENTO 2' or df['Tipo Emisor'][i] == 'SEGMENTO 3' or df['Tipo Emisor'][i] == 'SEGMENTO 4') and df['Entidad Calificadora'][i] != 'CALIFICACIÓN INTERNA'):
                df['Cumple (1) o no (0) la calificación mínima'][i] = 1
            else:
                df['Cumple (1) o no (0) la calificación mínima'][i] = 0
        return df
    
    
    def get_lim_calif_contraparte(self,I02,riesgo_contraparte,lim_tipo_emisor,lt):
        ## Bancos 
        lim_calif_contra = pd.DataFrame(index=['CALMB','CALMBP'])
        lim_calif_contra['Emisor'] = ['BANCOS PRIVADOS','BANCOS PÚBLICOS']
        lim_calif_contra['Sector'] = ['Sector Financiero Privado','Sector Financiero Públicos']
        lim_calif_contra['Calificación Mínima'] = lt.loc[lim_calif_contra.index]
        lim_calif_contra['Número de Operaciones'] = [len(I02[I02['TI02_SEGMENTO_ENTIDAD']==lim_calif_contra['Emisor'][i]]) for i in range(len(lim_calif_contra['Emisor']))]
        lim_calif_contra['Monto invertido inferior a la calificación mínima'] =  [riesgo_contraparte.loc[(riesgo_contraparte['Tipo Emisor'] == lim_calif_contra['Emisor'][i]) & (riesgo_contraparte['Cumple (1) o no (0) la calificación mínima']==0),'Monto Invertido'].sum() for i in range(len(lim_calif_contra))]
        lim_calif_contra['Monto invertido superior a la calificación mínima'] =  [riesgo_contraparte.loc[(riesgo_contraparte['Tipo Emisor'] == lim_calif_contra['Emisor'][i]) & (riesgo_contraparte['Cumple (1) o no (0) la calificación mínima']==1),'Monto Invertido'].sum() for i in range(len(lim_calif_contra))]
        lim_calif_contra.loc['Total'] = lim_calif_contra.sum(numeric_only=True)

        ## Segmento 1
        lim_calif_contra1 = pd.DataFrame()
        lim_calif_contra1['Emisor'] = ['SEGMENTO 1']
        lim_calif_contra1['Sector'] = ['Sector Financiero Popular y solidario']
        lim_calif_contra1['Calificación Mínima'] = lt.loc['CALMCEX'].iloc[0]
        lim_calif_contra1['Número de Operaciones'] = [len(I02[I02['TI02_SEGMENTO_ENTIDAD']==lim_calif_contra1['Emisor'][0]])]
        lim_calif_contra1['Monto invertido inferior a la calificación mínima'] =  [riesgo_contraparte.loc[(riesgo_contraparte['Tipo Emisor'] == lim_calif_contra1['Emisor'][i]) & (riesgo_contraparte['Cumple (1) o no (0) la calificación mínima']==0),'Monto Invertido'].sum() for i in range(len(lim_calif_contra1))]
        lim_calif_contra1['Monto invertido superior a la calificación mínima'] =  [riesgo_contraparte.loc[(riesgo_contraparte['Tipo Emisor'] == lim_calif_contra1['Emisor'][i]) & (riesgo_contraparte['Cumple (1) o no (0) la calificación mínima']==1),'Monto Invertido'].sum() for i in range(len(lim_calif_contra1))]
        lim_calif_contra1.loc['Total1'] = lim_calif_contra1.sum(numeric_only=True)
        
        ## Segmento 2,3,4,5 y Otros
        lim_calif_contra2 = pd.DataFrame()
        lim_calif_contra2['Emisor'] = ['SEGMENTO 2','SEGMENTO 3','SEGMENTO 4','SEGMENTO 5','OTROS SFPS']
        lim_calif_contra2['Sector'] = 'Sector Financiero Popular y solidario'
        lim_calif_contra2['Calificación Mínima'] = lt.loc['CALMCIN'].iloc[0]
        lim_calif_contra2['Número de Operaciones'] = [len(I02[I02['TI02_SEGMENTO_ENTIDAD']==lim_calif_contra2['Emisor'][i]]) for i in range(len(lim_calif_contra2['Emisor']))]
        lim_calif_contra2['Monto invertido inferior a la calificación mínima'] =  [riesgo_contraparte.loc[(riesgo_contraparte['Tipo Emisor'] == lim_calif_contra2['Emisor'][i]) & (riesgo_contraparte['Cumple (1) o no (0) la calificación mínima']==0),'Monto Invertido'].sum() for i in range(len(lim_calif_contra2))]
        lim_calif_contra2['Monto invertido superior a la calificación mínima'] =  [riesgo_contraparte.loc[(riesgo_contraparte['Tipo Emisor'] == lim_calif_contra2['Emisor'][i]) & (riesgo_contraparte['Cumple (1) o no (0) la calificación mínima']==1),'Monto Invertido'].sum() for i in range(len(lim_calif_contra2))]
        lim_calif_contra2.loc['Total2'] = lim_calif_contra2.sum(numeric_only=True)
        
        ## Otros 
        lim_calif_contra3 = pd.DataFrame()
        lim_calif_contra3['Emisor'] = ['Bolsa de Valores','Otros']
        lim_calif_contra3['Sector'] = ['Mercado de Valores','Otros']
        lim_calif_contra3['Calificación Mínima'] = lt.loc['CALMMB'].iloc[0]
        lim_calif_contra3['Número de Operaciones'] = [len(I02[I02['TI02_SEGMENTO_ENTIDAD']==lim_calif_contra3['Emisor'][i]]) for i in range(len(lim_calif_contra3['Emisor']))]
        lim_calif_contra3['Monto invertido inferior a la calificación mínima'] =  [riesgo_contraparte.loc[(riesgo_contraparte['Tipo Emisor'] == lim_calif_contra3['Emisor'][i]) & (riesgo_contraparte['Cumple (1) o no (0) la calificación mínima']==0),'Monto Invertido'].sum() for i in range(len(lim_calif_contra3))]
        lim_calif_contra3['Monto invertido superior a la calificación mínima'] =  [riesgo_contraparte.loc[(riesgo_contraparte['Tipo Emisor'] == lim_calif_contra3['Emisor'][i]) & (riesgo_contraparte['Cumple (1) o no (0) la calificación mínima']==1),'Monto Invertido'].sum() for i in range(len(lim_calif_contra3))]
        lim_calif_contra3.loc['Total3'] = lim_calif_contra3.sum(numeric_only=True)
        lim_calif_contraparte = pd.concat([
                                            lim_calif_contra,
                                            lim_calif_contra1,
                                            lim_calif_contra2,
                                            lim_calif_contra3,
                                            ])
        val = lim_calif_contra['Número de Operaciones']['Total']+lim_calif_contra1['Número de Operaciones']['Total1']+lim_calif_contra2['Número de Operaciones']['Total2']+lim_calif_contra3['Número de Operaciones']['Total3']
        val1 = lim_calif_contra['Monto invertido inferior a la calificación mínima']['Total']+lim_calif_contra1['Monto invertido inferior a la calificación mínima']['Total1']+lim_calif_contra2['Monto invertido inferior a la calificación mínima']['Total2']+lim_calif_contra3['Monto invertido inferior a la calificación mínima']['Total3']
        val2 = lim_calif_contra['Monto invertido superior a la calificación mínima']['Total']+lim_calif_contra1['Monto invertido superior a la calificación mínima']['Total1']+lim_calif_contra2['Monto invertido superior a la calificación mínima']['Total2']+lim_calif_contra3['Monto invertido superior a la calificación mínima']['Total3']
        lim_calif_contraparte.loc['PTI'] = ['Portafolio Total de Inversiones','','',val,val1,val2]
        lim_calif_contraparte['Concentración']=lim_calif_contraparte['Monto invertido inferior a la calificación mínima']/(lim_calif_contraparte['Monto invertido inferior a la calificación mínima']+lim_calif_contraparte['Monto invertido superior a la calificación mínima'])
        return lim_calif_contraparte
    
    def get_values_table(self,df,I02):
        for i in range(2,len(df.index)):
            for j in range(1,len(df.columns)):
                try:
                    df.iloc[i,j] = (I02.loc[(I02['TI02_BANDA']==df.columns[j])&(I02['TI02_CUENTA_CONTABLE_4D']==df['Bandas de Maduración'][i]),['TI02_VALOR_LIBROS']].sum()).iloc[0]
                    if i in [3,5,7]:
                        df.iloc[i,j] = (I02.loc[(I02['TI02_BANDA']==df.columns[j])&(I02['TI02_CUENTA_CONTABLE_4D']==df['Bandas de Maduración'][i-1]),['TI02_MONTO_INTERES_GENERADO']].sum()).iloc[0]
                except:
                    df.iloc[i,j] = ''
        return df
    
    
    def div0(self,vect1,vect2):
        vect = []
        for i in range(len(vect1)):
            if vect2[i] != 0:
                vect.append(vect1[i]/vect2[i])
            else:
                vect.append(0.0)
        return vect
    
    
    
    def get_saldo_log_vol(self,fecha,bal):
        cuentas = ['1301','1302','1303','1304','1305','1306','1307']
        fechas = pd.date_range(pd.to_datetime(fecha)-pd.offsets.MonthEnd(24),periods=25,freq='M')
        fechas = fechas.sort_values(ascending=False)
        saldo_cartera = pd.DataFrame(index= fechas,columns=cuentas)
        for i in range(len(saldo_cartera.index)):
            for j in range(len(saldo_cartera.columns)):
                try:
                    saldo_cartera.iloc[i,j] = (bal.loc[(bal['BAL_FECHA']==saldo_cartera.index[i])&(bal['BAL_DATO_NUMERO_CTA']==saldo_cartera.columns[j]),['BAL_DATO_TOTAL']]).iloc[0,0]
                except:
                    saldo_cartera.iloc[i,j] = ''
                    
        log_saldo_cartera = saldo_cartera.copy()
        for i in range(len(log_saldo_cartera.index)):
            for j in range(len(log_saldo_cartera.columns)):
                if saldo_cartera.iloc[i,j] != 0:
                    try:
                        log_saldo_cartera.iloc[i,j] = math.log(saldo_cartera.iloc[i+1,j]/saldo_cartera.iloc[i,j])
                    except:
                        log_saldo_cartera.iloc[i,j] = 0.0
        log_saldo_cartera = log_saldo_cartera.fillna(0)
        
        volatilidad = pd.DataFrame(index=fechas[:12],columns=saldo_cartera.columns)
        for i in range(len(volatilidad.index)):
                try:
                    volatilidad.iloc[i,:] = (log_saldo_cartera.loc[log_saldo_cartera.index[i:i+12]]).std()
                except:
                    volatilidad.iloc[i,:] = ''
        return saldo_cartera,log_saldo_cartera,volatilidad

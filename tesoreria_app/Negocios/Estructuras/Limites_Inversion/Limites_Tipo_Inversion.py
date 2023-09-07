from ..Tesoreria import TesoreriaAwm
import pandas as pd
import math
import numpy as np
class Limites_De_Tipo_Inversion(TesoreriaAwm):
    
    
    def _obtenerValores(self):
        self.verifica_fin_de_mes(self.fecha)
        I02 = self.getI02()
        entidades = self.get_data_entidades()
        lt = self.get_lim_tesoreria()
        
        I02 = self.tratam_I02(I02)
        I02['TI02_CUENTA_CONTABLE_4D'] = [(I02['TI02_CUENTA_CONTABLE'][i])[:4] for i in range(len(I02['TI02_CUENTA_CONTABLE']))]
        I02['TI02_SEGMENTO_ENTIDAD'] = [entidades.loc[entidades['RUC_ENTIDAD'] == I02['TI02_IDENTIFICACION_EMISOR_DEPOSITARIO'][i],['ENTIDAD_SEGMENTO']].iloc[0,0] for i in range(len(I02['TI02_IDENTIFICACION_EMISOR_DEPOSITARIO']))]
        I02['TI02_PLAZO'] = [(I02['TI02_FECHA_VENCIMIENTO'][i]-I02['BAL_FECHA'][i]).days for i in range(len(I02))]
        I02['TI02_BANDA'] = self.obt_bandas(I02)
        
        lim_tipo_inversion = self._obtenerValoresTipoInversion(lt,I02)
        return lim_tipo_inversion
    
        
    def _obtenerValoresTipoInversion(self,lt,I02):
        
        ## LIMITES POR TIPO DE INVERSIÓN

        lim_tipo_inversion = pd.DataFrame(index=['LI1301','LI1302','LI1303','LI1304','LI1305','LI1306','LI1307','LI1103'])
        lim_tipo_inversion['Codigo de Cuenta'] = ['1301','1302','1303','1304','1305','1306','1307','1103']
        lim_tipo_inversion['Producto'] = ['A valor razonable con cambios en el estado de resultados de entidades del sector privado y sector financiero popular y solidario',				
                                            'A valor razonable con cambios en el estado de resultados del Estado o de entidades del sector público',
                                            'Disponibles para la venta de entidades del sector privado y sector financiero popular y solidario',
                                            'Disponibles para la venta del Estado o de entidades del sector público',	
                                            'Mantenidas hasta su vencimiento de entidades del sector privado y sector financiero popular y solidario',
                                            'Mantenidas hasta su vencimiento del Estado o de entidades del sector público',
                                            'De disponibilidad restringida',
                                            'Bancos y otras instituciones financieras',
                                            ]
        lim_tipo_inversion['Límite de Concentración'] = lt.loc[lim_tipo_inversion.index]
        lim_tipo_inversion['Límite de Concentración'] = lim_tipo_inversion['Límite de Concentración'].astype(np.float64)
        lim_tipo_inversion['Número de Operaciones'] = [len(I02[I02['TI02_CUENTA_CONTABLE_4D']==lim_tipo_inversion['Codigo de Cuenta'][i]]) for i in range(len(lim_tipo_inversion['Codigo de Cuenta']))]
        lim_tipo_inversion['Monto Invertido'] = [(I02.loc[I02['TI02_CUENTA_CONTABLE_4D']==lim_tipo_inversion['Codigo de Cuenta'][i],['TI02_VALOR_LIBROS']].sum()).iloc[0] for i in range(len(lim_tipo_inversion['Codigo de Cuenta']))]
        lim_tipo_inversion['Monto Invertido'] = lim_tipo_inversion['Monto Invertido'].astype(float)
        lim_tipo_inversion['Concentración'] = lim_tipo_inversion['Monto Invertido']/lim_tipo_inversion['Monto Invertido'].sum()
        lim_tipo_inversion.loc['Total'] = lim_tipo_inversion.sum(numeric_only=True)
        lim_tipo_inversion['Producto']['Total']= 'Portafolio total de Inversiones'
        lim_tipo_inversion = lim_tipo_inversion.fillna('')
        return lim_tipo_inversion # endpoint
    
        
        
 
        
       

    
    
    def _limpiarDatos(self, dataf: pd.DataFrame):
        df = dataf.reset_index(drop=True)
        df =  df.fillna('')
        df = df.rename(columns={'Codigo de Cuenta': '1','Producto':'2','Límite de Concentración':'3','Número de Operaciones':'4',
                                'Monto Invertido':'5','Concentración':'6'})
        
        return df
    

    def getReporte(self) : #funcion final
        
        
        report =self._obtenerValores()
        report =  self._limpiarDatos(report)
            
        
        return report
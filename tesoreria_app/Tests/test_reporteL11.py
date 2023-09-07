import unittest
import pandas as pd
from ..Utilitarios.utilitarios import realizarComparacionDatraframes

'''
Ejecución: 
python .\manage.py test -v3 app_rdml.Tests.test_reporteL11
'''
class Test_ReporteL11(unittest.TestCase):

    #Crea un método que sirve como constructor
    def setUp(self):
        #Se crea una variable de clase
        self.RUTA_BASE_MIA = "D:/Todo Proyecto API Risknadim/rdml_awm_gestion_riesgos/RDML_awm/RDML/reports/"
        self.RUTA_BASE_EXTERNO = "D:/OneDrive - Bigdata C.A/Descargas/rdml/"


    def test_validarIntegridad_1(self):
        RUTA_MIA = self.RUTA_BASE_MIA + "L11_1390067506001_2023-02-28.xlsx"
        RUTA_EXTERNA = self.RUTA_BASE_EXTERNO + "L11_2023-02-28.xlsx"

        #Se leen los excel
        df1 = pd.read_excel(RUTA_MIA)
        df2 = pd.read_excel(RUTA_EXTERNA)

        #SE tratan los campos NAN
        df1 = df1.fillna(-99)
        df2 = df2.fillna(-99)

        #SE colocan los nombre de columnas todos como string
        df1 = df1.rename(columns=str)
        df2 = df2.rename(columns=str)

        realizarComparacionDatraframes("Análisis L11", df1, df2)
        pd.testing.assert_frame_equal(df1, df2)


    def test_validarIntegridad_2(self):
        RUTA_MIA = self.RUTA_BASE_MIA + "L11_1390067506001_2023-03-31.xlsx"
        RUTA_EXTERNA = self.RUTA_BASE_EXTERNO + "L11_2023-03-31.xlsx"

        #Se leen los excel
        df1 = pd.read_excel(RUTA_MIA)
        df2 = pd.read_excel(RUTA_EXTERNA)

        #SE tratan los campos NAN
        df1 = df1.fillna(-99)
        df2 = df2.fillna(-99)

        #SE colocan los nombre de columnas todos como string
        df1 = df1.rename(columns=str)
        df2 = df2.rename(columns=str)

        realizarComparacionDatraframes("Análisis L11", df1, df2)
        pd.testing.assert_frame_equal(df1, df2)

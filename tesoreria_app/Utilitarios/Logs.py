# Para registrar los logs.
# import sys
import logging
from datetime import datetime
import pytz
# sys.path.append("...")
# from RUTAS import RUTA_LOGS, RUTA_BALANCES_DEFECTUOSOS
from RUTAS import RUTA_LOGS

class Logs:
    @staticmethod
    def registrarLog(mensaje: str, soloMensaje: bool = False):
        # SE crea un archivo de logs por día
        nombreArchivoLog = f"LOGS_{datetime.now().date():%Y-%m-%d}.log"
        # Se especifica donde se generarán los reportes
        logging.basicConfig(filename=RUTA_LOGS+nombreArchivoLog,
                            level=logging.WARNING, force=True)

        # Se registra el mensaje
        zonaEcuador = pytz.timezone('America/Guayaquil')
        tiempoEcuador = datetime.now(zonaEcuador)
        formatoTiempo = f"[{tiempoEcuador.date():%d-%m-%Y}] - [{tiempoEcuador.hour}:{tiempoEcuador.minute}:{tiempoEcuador.second}]"
        # Solo se muestra el mensaje que se manda
        if soloMensaje:
            logging.warning(
                f"\n\nMENSAJE= {formatoTiempo}: \n*****{mensaje}*****\n")
        else:
            # Se muestra el mensaje y el traceback del error.
            logging.exception(
                f"\n\nMENSAJE= {formatoTiempo}: \n*****{mensaje}*****\n")

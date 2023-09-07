
class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class SinBalancesError(Error):
    def __init__(self, message="No se encontró información para los parámetros ingresados o no existen balances requeridos."):
        self.message = message
        super().__init__(self.message)


class BalancesIncompletosError(Error):
    def __init__(self, listaFechas, message="Hay fechas que no tienen balances, por favor cargue los balances faltantes y luego vuelva a intentar."):
        self.message = message
        self.miLista = listaFechas
        super().__init__(self.message)


class SinIndicadorConcentracion(Error):
    def __init__(self, message="No se encontró el indicador de concentración."):
        self.message = message
        super().__init__(self.message)


class DatosSupuestosError(Error):
    def __init__(self, message="Error en la carga de datos de supuestos."):
        self.message = message
        super().__init__(self.message)


class SinOficinaConsolidadoError(Error):
    def __init__(self, message="No se encontró la oficina consolidado."):
        self.message = message
        super().__init__(self.message)


class CustomError(Exception):
    def __init__(self, message="Error"):
        self.message = message
        super().__init__(self.message)

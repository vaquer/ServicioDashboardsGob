"""
Modulo que contiene las herramientas
y funciones necesarias para calcular
calificaciones, ordenamientos y datos
complementarios de las dependencias
"""
import requests
import operator
from collections import OrderedDict
from django.core.cache import cache


MEDALLAS = {'bronce': 1, 'plata': 2, 'oro': 3, 'N/A': 0}
ARRAY_MEDALLAS = {0: 'N/A', 1: 'bronce', 2: 'plata', 3: 'oro'}

JSON_DEPENDENCIAS = OrderedDict()
JSON_RECURSOS = OrderedDict()
URL_ADELA = 'http://api.datos.gob.mx/v1/data-fusion?adela.inventory.slug={0}&page={1}'
URL_CKAN = 'http://datos.gob.mx/busca/api/3/action/organization_list'
KEY_DEPEN = 'resumen-dependendencias'
KEY_RECUR = 'descargas-recursos'
CACHE_TTL = 60 * 60 * 27


class NetWorkTablero(object):
    """
    Clase estatica que contiene
    las herramientas de networking
    para comunicarse con las APIS
    """
    @staticmethod
    def recuperar_dependencias():
        """
        Funcion que devuelve la lista de dependencias
        del CKAN API
        Retorno: JSON Dict
        """

        respuesta_ckan = requests.get(URL_CKAN)
        dependencias = respuesta_ckan.json()

        return dependencias.get('result', [])

    @staticmethod
    def llamar_a_buda(depen, pagina=1):
        """
        Funcion que consulta el api de BUDA
        Parametro: (String)dependencia, (Int)pagina
        Retorno: Json Dict
        """
        respuesta_buda = requests.get(URL_ADELA.format(depen, str(pagina)))
        return respuesta_buda.json()


class MatTableros(object):
    """
    Clase estatica que contiene
    las herramientas para calculos
    matematicos sobre las dependencias
    """
    @staticmethod
    def genera_calificacion(calidad, atrasos, descargas, recomendaciones):
        """
        Funcion genera la calificacion ponderada
        de una dependencia
        Retorno: Int
        """
        calificacion_calidad = {'N/A': 0, 'bronce': 40, 'plata': 10, 'oro': 10}
        calificacion = 0

        calificacion += calificacion_calidad[calidad]

        if not atrasos:
            calificacion += 15

        if descargas:
            calificacion += 15

        if not recomendaciones:
            calificacion += 10

        return calificacion / 10

    @staticmethod
    def calcula_mediana(muestreo):
        """
        Funcion calcula la mediana
        de un muestreo
        Retorno: Int
        """
        muestreo_ordenado = sorted(muestreo)
        length = len(muestreo_ordenado)
        if not length % 2:
            a_m = muestreo_ordenado[length / 2]
            b_m = muestreo_ordenado[length / 2 - 1]
            return (a_m + b_m) / 2.0

        return muestreo_ordenado[(len(muestreo) / 2)]

    @staticmethod
    def calcula_ranking(deps):
        """
        Funcion calcula el ranking de una
        dependencia en base a sus atributos
        Retorno: Array
        """
        cal = {value: key['calificacion'] for value, key in deps.iteritems()}

        key_oper = operator.itemgetter(1)
        ordenadas = sorted(cal.items(), key=key_oper, reverse=True)

        aux_dep = None
        count_ord = len(ordenadas)

        for elemento in range(0, count_ord):
            # Recorrido de orden exponencial
            for index in range(0, count_ord):
                if elemento < 1:
                    ordenadas[index] = deps[ordenadas[index][0]]

                if index > 0:
                    if ordenadas[index]['calificacion'] == ordenadas[index - 1]['calificacion']:
                        if ordenadas[index]['descargas'] > ordenadas[index - 1]['descargas']:
                            aux_dep = ordenadas[index - 1]
                            ordenadas[index - 1] = ordenadas[index]
                            ordenadas[index] = aux_dep

        # Generamos la respuesta en un arreglo ordenado
        for elemento in range(0, count_ord):
            ordenadas[elemento]['ranking'] = (elemento + 1)

        return ordenadas

    @staticmethod
    def generar_paginacion(dependencia):
        """
        Funcion que calcula el numero
        total de paginas que se debe
        recorrer por dependencia
        Retorno: Json Dict
        Parametro: (String) dependencia
        """
        json_buda = NetWorkTablero.llamar_a_buda(dependencia)

        datos_totales = json_buda['pagination']['total']
        tamano_pagina = json_buda['pagination']['pageSize']

        paginas_totales = (datos_totales / tamano_pagina)
        paginas_totales += 0 if datos_totales % tamano_pagina == 0 else 1

        return range(1, paginas_totales + 1) if paginas_totales > 1 else [1]

    @staticmethod
    def generar_tablero(dependencia):
        """
        Funcion que recorre todos los recursos
        de una dependencia y devuelve
        el resumen de de sus datos
        Parametro: (String) dependencia
        Retorno: Json Dict
        """
        # Valores iniciales
        apertura_array = []
        apertura = 0
        contador = 0
        calidad = 0
        calificacion = 0
        descargas = 0
        recomendaciones = False
        pendientes = False
        nombre_institucion = ''

        # Se obtienen las paginas a recorrer
        vecindario_de_paginas = MatTableros.generar_paginacion(dependencia)

        for pagina in vecindario_de_paginas:
            json_buda = NetWorkTablero.llamar_a_buda(dependencia, pagina)

            for recurso in json_buda.get('results', []):
                if recurso['calificacion'] != u'none':
                    calidad += MEDALLAS[recurso['calificacion']]
                else:
                    calidad += 1
                try:
                    descargas += recurso['analytics']['downloads']['total']['value']
                    JSON_RECURSOS['{0}'.format(recurso['adela']['resource']['title'].encode('utf-8'))] = recurso['analytics']['downloads']['total']['value']
                except TypeError:
                    descargas += 0
                    JSON_RECURSOS['{0}'.format(recurso['adela']['resource']['title'].encode('utf-8'))] = 0

                if len(recurso['recommendations']) > 0:
                    recomendaciones = True

                if recurso['adela']['resource']['publishDate'] == None or recurso['adela']['resource']['publishDate'] == 'null':
                    pendientes = True

                try:
                    if not nombre_institucion:
                        nombre_institucion = recurso['ckan']['dataset']['organization']['title']
                except TypeError:
                    pass

                apertura_array.append(recurso['adela']['dataset']['openessRating'])
                contador += 1

        # Resultados finales
        if len(apertura_array) > 0:
            apertura = int(MatTableros.calcula_mediana(apertura_array))
        else:
            apertura = 0

        if contador == 0:
            contador = 1
            
        calidad = ARRAY_MEDALLAS[(calidad/contador)]
        calificacion = MatTableros.genera_calificacion(calidad, pendientes, descargas > 0, recomendaciones)


        return {
            'institucion': nombre_institucion or dependencia,
            'apertura': apertura,
            'calidad': calidad,
            'descargas': descargas,
            'slug': dependencia,
            'total': contador,
            'calificacion': calificacion,
            'ranking': 0
        } if len(json_buda.get('results', [])) > 1 else {
            'institucion': nombre_institucion or dependencia,
            'apertura': 0,
            'calidad': 'N/A',
            'descargas': 0,
            'total': 0,
            'calificacion': 0,
            'ranking': 0,
            'slug': dependencia
        }


def scrapear_api_buda():
    """
    Metodo que recorre el API de BUDA
    y obtiene el resumen de cada dependencia
    para guardarlo en cache
    """
    count_dependencias = 0
    for dep in NetWorkTablero.recuperar_dependencias():
        print "Dependencia: {0}".format(dep)
        count_dependencias += 1
        JSON_DEPENDENCIAS[dep] = MatTableros.generar_tablero(dep)

    # Se guarda en cache por 27 horas
    ranking = MatTableros.calcula_ranking(JSON_DEPENDENCIAS)
    cache.set(KEY_DEPEN, ranking, CACHE_TTL)
    cache.set(KEY_RECUR, JSON_RECURSOS, CACHE_TTL)
    print "************************Terminan calculos*************************************"
    print "DEPENDENCIAS PROCESADAS: {0}".format(str(count_dependencias))

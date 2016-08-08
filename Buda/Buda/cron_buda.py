import os
import sys
import requests
import operator
from collections import OrderedDict
from django.core.cache import cache


MEDALLAS = {'bronce': 1, 'plata': 2, 'oro': 3}
ARRAY_MEDALLAS = {1: 'bronce', 2: 'plata', 3: 'oro'}

json_dependendencias = OrderedDict()
json_dependendencias_ordered = []
json_recursos = OrderedDict()


def scrapear_api_buda():
    """
    Metodo que recorre el API de BUDA
    y obtiene el resumen de cada dependencia
    para guardarlo en cache
    """
    for dependencia in recuperar_dependencias():
        print dependencia
        json_dependendencias[dependencia] = calcular_datos_dependencia(dependencia)

    # Se guarda en cache por 27 horas
    cache.set('resumen-dependendencias', calcula_ranking(json_dependendencias), 60 * 60 * 27)
    cache.set('descargas-recursos', json_recursos, 60 * 60 * 27)


def recuperar_dependencias():
    """
    Funcion que devuelve la lista de dependencias
    del CKAN API
    Retorno: JSON Dict
    """
    respuesta_ckan = requests.get('http://datos.gob.mx/busca/api/3/action/organization_list')
    dependencias = respuesta_ckan.json()

    return dependencias.get('result', [])


def generar_vecindario_de_paginacion(dependencia):
    """
    Funcion que calcula el numero
    total de paginas que se debe
    recorrer por dependencia
    Retorno: Json Dict
    Parametro: (String) dependencia
    """
    json_buda = llamar_a_buda(dependencia)

    datos_totales = json_buda['pagination']['total']
    tamano_pagina = json_buda['pagination']['pageSize']

    paginas_totales = (datos_totales / tamano_pagina)
    paginas_totales += 0 if datos_totales % tamano_pagina == 0 else 1

    return range(1, paginas_totales + 1) if paginas_totales > 1 else [1]


def llamar_a_buda(dependencia, pagina=1):
    """
    Funcion que consulta el api de BUDA
    Parametro: (String)dependencia, (Int)pagina
    Retorno: Json Dict
    """
    respuesta_buda = requests.get('http://api.datos.gob.mx/v1/data-fusion?adela.inventory.slug={0}&page={1}'.format(dependencia, str(pagina)))
    return respuesta_buda.json()


def genera_calificacion(calidad, atrasos, descargas, recomendaciones):
    calificacion_calidad = {'bronce': 40, 'plata': 10, 'oro': 10}
    calificacion = 0

    calificacion += calificacion_calidad[calidad]

    if not atrasos:
        calificacion += 15

    if descargas:
        calificacion += 15

    if not recomendaciones:
        calificacion += 10            

    return (calificacion / 10)


def calcula_mediana(muestreo):
    muestreo_ordenado = sorted(muestreo)
    length = len(muestreo_ordenado)
    if not length % 2:
        return (muestreo_ordenado[length / 2] + muestreo_ordenado[length / 2 - 1]) / 2.0

    return muestreo_ordenado[(len(muestreo) / 2)]


def calcula_ranking(dependencias):
    dependencias_calif = { value: key['calificacion'] for value, key in dependencias.iteritems() }

    dependencias_ordenadas = sorted(dependencias_calif.items(), key=operator.itemgetter(1), reverse=True)

    aux_dependencia = None
    lengt_index_ordenada = len(dependencias_ordenadas)

    
    for elemento in range(0, lengt_index_ordenada):
        for index_dependencia in range(0, lengt_index_ordenada):
            
            if elemento < 1:
                dependencias_ordenadas[index_dependencia] = dependencias[dependencias_ordenadas[index_dependencia][0]]
            
            if index_dependencia > 0:
                if dependencias_ordenadas[index_dependencia]['calificacion'] == dependencias_ordenadas[index_dependencia - 1]['calificacion']:
                    if dependencias_ordenadas[index_dependencia]['descargas'] > dependencias_ordenadas[index_dependencia - 1]['descargas']:
                        aux_dependencia = dependencias_ordenadas[index_dependencia - 1]
                        dependencias_ordenadas[index_dependencia - 1] = dependencias_ordenadas[index_dependencia]
                        dependencias_ordenadas[index_dependencia] = aux_dependencia
            
    for elemento in range(0, lengt_index_ordenada):
        dependencias_ordenadas[elemento]['ranking'] = (elemento + 1)

    return dependencias_ordenadas



def calcular_datos_dependencia(dependencia):
    """
    Funcion que recorre todos los recursos
    de una dependencia y devuelve 
    el resumen de de sus datos 
    Parametro: (String) dependencia
    Retorno: Json Dict
    """

    # Valores iniciales
    apertura = 0
    apertura_array = []
    contador = 0
    calidad = 0
    descargas = 0
    tiene_recomendaciones = False
    tiene_pendientes = False
    nombre_institucion = ''

    # Se obtienen las paginas a recorrer
    vecindario_de_paginas = generar_vecindario_de_paginacion(dependencia)

    for pagina in vecindario_de_paginas:
        json_buda = llamar_a_buda(dependencia, pagina)
        resultados_pagina_json_buda = json_buda.get('results', [])

        for recurso in resultados_pagina_json_buda:
            if recurso['calificacion'] != u'none':
                calidad += MEDALLAS[recurso['calificacion']]
            else:
                calidad += 1 
            try:
                descargas += recurso['analytics']['downloads']['total']['value']
                json_recursos['{0}'.format(recurso['adela']['resource']['title'].encode('utf-8'))] = recurso['analytics']['downloads']['total']['value']
            except:
                descargas += 0
                json_recursos['{0}'.format(recurso['adela']['resource']['title'].encode('utf-8'))] = 0

            if len(recurso['recommendations']) > 0:
                tiene_recomendaciones = True

            if recurso['adela']['resource']['publishDate'] == None or recurso['adela']['resource']['publishDate'] == 'null':
                tiene_pendientes = True

            try:
                if not nombre_institucion:
                    nombre_institucion = recurso['ckan']['dataset']['organization']['title']
            except:
                pass

            apertura += recurso['adela']['dataset']['openessRating']
            apertura_array.append(recurso['adela']['dataset']['openessRating'])
            contador += 1
        
    if contador == 0:
        contador = 1

    return {
        'institucion': nombre_institucion if nombre_institucion else dependencia,
        'apertura': int(calcula_mediana(apertura_array)),
        'calidad': ARRAY_MEDALLAS[(calidad/contador)],
        'descargas': descargas,
        'slug': dependencia,
        'total': contador,
        'calificacion': genera_calificacion(ARRAY_MEDALLAS[(calidad/contador)], tiene_pendientes, descargas > 0, tiene_recomendaciones),
        'ranking': 0
    } if len(resultados_pagina_json_buda) > 1 else {'institucion': nombre_institucion if nombre_institucion else dependencia, 'apertura': 0, 'calidad': 'N/A', 'descargas': 0, 'total': 0, 'calificacion': 0, 'ranking': 0, 'slug': dependencia}

#scrapear_api_buda()

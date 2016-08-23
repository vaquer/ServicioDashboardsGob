"""
Modulo que controla
las vistas de la aplicacion
"""
import operator
from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse, Http404
from .buda_tools import scrapear_api_buda


def tabla_comparativa(request):
    """
    Vista principal de la tabla
    de instituciones y resumen de
    calificaciones de las mimas
    URL: /tablero-instituciones/
    """
    return render(request, 'tabla-comparativa.html', {'settings': settings})


def detalle_institucion(request, slug=''):
    """
    Vista detalle de una institucion
    en calificaciones y estadisticas
    URL: /tablero-instituciones/detalle-institucion/{slug}/
    """
    template = 'detalle-dependencia.html'
    return render(request, template, {'settings': settings, 'slug': slug})


def genera_resumen_dependencias(request):
    """
    Vista que renueva el resumen
    de las varibales de las dependencias
    URL: /tablero-instituciones/generar-resumen/
    RESPUESTA: Json
    Metodo Http: POST
    """
    if request.method != 'POST':
        raise Http404

    scrapear_api_buda()
    return JsonResponse({'status': 'ok'})


def api_comparativa(request):
    """
    Vista que retorna el calculo
    de las varibales de las dependencias
    URL: /tablero-instituciones/apicomparativa/
    RESPUESTA: Json
    """
    dependencias_cache = cache.get('resumen-dependendencias', None)
    return JsonResponse({'dependencias': dependencias_cache})


def recursos_mas_descargados(request):
    """
    Vista que retorna el Top 5
    de recursos mas descargados
    URL: tablero-instituciones/apicomparativa/recursos-mas-descargados/
    RESPUESTA: Json
    """
    recursos = cache.get('descargas-recursos', None)
    recursos_ordenados = []

    if recursos is not None:
        ky = operator.itemgetter(1)
        recursos_ordenados = sorted(recursos.items(), key=ky, reverse=True)[:5]

    return JsonResponse({'recursos': recursos_ordenados}, safe=False)

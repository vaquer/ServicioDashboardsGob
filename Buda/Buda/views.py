import operator
from django.core.cache import cache
from django.http import JsonResponse
from .cron_buda import scrapear_api_buda


def home(request):
    """
    Vista que retorna el calculo
    de las varibales de las dependencias
    """
    dependencias_cache = cache.get('resumen-dependendencias', None)
    if not dependencias_cache:
        scrapear_api_buda()
        dependencias_cache = cache.get('resumen-dependendencias', {})

    return JsonResponse({'dependencias': dependencias_cache})


def recursos_mas_descargados(request):
    """
    Vista que retorna el Top 5
    de recursos mas descargados
    """
    recursos = cache.get('descargas-recursos', None)
    respuesta_ordenada = {}

    if not None:
        recursos_ordenados = sorted(recursos.items(), key=operator.itemgetter(1), reverse=True)[:5]

    return JsonResponse({'recursos': recursos_ordenados}, safe=False)
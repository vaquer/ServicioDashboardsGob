from django.core.cache import cache
from django.http import JsonResponse
from .cron_buda import scrapear_api_buda


def home(request):
	dependencias_cache = cache.get('resumen-dependendencias', None)
	if not dependencias_cache:
		scrapear_api_buda()
		dependencias_cache = cache.get('resumen-dependendencias', {})

    return JsonResponse(dependencias_cache)


def recursos_mas_descargados(request):
    recursos = cache.get('descargas-recursos', None)
    respuesta_ordenada = {}

    if not None:
		recursos_ordenados = sorted(recursos, key=recursos.__getitem__, reverse=True)[:5]
		respuesta_ordenada = {recurso: recursos[recurso] for recurso in recursos_ordenados}

    return JsonResponse(respuesta_ordenada, safe=False)
from django.core.cache import cache
from django.http import JsonResponse


def home(request):
    return JsonResponse(cache.get('resumen-dependendencias'))


def recursos_mas_descargados(request):
    recursos = cache.get('descargas-recursos')
    recursos_ordenados = sorted(recursos, key=recursos.__getitem__, reverse=True)[:5]

    return JsonResponse({recurso: recursos[recurso] for recurso in recursos_ordenados}, safe=False)
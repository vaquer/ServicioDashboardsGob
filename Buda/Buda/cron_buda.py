"""
Modulo que contiene las herramientas
y funciones necesarias para calcular
calificaciones, ordenamientos y datos
complementarios de las dependencias
"""
import sys
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Buda.settings")
CURRENT = os.path.dirname(__file__)
sys.path.insert(0, os.path.realpath(os.path.join(CURRENT, '../')))
application = get_wsgi_application()

if __name__ == '__main__':
    from Buda.buda_tools import scrapear_api_buda
    #scrapear_api_buda()
    print "Hola!"


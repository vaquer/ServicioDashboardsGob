# ServicioDashboardsGob
Esta herramienta permite a los usuarios tener una vista comparativa de los datos resumidos de las dependencias.
La herramienta esta construida en [Django 1.9.7](https://docs.djangoproject.com/en/1.9/) y diseñada para correr en ambientes
con sistema operativo Linux.

Nota. Los comandos para la instalación corren sobre Ubuntu 15.10.

# Instalación Local

### Requerimientos Locales
- [Python](https://www.python.org/download/releases/2.7/)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)
- [Redis](http://redis.io/)

### Instalación
Los siguientes pasos asumen que se han instalado los requerimientos señalados anteriormente. Correr los siguientes comandos:
```shell
  git clone git@github.com:vaquer/ServicioDashboardsGob.git
  virtualenv {{TU_VIRTUALENV}}
  . {{TU_VIRTUALENV}}/bin/activate
  pip install -r ServicioDashboardsGob/requirements.txt
```

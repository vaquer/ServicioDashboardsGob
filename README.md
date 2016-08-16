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

### Uso
Para poder ver la herramienta corra el siguiente comando:
```
   python ServicioDashboardsGob/Buda/manage.py runserver
```
Despues en el navegador:
```
http://127.0.0.1:8000/tablero-instituciones/
```

# Instalación Docker
### Instalación
Para los siguientes pasos se require tener instalada la plataforma Docker_ en el servidor aplicativo.

En el servidor aplicativo construimos la imagen del contenedor:
```
  git clone git@github.com:opintel/TransformaDocumentos.git
  docker build -t tableros ServicioDashboardsGob/Buda/Docker/.
```
### Uso
Una vez construida la imagen Docker de la herramienta, ya es posible generar el contenedor donde estara ejecutandose la herramienta. Un punto a considerar antes de avanzar con la creación del contenedor es que el contenedor hace uso de la tecnologia Redis como background en el manejo de la información procesada, por lo que se necesita crear un contenedor Docker con Redis y conectarlo al contenedor aplicativo.

Los comandos de consola para correr la aplicacion con toda la arquitectura necesaria son los siguientes:
```
  docker run --name redistableros -p 6379:6379 -d redis
  docker run --name tableros -e SECRET_KEY="{{secret_key}}" --link redistableros:redis -e FQDN="http://tudominio.com/" -e DEBUG=False -p 80:80 tableros
```

Despues en el navegador:
```
http://tudominio.com/tablero-instituciones/
```
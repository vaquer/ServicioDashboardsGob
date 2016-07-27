FROM ubuntu:14.04
MAINTAINER Francisco Vaquero <akura11.tt@gmail.com>

RUN apt-get update && \
	apt-get install -y python-virtualenv git && \

RUN mkdir /project && touch /var/log/buda.log && /var/log/test.log && \
	git clone https://github.com/vaquer/HerramientaFormatosGob.git /project && \
    pip install -r /project/requirements.txt

EXPOSE 8000

ADD cron.d /etc/cron.d

CMD ["python", "project/Buda/manage.py", "runserver", "0.0.0.0:8000"]

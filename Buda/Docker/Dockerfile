FROM ubuntu:14.04
MAINTAINER Francisco Vaquero <akura11.tt@gmail.com>

RUN apt-get update && \
	apt-get install -y supervisor python-virtualenv git

RUN mkdir /project && touch /var/log/buda.log && touch /var/log/test.log && touch /var/log/budacron.log && \
	git clone https://github.com/vaquer/ServicioDashboardsGob.git /project && \
    pip install -r /project/requirements.txt

EXPOSE 8000

COPY buda_cron.conf /etc/supervisor/conf.d/buda_cron.conf
#COPY supervisord.conf /etc/supervisor/supervisord.conf

ADD cron.d /etc/cron.d/cron.d
ADD start.sh /start.sh
RUN chmod 0644 /etc/cron.d/cron.d

#CMD ["python", "project/Buda/manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["/start.sh"]

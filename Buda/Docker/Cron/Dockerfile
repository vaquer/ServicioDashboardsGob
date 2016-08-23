FROM python:2-alpine
MAINTAINER Francisco Vaquero <akura11.tt@gmail.com>

RUN apk add git bash --update-cache && rm -rf /var/cache/apk/*

RUN mkdir /project && touch /var/log/buda.log && \
    git clone https://github.com/vaquer/ServicioDashboardsGob.git /project && \
    pip install -r /project/requirements.txt

COPY cron.d /var/spool/cron/crontabs/root
RUN chmod +x  /project/Buda/Buda/cron_buda.py
CMD crond -l 2 -f
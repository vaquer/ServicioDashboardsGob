# placed in /etc/cron.d 

0 1 * * * python /project/Buda/Buda/cron_buda.py >> /var/log/buda.log
*/1 * * * * python /project/Buda/Buda/cron_buda.py >> /var/log/buda.log
*/1 * * * * echo "Hola" >> /var/log/buda.log
# placed in /etc/cron.d 

0 1 * * * root python /project/Buda/Buda/cron_buda.py >> /var/log/buda.log
*/1 * * * * root python /project/Buda/Buda/cron_buda.py >> /var/log/buda.log
*/1 * * * * root python print "Hola" >> /var/log/buda.log
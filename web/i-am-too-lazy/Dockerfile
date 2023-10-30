FROM php:7.2-apache
COPY ./web/ /var/www/html/
COPY flagfiles/* /

RUN chmod 0555 /var/www/html \
&& find /var/www/html -type d -iname "*" -print0 | xargs -I {} -0 chmod 0544 {} \
&& chmod 0555 /var/www/html/config \
&& chmod 0444 /Hey.txt /Heyhey.txt /Heyheyhey.txt /Heyheyheyhey.txt


EXPOSE 80
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
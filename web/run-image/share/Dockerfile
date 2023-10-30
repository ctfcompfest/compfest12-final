FROM richarvey/nginx-php-fpm

WORKDIR /var/www/html
COPY ./web .
RUN mkdir uploads

RUN echo "this_is_not_the_flag" > /flag_randomstring.txt

CMD ["/start.sh"]
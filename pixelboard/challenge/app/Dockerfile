FROM php:8.2-apache

RUN apt-get update \
    && apt-get install -y --no-install-recommends libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && docker-php-ext-install pdo pdo_sqlite \
    && a2enmod rewrite \
    && { \
        echo "date.timezone=UTC"; \
        echo "file_uploads=On"; \
        echo "upload_max_filesize=5M"; \
        echo "post_max_size=6M"; \
    } > /usr/local/etc/php/conf.d/pixelboard.ini

COPY src/ /var/www/html/
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN mkdir -p /var/www/html/uploads /var/www/data \
    && chmod +x /usr/local/bin/docker-entrypoint.sh \
    && chown -R www-data:www-data /var/www/html/uploads /var/www/data

EXPOSE 80
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["apache2-foreground"]

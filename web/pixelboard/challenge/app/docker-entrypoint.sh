#!/bin/sh
set -e

if [ ! -f /var/www/html/uploads/default.png ]; then
    echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=" \
        | base64 -d > /var/www/html/uploads/default.png
    chown www-data:www-data /var/www/html/uploads/default.png
fi

echo "${FLAG}" > /flag.txt
chmod 644 /flag.txt

exec "$@"

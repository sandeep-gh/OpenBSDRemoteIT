. /tmp/env.sh
certbot -n --nginx -d www.$1.$2 -m $3 --agree-tos

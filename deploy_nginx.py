import os
import sys
import subprocess
from execUtils import exec_cmd, checkIfProcessRunning
import logging

logging.basicConfig(filename="deploy_nginx.log", level=logging.INFO)


def install():
    try:
        precondition = os.path.exists(
            "/etc/nginx/nginx.conf") and ("include /etc/nginx/" not in open("/etc/nginx/nginx.conf", "r").read())
        logging.info(f"precondition = {precondition}")

        if precondition:
            os.system("doas mv /tmp/nginx.conf /etc/nginx/")

            # grant permission
            os.system("doas chown -R www:www /var/log/nginx")
            os.system("doas mkdir -p /var/cache/nginx")
            os.system("doas chown -R www:www /var/cache/nginx")
            os.system("doas mkdir /etc/nginx/conf.d")
            logging.info("successfully configured nginx")

    except Exception as e:
        logging.info("configure nginx failed ", e)
        sys.exit()

    if not checkIfProcessRunning("nginx"):
        os.system("doas /usr/sbin/nginx &")


if os.path.exists("/tmp/env.sh"):
    install()

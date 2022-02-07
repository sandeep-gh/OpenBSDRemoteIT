#proj, gdal, geos, tiff, protobuf, readline
#dependency: iconv

import importlib
import os
import time
from execUtils import exec_cmd, pip_install
import subprocess
import wget
import logging
logging.basicConfig(filename="install_nginx.log", level=logging.INFO)

CXX = "/usr/bin/c++"

version = "1.20.2"
name = "nginx"
geturl = f"https://nginx.org/download/{name}-{version}.tar.gz"


def openssl():
    install_basedir = os.environ['install_basedir']  # '/home/shared'
    os.chdir(install_basedir)
    version = "1.1.1m"
    name = "openssl"
    geturl = f"https://www.openssl.org/source/{name}-{version}.tar.gz"
    os.chdir("downloads")
    if not os.path.exists(f"{name}-{version}"):
        # fn = wget.download(geturl) #workaround
        os.system(f"""wget '{geturl}'""")
        os.system(f"gunzip {name}-{version}.tar.gz")
        os.system(f"tar xvf {name}-{version}.tar")

    openssl.version = version


def install(force_rebuild=False):

    #os.system("""doas python3 -m pip install certbot-nginx""")
    # pip_install("certbot-nginx")
    openssl()
    install_basedir = os.environ['install_basedir']  # '/home/shared'
    os.chdir(install_basedir)
    os.chdir("downloads")
    if not os.path.exists(f"{name}-{version}"):
        #fn = wget.download(geturl)
        os.system(f"""wget '{geturl}'""")
        os.system(f"gunzip {name}-{version}.tar.gz")
        os.system(f"tar xvf {name}-{version}.tar")

    try:
        os.chdir(f"{install_basedir}/Builds/")
        if not os.path.exists(f"{name}-{version}"):
            os.makedirs(f"{name}-{version}")
            os.chdir(f"{install_basedir}/downloads/{name}-{version}")
            build_cmd = f""". /tmp/env.sh ;
            ./configure --prefix={install_basedir}/Builds/{name}-{version} \
            --sbin-path=/usr/sbin/nginx \
            --modules-path=/usr/lib64/nginx/modules  \
            --conf-path=/etc/nginx/nginx.conf \
            --error-log-path=/var/log/nginx/error.log \
            --http-log-path=/var/log/nginx/access.log \
            --pid-path=/var/run/nginx.pid \
            --lock-path=/var/run/nginx.lock \
            --http-client-body-temp-path=/var/cache/nginx/client_temp \
            --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
            --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
            --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
            --http-scgi-temp-path=/var/cache/nginx/scgi_temp \
            --user=www \
            --group=www   \
            --with-compat \
            --with-threads \
            --with-http_addition_module \
            --with-http_auth_request_module \
            --with-http_dav_module \
            --with-http_flv_module \
            --with-http_gunzip_module \
            --with-http_gzip_static_module \
            --with-http_mp4_module \
            --with-http_random_index_module \
            --with-http_realip_module \
            --with-http_secure_link_module \
            --with-http_slice_module \
            --with-http_ssl_module \
            --with-http_stub_status_module \
            --with-http_sub_module \
            --with-http_v2_module \
            --with-mail \
            --with-mail_ssl_module \
            --with-stream \
            --with-stream_realip_module \
            --with-stream_ssl_module \
            --with-stream_ssl_preread_module \
            --with-openssl=/home/shared/downloads/openssl-{openssl.version}/
            
            make
            doas make install
            """
            print(build_cmd)
            os.system(build_cmd)
            logging.info("Successfully installed")
        else:
            logging.info("nginx already installed")
            # ==================== path ownerships ===================
            # /var/log/nginx
            # /var/run/nginx
            # /var/run/nginx.pid
            # =============================== done ===============================
    except Exception as e:
        print(e)
        logging.info(f"errored:cleaning up: {e}")
        os.chdir(f"{install_basedir}")
        os.rmdir(f"Builds/{name}-{version}")


# os.chdir(f"{project_root}")

if os.path.exists("/tmp/env.sh"):
    print("installing..")
    install()

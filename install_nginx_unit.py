# TODO: what about process isolation

#proj, gdal, geos, tiff, protobuf, readline
#dependency: iconv

import importlib
import os
import wget
import logging
logging.basicConfig(filename="install_nginx_unit.log", level=logging.INFO)


version = "1.26.1"
name = "unit"
geturl = f"https://unit.nginx.org/download/{name}-{version}.tar.gz"


def install(force_rebuild=False):

    install_basedir = os.environ['install_basedir']  # '/home/shared'
    os.chdir(install_basedir)
    os.chdir("Builds")
    if not os.path.exists(f"{name}-{version}"):
        #fn = wget.download(geturl)
        # print(fn)
        os.chdir(install_basedir)
        os.chdir("downloads")
        os.system(f"wget {geturl}")
        os.system(f"gunzip {name}-{version}.tar.gz")
        os.system(f"tar xvf {name}-{version}.tar")

    try:
        os.chdir(f"{install_basedir}/Builds/")
        if not os.path.exists(f"{name}-{version}") or force_rebuild:
            os.makedirs(f"{name}-{version}")
            os.chdir(f"{install_basedir}/downloads/{name}-{version}")
            build_cmd = f""". /tmp/env.sh;
            ./configure --prefix=/home/shared/Builds/{name}-{version}  --openssl  --user=www --group=www --ld-opt="-L/usr/local/lib/eopenssl11/ -Wl,-rpath /usr/local/lib/eopenssl11/ -lssl -lcrypto"  --cc-opt="-fPIC -I/usr/local/include/eopenssl11 --debug";
            . /tmp/env.sh;
            ./configure  python  --lib-path={install_basedir}/Builds/Python-3.10/lib  --config=/home/shared/Builds/Python-3.10/bin/python3.10-config
            make 
            make install

            """
            os.system(build_cmd)
            logging.info("unit successfully installed")
    except Exception as e:
        print(e)
        os.chdir(f"{install_basedir}")
        os.rmdir(f"Builds/{name}-{version}")
        logging.info(f"couldn't install unit {e}")


# os.chdir(f"{project_root}")

if os.path.exists("/tmp/env.sh"):
    install()

import importlib
import os
import time
import subprocess
import wget
import logging

logging.basicConfig(filename="install_python.log", level=logging.INFO)

CXX = "/usr/bin/c++"
CC = "/usr/bin/cc"


version = "3.10"
minor = "2"
name = "Python"
geturl = f"https://www.python.org/ftp/python/{version}.{minor}/{name}-{version}.{minor}.tar.xz"
print(geturl)


def install():
    install_basedir = os.environ['install_basedir']  # '/home/shared'
    os.system("""
    mkdir /home/shared/downloads
    mkdir /home/shared/Builds
    """)
    os.chdir(f"{install_basedir}/downloads/")
    if not os.path.exists(f"{name}-{version}.{minor}"):
        fn = wget.download(geturl)
        os.system(f"unxz {name}-{version}.{minor}.tar.xz")
        os.system(f"tar xvf {name}-{version}.{minor}.tar")

    os.chdir(f"{install_basedir}/Builds")
    try:
        if not os.path.exists(f"{name}-{version}"):
            os.chdir(f"{install_basedir}/downloads/{name}-{version}.{minor}")
            build_cmd = f"""CC={CC} CXX={CXX}  OPENSSL_LDFLAGS="-L/usr/local/lib" OPENSSL_LIBS="-lssl -lcrypto" OPENSSL_INCLUDES=-I/usr/local/include  CFLAGS="-fPIC"   ./configure --prefix={install_basedir}/Builds/Python-{version}  --enable-optimizations --with-lto --with-computed-gotos --with-system-ffi  --with-openssl-rpath=auto --with-openssl=/usr/local  --enable-shared
            make -j 4
            make altinstall
            """
            os.system(build_cmd)
            os.chdir(f"{install_basedir}/Builds/{name}-{version}/bin")
            os.system("ln -s python3.10 python3")
        else:
            logging.info("will not build-- python3.10 already present")
    except Exception as e:
        logging.info("unable to install..cleaning up")
        os.chdir(f"{install_basedir}")
        os.rmdir(f"Builds/{name}-{version}")


if os.path.exists("/tmp/env.sh"):
    install()

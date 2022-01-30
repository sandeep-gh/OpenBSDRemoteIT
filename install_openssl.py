import importlib
import os
import time
import subprocess
import logging
logging.basicConfig(filename='install_openssl.log',
                    level=logging.INFO)
if not os.path.exists("/usr/local/lib/libssl.a"):
    os.chdir("""/usr/ports/security/openssl/1.1""")
    os.system("""
    doas patch -p1 < /tmp/openssl_makefile.patch
    """)
    os.system("""
    make PKG_CREATE_NO_CHECKS=Yes install
    """)
    os.system("""cd /usr/local/include
        doas ln -s  eopenssl11/openssl .
        cd /usr/local/lib
        doas ln -s eopenssl11/libssl.a .
        doas ln -s eopenssl11/libcrypto.a .""")
    logging.info("openssl installed successfully")
else:
    logging.info("openssl already installed")

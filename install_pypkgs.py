import logging
from execUtils import exec_cmd, pip_install
logging.basicConfig(filename="install_pypkgs.log", level=logging.INFO)


pip_install("wget")
pip_install("psutil")
pip_install("cryptography")
pip_install("cffi")
pip_install("certbot-nginx")
logging.info("done installation")

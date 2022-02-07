import os
import logging
from execUtils import exec_cmd, checkIfProcessRunning
logging.basicConfig(filename="deploy_nginx_unit.log", level=logging.INFO)

version = "1.26.1"
name = "unit"


def install():
    install_dir = os.environ['install_basedir']
    # os.system("""doas useradd -s /usr/local/bin/zsh -p $2b$08$CfofWxG6NNLue9fmT4mThuec7WeJ01C0SrNbKPBjB.bz9UnCexkCG  -L daemon unit""")

    if checkIfProcessRunning("unit"):
        logging.info("unit already running")
        return

    os.chdir(f"{install_dir}")

    if not os.path.exists("/var/run"):
        os.system("doas mkdir /var/run/")
    if not os.path.exists("/var/run/unit"):
        os.system("doas mkdir /var/run/unit")
    if not os.path.exists("/var/lib"):
        os.system("doas mkdir /var/lib/")
    if not os.path.exists("/var/lib/unit"):
        os.system("doas mkdir /var/lib/unit")
    if not os.path.exists("/var/tmp"):
        os.system("doas mkdir /var/tmp/")
    if not os.path.exists("/var/tmp/unit"):
        os.system("doas mkdir /var/tmp/unit")
    if not os.path.exists("/var/log/unit"):
        os.system("doas mkdir /var/log/unit")

    os.system(
        "doas chown -R www:www /var/run/unit /var/log/unit /var/lib/unit /var/tmp/unit")
    os.system(
        f"doas {install_dir}/Builds/{name}-{version}/sbin/unitd --control unix:/var/run/unit/control.sock  --pid /var/run/unit.pid --log /var/log/unit/unit.log --modules {install_dir}/modules --state /var/lib/unit/ --tmp /var/tmp/unit/")


if os.path.exists("/tmp/env.sh"):
    install()

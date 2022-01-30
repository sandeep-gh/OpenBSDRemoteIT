from execUtils import exec_cmd, pip_install
import os
import subprocess
import logging
logging.basicConfig(filename='bootstrap_for_adming.log',
                    level=logging.INFO)


passwords = open(".passwords").read().split()


def mkdir(adir):
    if not os.path.exists(adir):
        os.mkdir(adir)
    else:
        logging.info(f"{adir} already present")


exec_cmd("groupadd -g 1002 shared".split(), "is a duplicate")
exec_cmd(["useradd",  "-m", "-b", "/home",
          "-L", "staff", "-s", "/bin/ksh", "-p", f"\'{passwords[0]}\'", "adming"], "already a")
exec_cmd("usermod -G shared adming".split(), "")

os.system(f"""
touch /etc/doas.conf
""")

mkdir("/home/adming/.ssh")
if not os.path.exists("/home/adming/.ssh/authorized_keys"):
    os.system("""su adming -c 'touch /home/adming/.ssh/authorized_keys'""")
os.system(
    """su  adming -c '/bin/cat /tmp/id_rsa.pub >> /home/adming/.ssh/authorized_keys'""")


setup_ports = """
    usermod -G _pbuild adming
    pkg_add portslist
    """
os.system(setup_ports)

if "permit keepenv nopass adming as root" not in open("/etc/doas.conf").read():
    os.system("""
    echo "permit keepenv nopass adming as root" >> /etc/doas.conf
    echo "permit keepenv nopass adming as _pbuild" >> /etc/doas.conf
    echo "permit keepenv nopass adming as _pfetch" >> /etc/doas.conf
    """)

else:
    logging.info("user already as doas")


pip_install("wget", "/usr/local/bin/pip3.8")

os.system("""
    mkdir /home/shared
    chown -R adming:shared  /home/shared
""")

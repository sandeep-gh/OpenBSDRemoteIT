import os
import subprocess
import sys
from typing import List
import psutil
import logging


def pip_install(pkg: str, pipbin: str = ""):
    all_pkgs = [_.decode('ascii').lower() for _ in subprocess.check_output(
        [f"{pipbin}", 'list']).split()]
    if pkg in all_pkgs:
        logging.info(f"pkg= , {pkg},  is present")
        return "already present"
    else:
        os.system(f"{pipbin} install {pkg}")
        return "installed"


class Error:
    pass


error = Error()


def exec_cmd(cmdl: List[str], errcheck: str):
    """

    """
    try:
        res = subprocess.check_output(cmdl, stderr=subprocess.STDOUT)
        return res

    except subprocess.CalledProcessError as e:
        if errcheck in str(e.output):
            logging.info(f"{cmdl[0]} already active")
        else:
            raise e


def append_to_file(fullfp: str, apstr: str):
    dirn = os.path.dirname(fullfp)
    fn = os.path.basename(fullfp)
    if os.path.exists(fullfp):
        os.system(f"doas cp {fullfp} {fullfp}.premod")
        os.system(f"cp {fullfp} /tmp/{fn}")

    with open(f"/tmp/{fn}", "a") as fh:
        fh.write(apstr)
    os.system(f"doas mv /tmp/{fn} {fullfp}")


def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

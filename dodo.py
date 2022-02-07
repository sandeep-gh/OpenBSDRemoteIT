import importlib
import logging
import os
import clushUtils
from deployConfig import targetNode, logDir, install_basedir, maintainer_email
from manage_env import build_env, add_to_env
from pathlib import Path
import logging

homeDir = str(Path.home())

DOIT_CONFIG = {
    'verbosity': 2,  # realtime print statement
}


def setup_env():
    add_to_env("install_basedir", install_basedir)
    with open(f"{logDir}/initDeployment.log", "w") as fh:
        fh.write(build_env())
        print("env = ", build_env())


def task_initDeployment():
    return {'actions': [(setup_env)],
            'targets': [f'{logDir}/initDeployment.log'],
            'file_dep': ["deployConfig.py"],
            }


def task_bootstrap_for_adming():
    """
    """
    return {'actions': [(clushUtils.exec_script, [targetNode, "bootstrap_for_adming.py"],
                         {
                             'dependsFiles': [".passwords", f"{homeDir}/.ssh/id_rsa.pub"],
                             'user':"root",
                             'manageEnv': False,
                             'dependsPkgs':['py3-pip', 'py3-psutil', 'curl'],
                             'logOutput': 'bootstrap_for_adming.log'
    }
    )
    ],
        'targets': [f'{logDir}/bootstrap_for_adming.log.{targetNode}'],
        'file_dep': ["deployConfig.py"],
    }


def task_setup_ports():
    """
    """
    print("targetNode = ", logDir)
    return {'actions': [(clushUtils.exec_script, [targetNode, "setup_ports.py"],
                         {
                             'dependsFiles': [],
                             'user':"adming",
                             'manageEnv': False,
                             'dependsPkgs':[],
                             'logOutput': 'setup_ports.log'
    }
    )
    ],
        # [f'{logDir}/setup_ports.log.{targetNode}'],
        'targets': [f'{logDir}/setup_ports.log.{targetNode}'],
        'file_dep': ["deployConfig.py"],
    }


def task_install_openssl():
    """
    """
    return {'actions': [(clushUtils.exec_script, [targetNode, "install_openssl.py"],
                         {
                             'dependsFiles': ["openssl_makefile.patch"],
                             'user':"adming",
                             'manageEnv': False,
                             'dependsPkgs':[],
                             'logOutput': 'install_openssl.log'
    }
    )
    ],
        'targets': [f'{logDir}/install_openssl.log.{targetNode}'],
        'file_dep': ["deployConfig.py"],
    }


def task_install_python():
    """
    """
    def update_env():
        module = importlib.import_module("install_python")
        path = f"{install_basedir}/Builds/{module.name}-{module.version}"
        add_to_env("LD_LIBRARY_PATH", f"{path}/lib")
        add_to_env("PATH", f"{path}/bin")
        pass
    return {'actions': [(
        clushUtils.exec_script,
        [targetNode, "install_python.py"],
        {
            'dependsFiles': [],
            'user':"adming",
            'manageEnv': True,
            'dependsPkgs':[],
            'logOutput': 'install_python.log'
        }
    ),
        (update_env)
    ],
        'targets': [f'{logDir}/install_python.log.{targetNode}'],
        'file_dep': ["deployConfig.py"],
    }


def task_install_pypkgs():
    """
    """

    return {'actions': [(
        clushUtils.exec_script,
        [targetNode, "install_pypkgs.py"],
        {
            'dependsFiles': [],
            'user':"adming",
            'manageEnv': True,
            'dependsPkgs':["rust"],
            'logOutput': 'install_pypkgs.log'
        }
    )

    ],
        'targets': [f'{logDir}/install_pypkgs.log.{targetNode}'],
        'file_dep': ["deployConfig.py"],
    }


def task_install_nginx():
    """
    """
    def update_env():
        module = importlib.import_module("install_nginx")
        path = f"{install_basedir}/Builds/{module.name}-{module.version}"
        add_to_env("LD_LIBRARY_PATH", f"{path}/lib")
        add_to_env("PATH", f"{path}/bin")
        pass
    return {'actions': [(
        clushUtils.exec_script,
        [targetNode, "install_nginx.py"],
        {
            'dependsFiles': [],
            'user':"adming",
            'manageEnv': True,
            'dependsPkgs':["pcre", "certbot", "py3-cffi", "py3-cryptography"],
            'logOutput': 'install_nginx.log'
        }
    ),
        (update_env)
    ],
        'targets': [f'{logDir}/install_nginx.log.{targetNode}'],
        'file_dep': ["deployConfig.py"],
    }


def task_deploy_nginx():
    return {'actions': [(
        clushUtils.exec_script,
        [targetNode, "deploy_nginx.py"],
        {
            'dependsFiles': ["nginx.conf"],
            'user':"adming",
            'manageEnv': True,
            'dependsPkgs':[],
            'logOutput': 'deploy_nginx.log'
        }
    )
    ],
        'targets': [f'{logDir}/deploy_nginx.log.{targetNode}'],
        'file_dep': ["deployConfig.py"],
    }


def task_install_nginx_unit():
    return {'actions': [(
        clushUtils.exec_script,
        [targetNode, "install_nginx_unit.py"],
        {
            'dependsFiles': [],
            'user':"adming",
            'manageEnv': True,
            'dependsPkgs':[],
            'logOutput': 'install_nginx_unit.log'
        }
    )
    ],
        'targets': [f'{logDir}/install_nginx_unit.log.{targetNode}'],
        'file_dep': ["deployConfig.py"],
    }


def task_deploy_nginx_unit():
    return {'actions': [(
        clushUtils.exec_script,
        [targetNode, "deploy_nginx_unit.py"],
        {
            'dependsFiles': [],
            'user':"adming",
            'manageEnv': True,
            'dependsPkgs':[],
            'logOutput': 'deploy_nginx_unit.log'
        }
    )
    ],
        'targets': [f'{logDir}/deploy_nginx_unit.log.{targetNode}'],
        'file_dep': ["deployConfig.py"],
    }


def task_hostsite_nginxunit():
    def pre_action():
        add_to_env("maintainer_email", maintainer_email)

    return {'actions': [(pre_action), (
        clushUtils.exec_script,
        [targetNode, "hostsite_nginx.py"],
        {
            'dependsFiles': ["sites.txt", "versaanalytics.tech.tgz", "build_venv.sh", "run_certbot.sh"],
            'user':"adming",
            'manageEnv': True,
            'dependsPkgs':[],
            'logOutput': 'hostsite_nginxunit.log'
        }
    )
    ],
        'targets': [f'{logDir}/hostsite_nginx_unit.log.{targetNode}'],
        'file_dep': ["deployConfig.py"],
    }

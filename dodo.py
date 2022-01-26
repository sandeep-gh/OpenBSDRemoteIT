import os
import clushUtils
from deployConfig import targetNode, logDir

from pathlib import Path
homeDir = str(Path.home())


def task_bootstrap_for_adming():
    """
    """
    return {'actions': [(clushUtils.exec_script, [targetNode, "bootstrap_for_adming.py"],
                         {
                             'dependsFiles': [".passwords", f"{homeDir}/.ssh/id_rsa.pub"],
                             'user':"root",
                             'manageEnv': False,
                             'dependsPkgs':['py3-pip', 'py3-psutil'],
                             'logOutput': 'bootstrap_for_adming.log'
    }
    )
    ],
        'targets': [f'{logDir}/bootstrap_for_adming.log.{targetNode}'],
    }

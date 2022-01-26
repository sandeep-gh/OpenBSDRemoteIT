import os

scriptsDir = os.path.dirname(os.path.realpath(__file__))
targetNode = os.environ['targetNode']
workDir = os.environ['workDir']
if 'logDir' in os.environ:
    logDir = os.environ['logDir']
else:
    logDir = f"{workDir}/logs"

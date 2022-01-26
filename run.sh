#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export targetNode=$1
export workDir=`pwd`
mkdir -p logs
doit -f ${SCRIPT_DIR}/dodo.py

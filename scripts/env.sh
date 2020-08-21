# This file should be sourced, not executed
if [ "${BASH_SOURCE[0]}" -ef "$0" ]; then
    echo "Source this script to activate virtual environment; do not execute directly!"
    echo "E.g. \`source $0\`"
    exit 1
fi

source scripts/config.sh

if [ ! -d ${VENV_PATH} ]; then
    echo >&2 "Failed to find virtual environment '${VENV_PATH}'; run initial setup first!"
    return 1
fi

source ${VENV_PATH}/bin/activate

echo "Activated virtual environment"

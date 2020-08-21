#!/usr/bin/env bash
source scripts/config.sh

############################
# Create Virtual Environment
############################
echo "Creating virtual environment; please wait"
echo "This may take up to 10 minutes."
if [ -x "$(command -v pv)" ]; then
    # Include a timer if we have pv
    python3 -m venv ${VENV_PATH} | pv -t
else
    python3 -m venv ${VENV_PATH}
fi
echo "Successfully created virtual environment"

######################
# Activate Environment
######################
source ${ACTIVATE_ENV_PATH}

####################
# Update Environment
####################
echo "Updating pip"
pip install --upgrade pip
echo "Updating setuptools"
pip install --upgrade setuptools
echo "Installing packages"
pip install -r requirements.txt

#########
# Cleanup
#########
echo "Setup complete!"

set -euo pipefail

MODULE_NAME=$1

echo "Ensuring pip is up to date"
python -m pip install --upgrade pip
echo "Installing the latest setuptools & wheel"
pip install --upgrade setuptools wheel

echo "--------------"
echo "Building wheel"
python setup.py bdist_wheel

APP_DIR=$(pwd)

# move into root dir so Python will import the installed package instead of the local source files
cd /
echo "------------------"
echo "Installing package"
pip install ${APP_DIR}/dist/*.whl

echo "-----------------------------"
echo "Attempting to import package"
python "${GITHUB_ACTION_PATH}/test_module_import.py" "${MODULE_NAME}"

set -euo pipefail

echo "Ensuring pip is up to date"
python -m pip install --upgrade pip==24.2
echo "Installing the latest version of pypa/build"
pip install build==1.2.1

python -m build --outdir dist/ .

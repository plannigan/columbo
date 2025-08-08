set -euo pipefail

echo "Ensuring pip is up to date"
python -m pip install --upgrade pip==25.2
echo "Installing the latest version of pypa/build"
pip install build==1.3.0

python -m build --outdir dist/ .

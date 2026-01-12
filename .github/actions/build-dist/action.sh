set -euo pipefail

echo "Ensuring pip is up to date"
python -m pip install --upgrade pip==25.3
echo "Installing the latest version of pypa/build"
pip install build==1.4.0

python -m build --outdir dist/ .

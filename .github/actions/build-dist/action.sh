set -euo pipefail

echo "Ensuring pip is up to date"
python -m pip install --upgrade pip==23.3.2
echo "Installing the latest version of pypa/build"
pip install build==1.0.3

python -m build --outdir dist/ .

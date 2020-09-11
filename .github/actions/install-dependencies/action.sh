set -euo pipefail

echo "Ensuring pip is up to date"
python -m pip install --upgrade pip

if [[ "${INPUT_REQUIREMENTS:-}" == "true"  ]]; then
  echo "Installing code requirements"
  pip install -r requirements.txt
fi

if [[ "${INPUT_TEST_REQUIREMENTS:-}" == "true"  ]]; then
  echo "Installing test requirements"
  pip install -r requirements-test.txt
fi

#!/usr/bin/env bash

set -eo pipefail

NEW_IS_DEV="false"
OLD_IS_DEV="false"

function usage() {
  echo "usage: update_docs_for_version.sh OLD_VERSION NEW_VERSION"
  echo ""
  echo " OLD_VERSION : Version being updated from"
  echo " NEW_VERSION : Version being updated to"
  exit 1
}

function is_dev() {
  [[ "${1}" =~ .+-dev$ ]]
}

if [[ $# != 2 ]]; then
  usage
fi

OLD_VERSION="${1}"
NEW_VERSION="${2}"

if is_dev "${OLD_VERSION}"; then
  OLD_IS_DEV="true"
fi
if is_dev "${NEW_VERSION}"; then
  NEW_IS_DEV="true"
fi

if [[ "${NEW_IS_DEV}" == "true" ]]; then
  mike deploy dev
else
  if [[ "${OLD_IS_DEV}" != "true" ]]; then
    mike retitle --message "Remove latest from title of ${OLD_VERSION}" "${OLD_VERSION}" "${OLD_VERSION}"
  fi
  mike deploy --update-aliases --title "${NEW_VERSION} (latest)" "${NEW_VERSION}" "latest"
fi

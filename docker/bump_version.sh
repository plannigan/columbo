#!/usr/bin/env bash

set -eo pipefail

DEFAULT_BRANCH="main"

function usage() {
  echo "usage: bump_version.sh major|minor|patch"
  echo ""
  echo " major|minor|patch : Part of version string to updated."
  exit 1
}

if [[ $# != 1 || ! "${1}" =~ major|minor|patch ]]; then
  usage
else
  PART="${1}"
fi

CURRENT_BRANCH=$(git branch --show-current)
CURRENT_STATUS=$(git status --short --untracked-files=no)

if [[ "${CURRENT_BRANCH}" != "${DEFAULT_BRANCH}" ]]; then
  echo "A version bump must be run from the default branch."
  echo "Run 'git switch ${DEFAULT_BRANCH}'"
  exit 2
elif [[ "$CURRENT_STATUS" != "" ]]; then
  echo "The working tree has uncommitted changes."
  echo "Commit or stash the changes before running a version bump."
  exit 3
fi
# Ensure on default branch
git switch --no-guess main
# Capture value of new version
NEW_VERSION=$(bump2version --dry-run --list "${PART}" | grep new_version | sed -r s,"^.*=",,)
# Create bump branch
BUMP_BRANCH_NAME="bump_version_to_${NEW_VERSION}"
git switch -c "${BUMP_BRANCH_NAME}"
# Update files
bump2version "${PART}"

# Updating the changelog has to be done manually
#   - bump2version doesn't support inserting dates https://github.com/c4urself/bump2version/issues/133
#   - It is not possible to have a multiline string in an INI file where a line after the first line starts with '#'.
#     The config parser reads it as a comment line.
TODAY=$(date +%Y-%m-%d)
sed -i "s/## \[Unreleased\]/## \[Unreleased\]\n\n## \[${NEW_VERSION}\] - ${TODAY}/g" CHANGELOG.md

# Add changelog to bump commit
git add CHANGELOG.md
git commit --amend --no-edit
# Show effected files
git show --pretty="" --name-only

echo "Run 'git push --set-upstream origin ${BUMP_BRANCH_NAME}' to "

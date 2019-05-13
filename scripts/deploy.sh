read -e -p "Bump Version (major/minor/patch): " -i "patch" BUMPVERRSION
rm -rf dist/
bumpversion $BUMPVERRSION
export CURRENT_BRANCH
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
git push --tags
git push origin "$CURRENT_BRANCH:$CURRENT_BRANCH"
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*

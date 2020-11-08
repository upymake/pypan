#!/usr/bin/env bash

PACKAGE_NAME="pypans"


setup() {
:<<DOC
  Installs a package
DOC
  python setup.py install
}


test-package() {
:<<DOC
  Test a package
DOC
  pip list | grep ${PACKAGE_NAME}
}


cleanup() {
:<<DOC
  Clean up a package
DOC
  rm -rf ${PACKAGE_NAME}.egg-info dist build
  pip uninstall -y ${PACKAGE_NAME}
}


run-test-suite() {
:<<DOC
  Test entrypoint
DOC
  setup && test-package && cleanup
}


run-test-suite

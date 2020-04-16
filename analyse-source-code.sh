#!/usr/bin/env bash

PACKAGE="pypans"


pretty-printer-box() {
:<<DOC
    Provides pretty-printer check box
DOC
    echo "Start ${1} analysis ..."
}


remove-pycache() {
:<<DOC
    Removes python cache directories
DOC
    ( find . -depth -name __pycache__ | xargs rm -r )
}


check-black() {
:<<DOC
    Runs "black" code analyser
DOC
    pretty-printer-box "black" && ( black --check ${PACKAGE} )
}


check-flake() {
:<<DOC
    Runs "flake8" code analysers
DOC
    pretty-printer-box "flake" && ( flake8 ./ )
}


check-pylint() {
:<<DOC
    Runs "pylint" code analyser
DOC
    pretty-printer-box "pylint" && ( find ${PACKAGE} -type f -name "*.py" | xargs pylint )
}


check-mypy() {
:<<DOC
    Runs "mypy" code analyser
DOC
    pretty-printer-box "mypy" && ( mypy --package "${PACKAGE}" )
}


check-docstrings() {
:<<DOC
     Runs "pydocstyle" static documentation code style formatter
DOC
    pretty-printer-box "pydocstyle" && ( pydocstyle --explain --count ${PACKAGE} )
}


check-unittests() {
:<<DOC
    Runs unittests using "pytest" framework
DOC
    pretty-printer-box "unitests" && pytest
}


check-pymanifest() {
:<<DOC
    Runs unittests using "check-manifest" tool
DOC
    pretty-printer-box "check-manifest" && check-manifest -v ./
}


main() {
:<<DOC
    Runs "main" code analyser
DOC
    (
      remove-pycache
      check-black && \
      check-mypy && \
      check-pylint && \
      check-flake && \
      check-docstrings && \
      check-pymanifest && \
      check-unittests
    )
}


main
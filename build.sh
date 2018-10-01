#!/bin/sh

AGENT=ia-agent

cd agent
pyinstaller --clean -F --additional-hooks-dir=. -n=${AGENT} --distpath=.. main.py
rm ${AGENT}.spec

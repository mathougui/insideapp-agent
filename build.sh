#!/bin/sh

AGENT=ia-agent

rm ia-agent
rm -r agent/build
cd agent
pyinstaller --clean -F --additional-hooks-dir=. -n=${AGENT} --distpath=.. main.py
rm ${AGENT}.spec

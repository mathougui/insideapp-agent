#!/bin/sh

AGENT=ia-agent

cd agent
pyinstaller -F --additional-hooks-dir=. -n=${AGENT} --distpath=.. main.py
rm ${AGENT}.spec
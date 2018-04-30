#!/bin/sh

AGENT=ia-agent

cd agent
zip -r ../agent.zip *
cd ..
echo '#!/usr/bin/env python' | cat - agent.zip > $AGENT
rm agent.zip
chmod +x $AGENT

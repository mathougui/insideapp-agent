#!/bin/sh

# Need AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY to be set

pip install --user awscli pyinstaller
./build.sh
aws s3 cp ia-agent s3://insideapp/ia-agent --endpoint-url=http://s3.insideapp.io

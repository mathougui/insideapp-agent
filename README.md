# insideapp-agent
Agent for insideapp

### Environment variables
* `API_URL` (`https://metrics.insideapp.io` by default)
* `ADMIN_URL` (`http://insideapp.io` by default)

### Generate executable
`./build.sh`

### Launch the agent
To launch the agent, you must use the `start` command: `sudo ia-agent start --api_key xxxxxxxxxxxxxxxxxxxxxxxxx`

### Daemon
To launch the agent in daemon mode, you must specify the `daemon start` command: `sudo ia-agent daemon start --api_key xxxxxxxxxxxxxxxxxxxxxxxxx`  
To stop the daemon, you must use the `daemon stop` command:  `ia-agent daemon stop`  

### Options  
* `--api_key` to specify the api key
* `-n, --name <process_name>` to specify the process name
* `-p, --pid <process_id>` to specify the process PID
* `-v, --verbose` to print debug statements

The only mandatory argument when using the `start` or `daemon start` command is `--api_key`.  
If you do not specify a process with either the `-n` or `-p` options, then the agent will only send the global metrics not related to any process, e.g. the global CPU percentage usage.

### Log file
The log file is situated at '/var/log/insideapp/insideapp-agent.log'

### Config file
To specify log files, you need to create a yaml file.
By default, the agent will look for '/etc/insideapp.yml'
You can change this path by setting the env variable `INSIDEAPP_CONFIG`
The file should look like this:

```
nginx: /var/log/nginx/error.log.4
nginx2: /var/log/nginx/error.log
```
### Troubleshoot
```
Fatal Python error: initfsencoding: unable to load the file system codec
zipimport.ZipImportError: can't find module 'encodings'
```
This error appears because you tried to build the agent using python 3.7.
You must build it using python 3.6.  
To create a virtualenv using python 3.6, use `virtualenv venv --python=/bin/python3.6`
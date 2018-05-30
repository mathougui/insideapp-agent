# insideapp-agent
Agent for insideapp

### Environment variables
* `API_URL` (`http://insideapp.io:5000` by default)
* `ADMIN_URL` (`http://insideapp.io` by default)

### Generate executable
`cd agent`
`python setup.py build`
This will create a directory in agent/build containing the executable, the lib directory and the config.json file

### Config file
To specify log files, you need to create a yaml file.
By default, the agent will look for '/etc/insideapp.yml'
You can change this path by setting the env variable `INSIDEAPP_CONFIG`
The file should look like this:

```
nginx: /var/log/nginx/error.log.4
nginx2: /var/log/nginx/error.log
```

Options:
`-n, --name <process_name>`  
`-p, --pid <process_id>   
`-v, --verbose

The agent will automatically create a daemon if not launched with the verbose mode  
To stop this daemon, run `python __main__.py stop`

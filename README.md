# insideapp-agent
Agent for insideapp

### Environment variables
* `API_URL` (`https://metrics.insideapp.io` by default)
* `ADMIN_URL` (`http://insideapp.io` by default)

### Generate executable

`./build.sh`

Options:
`--api_key` to specify the api key
`-n, --name <process_name>` to specify the process name
`-p, --pid <process_id>` to specify the process PID
`-v, --verbose` to print debug statements
`--start` to start the agent in daemon mode
`--stop` to stop the agent if it was launched in daemon mode

### Config file
To specify log files, you need to create a yaml file.
By default, the agent will look for '/etc/insideapp.yml'
You can change this path by setting the env variable `INSIDEAPP_CONFIG`
The file should look like this:

```
nginx: /var/log/nginx/error.log.4
nginx2: /var/log/nginx/error.log
```

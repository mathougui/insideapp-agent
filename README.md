# insideapp-agent
Agent for insideapp

### Environment variables
* `API_URL` (`http://localhost:5000` by default)  
* `ADMIN_URL` (`http://localhost:3000` by default)  

### Generate executable
`cd agent`  
`zip -r ../agent.zip` *  
`cd ..`  
`echo '#!/usr/bin/env python' | cat - agent.zip > agent-bin`  
`chmod +x agent-bin`  

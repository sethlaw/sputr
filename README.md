Security Payload Unit Test Repository (SPUTR)
---
A repository of payloads for security unit/integration testing.

Quickstart
--
1- sputr.py -h

Layout
--
* /
* sputr.py           # Go here for everything
* ../payloads/       # Different payload sets
* ../exploit_chars/  # Used by generate_payloads, interesting characters by vulnerability
* ../libs/           # language/framework libraries for including in unit tests.


config.json
---
To generate and start tests, need to build a config.json file. There are a few required json parameters if you building it by hand.

Required Configuration Details
---
The following example configuration tests one endpoint for XSS, each of the the main json objects are required by SPUTR (token, creds, csrf, domain, endpoints).

```
{
        "token":{
                        "name":"session_cookie", "value":""
        },
        "creds":{
                        "username":{ "name":"username", "value":"seth" },
                        "password":{ "name":"password", "password":"soccerlover" }
        },
        "csrf":{
                "pattern":"\\w{32}",
                "name":"csrfmiddlewaretoken",
                "login_url":"http://localhost:8000/taskManager/login/",
                "auth_url":"http://localhost:8000/taskManager/project_list/"
        },
        "domain":{
                        "host":"localhost:8000",
                        "protocol":"http://",
                        "login_url":"http://localhost:8000/taskManager/login/",
                        "auth_url":"http://localhost:8000/taskManager/project_list/"
        },
        "endpoints":[
                        { "path":"/taskManager/search/",
                	  "method":"GET",
                          "auth":1,
                          "params":{ "q":"item" },
                          "tests":"01000" }
        ]
}
```

JSON Objects
---
* token: session token that must be tracked for authentication
* creds: credentials for accessing the application during testing
* csrf: csrf token to track for requests
* domain: application connection information, including login_url for authenticaiton and auth_url for authentication test
* endpoints: each of the different locations and tests to run
* tests: inside endpoints, determines what tests to run on each endpoint (currently 5)
** 10000 == SQL Injection (SQLi)
** 01000 == Cross-Site Scripting (XSS)
** 00100 == Insecure Direct Object Reference (IDOR)
** 00010 == Cross-Site Request Forgery (CSRF)
** 00001 == Missing Function Level Access Control (MFLAC)

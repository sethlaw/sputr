{
	"creds":{
			"username":{
				"name":"username",
				"value":"user"
			},
			"password":{
				"name":"password",
				"password":"user123"
			}
	},
	"csrf":{
		"pattern":"\\w{32}",
		"name":"_csrf",
		"login_url":"http://localhost:8085/login",
		"auth_url":"http://localhost:8085/dashboard"
	},
	"domain":{
			"host":"localhost:8085",
			"protocol":"http://",
			"login_url":"http://localhost:8085/login",
			"auth_url":"http://localhost:8085/dashboard"
	},
	"endpoints":[
			{ "path":"/login",
			  "method":"POST",
			  "auth":0,
			  "params":{
				"username":"u",
				"password":"p"
			  },
			  "tests":"11001"
			},
			{ "path":"/event/search",
			  "method":"GET",
			  "auth":1,
			  "params":{"q":"a"},
			  "tests":"11001"
			},
			{ "path":"/payment/make-payment",
			  "method":"GET",
			  "auth":1,
			  "params":{"event":"5"},
			  "tests":"11001"
			},
			{ "path":"/payment/list-sent/3",
			  "method":"POST",
			  "auth":1,
			  "params":{"event":"5",
				    "amount":"0.01"
				   },
			  "tests":"11001"
			},
			{ "path":"/dashboard/",
			  "method":"GET",
			  "auth":1,
			  "params":{ },
			  "tests":"00001"
			}
	]
}

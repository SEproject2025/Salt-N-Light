# frontend

## Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Lints and fixes files

```
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

## Endpoint Documentation

#### Preface

- if you have not installed axios, use the `npm install axios` command to install it
- when using axios calls, inside your scripts use `from axios import "axios";` to be able to use it
- to make the actual call, use `axios.WhateverMethod(URL of target)`
  - for example, in my components folder in frontend, inside ChurchRegister.vue you can see where I import axios inside the script part and how I use it to make a call to my endpoint
- **Make sure to run both servers on different terminals**

### Account Creation Endpoint

1. Mock endpoint for account creation, this endpoint does not return anything except for an "OK"
2. should be able to send this endpoint anything (not 100% sure about this, haven't fully tested it)
3. this endpoint is specified as 'POST', so expect to be inputting information when making calls to this endpoint
4. once you have completed installing axios, you can make calls to this endpoint using `await axios.post("http://127.0.0.1:8000/createaccount/"`
5. again, expect to get nothing back as this endpoint does not do anything except take in whatever you send it and give back a 200 'OK'

### Login Page Endpoint

1. Mock endpoint for the user login page, this endpoint does not return anything except for an "OK"
2. should be able to send this endpoint anything (not 100% sure about this, haven't fully tested it)
3. this endpoint is specified as 'POST' and 'GET', so expect to be inputting information when making calls to this endpoint and getting information back based on your specifications on what you need back
4. once you have completed installing axios, you can make calls to this endpoint using `await axios.post("http://127.0.0.1:8000/userlogin/"` or `await axios.get("http://127.0.0.1:8000/userlogin/"`
5. again, expect to get nothing back as this endpoint does not do anything except take in whatever you send it and give back a 200 'OK'

### Profile Page Endpoint

1. Mock endpoint for the user profile page, this endpoint does not return anything except for an "OK"
2. should be able to send this endpoint anything (not 100% sure about this, haven't fully tested it)
3. this endpoint is specified as 'POST', 'GET', and 'PUT', so expect to be inputting information when making calls to this endpoint and getting information back based on your specifications on what you need back
4. once you have completed installing axios, you can make calls to this endpoint using `await axios.post("http://127.0.0.1:8000/userprofile/"` or `await axios.get("http://127.0.0.1:8000/userprofile/"` or `await axios.put("http://127.0.0.1:8000/userprofile/"`
5. again, expect to get nothing back as this endpoint does not do anything except take in whatever you send it and give back a 200 'OK'

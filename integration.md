# Chunk 3: Front End / Back End Integration & Smoke Testing
Time to link the front end to the back end and add a hit counter to the web page.
## Step 7 - Javascript to call the API
I used the Javascript fetch() to call the back-end.
```javascript
const myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

const raw = JSON.stringify({
    "counter": "cloud-resume"
});

const requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};

const span = document.getElementById('counter');

fetch("https://vverqscq65.execute-api.us-east-1.amazonaws.com/PROD", requestOptions)
    .then(response => response.text())
    .then(result => span.innerText = result)
    .catch(error => console.log('error', error));
```

This worked fantastically from Postman, however using from a browser resulted in a [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) issue.

To resolve this, I had to enable CORS on the [API](api.md).
## Step 11 - Smoke Testing with Cypress

### PAGE 102

## Wrap Up
So that's the Front end, API, database, Lambda function all working in AWS, 
however only the Front-end stuff has any CloudFormation currently.  All the back-end
was set up in my Development account using the console, so at some point I will need
to revisit the [API setup](api.md) and this Integration setup and get it all working
from CloudFormation templates.


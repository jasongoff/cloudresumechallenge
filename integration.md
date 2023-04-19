# Chunk 3: Front End / Back End Integration
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

### PAGE 99

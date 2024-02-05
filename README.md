**WIP!

First, generate the client library. Ensure that your FastAPI server is running so you can grab the schema:

``` bash
openapi-generator-cli generate -g python -i http://localhost:8000/openapi.json -o ./client
```

Next, you can run main.py which can route any function call to the correct API destination.

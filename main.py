import openapi_client

class SimplifiedClient:
    def __init__(self, host="http://localhost:8000"):
        self.configuration = openapi_client.Configuration(host=host)
        self.api_client = openapi_client.ApiClient(self.configuration)
        self._apis = self._discover_apis()

    def _discover_apis(self):
        """
        Dynamically discovers all API classes from the openapi_client module and initializes them.
        """
        apis = {}
        for attr_name in dir(openapi_client):
            # Check if the attribute name ends with 'Api', indicating an API class
            if attr_name.endswith('Api'):
                attr = getattr(openapi_client, attr_name)
                # Initialize the API class and store it
                apis[attr_name.lower()] = attr(self.api_client)
        return apis

    def __getattr__(self, name):
        # Dynamically find and return the method from the appropriate API class
        for api in self._apis.values():
            if hasattr(api, name):
                def method(*args, **kwargs):
                    return getattr(api, name)(*args, **kwargs)
                return method
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def route_function(self, function_name, *args, **kwargs):
        """
        Routes a function call to the appropriate API method based on the function name.
        """
        for api in self._apis.values():
            if hasattr(api, function_name):
                method = getattr(api, function_name)
                return method(*args, **kwargs)
        raise AttributeError(f"No such method '{function_name}' found in any API class.")
    
client = SimplifiedClient(host="http://localhost:8000")


# Example usage
response = client.route_function("create_project_anon", project_name="lucas")
print(response)
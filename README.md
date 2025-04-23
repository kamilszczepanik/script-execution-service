# Safe Python Script Execution Service

A Flask-based API service to execute arbitrary Python scripts safely using nsjail.

## Local Development

1.  **Build the Docker image:**
    ```bash
    docker build -t safe-script-runner .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 8080:8080 safe-script-runner
    ```
****
3.  **Send a request (example):**
    ```bash
    curl -X POST -H "Content-Type: application/json" \
         -d '{"script": "def main():\n    return {\"message\": \"Hello from script!\"}"}' \
         http://localhost:8080/execute
    ```

## Cloud Run Deployment

*(Instructions to be added later)*

## TODO

- Implement actual script execution using nsjail.
- Configure nsjail for security.
- Handle script output (stdout, return value).
- Add pandas/numpy dependencies.
- Deploy to Cloud Run.
- Add Cloud Run URL and updated curl command here. 
# Safe Python Script Execution Service

A secure microservice for executing Python scripts in an isolated environment.

## Development

  **Build & run the Docker image (local mode):**
    ```bash
    docker compose up --build 
    ```

## Deployment

1. **Install Google Cloud SDK** (if you don't have it already):
   ```bash
   curl https://sdk.cloud.google.com | bash
   gcloud init
   ```

2. **Build and deploy to Cloud Run**:
   ```bash
   # Set your Google Cloud project ID
   export PROJECT_ID=$(gcloud config get-value project)
   
   # Build and push the container
   gcloud builds submit --tag gcr.io/$PROJECT_ID/script-execution-service
   
   # Deploy to Cloud Run
   gcloud run deploy script-execution-service \
     --image gcr.io/$PROJECT_ID/script-execution-service \
     --platform managed \
     --allow-unauthenticated \
     --region us-central1 \
     --memory 512Mi
   ```

### Security Considerations

- The service is configured to allow unauthenticated access. For production, consider adding authentication.
  
## API Usage

### Live Service

The service is deployed at: https://script-execution-service-94204096560.us-west2.run.app/

You can test it using the following curl commands:

1. **Basic test (hello world):**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    return {\"message\": \"Hello from Cloud Run!\"}"}' \
        https://script-execution-service-94204096560.us-west2.run.app/execute
   ```

2. **Using numpy for calculations:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    import numpy as np\n    data = np.array([1, 2, 3, 4, 5])\n    return {\"mean\": float(np.mean(data)), \"sum\": int(np.sum(data)), \"std\": float(np.std(data))}"}' \
        https://script-execution-service-94204096560.us-west2.run.app/execute
   ```

3. **Working with pandas dataframes:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    import pandas as pd\n    df = pd.DataFrame({\"A\": [1, 2, 3], \"B\": [4, 5, 6]})\n    return {\"description\": df.describe().to_dict(), \"column_sum\": df.sum().to_dict()}"}' \
        https://script-execution-service-94204096560.us-west2.run.app/execute
   ```

4. **Using stdout and returning results:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    print(\"Processing data...\")\n    data = [1, 2, 3, 4, 5]\n    print(f\"Sum: {sum(data)}\")\n    return {\"result\": sum(data), \"length\": len(data)}"}' \
        https://script-execution-service-94204096560.us-west2.run.app/execute
   ```

5. **Error handling example:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    try:\n        x = 1 / 0\n    except Exception as e:\n        print(f\"Caught error: {e}\")\n        return {\"error_handled\": str(e)}\n    return {\"result\": \"This will not execute\"}"}' \
        https://script-execution-service-94204096560.us-west2.run.app/execute
   ```

### Locally

#### Successful Cases

1. **Basic script execution:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    return {\"message\": \"Hello from script!\"}"}' \
        http://localhost:8080/execute
   ```

2. **Using stdout:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    print(\"Output to stdout\")\n    return {\"message\": \"Hello from script!\"}"}' \
        http://localhost:8080/execute
   ```

3. **Using numpy library:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    import numpy as np\n    arr = np.array([1, 2, 3])\n    return {\"sum\": int(np.sum(arr)), \"mean\": float(np.mean(arr))}"}' \
        http://localhost:8080/execute
   ```

4. **Using pandas library:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    import pandas as pd\n    df = pd.DataFrame({\"A\": [1, 2, 3], \"B\": [4, 5, 6]})\n    return {\"columns\": list(df.columns), \"shape\": list(df.shape)}"}' \
        http://localhost:8080/execute
   ```

5. **Using os library:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    import os\n    return {\"current_dir\": os.getcwd(), \"env_vars\": list(os.environ.keys())[:5]}"}' \
        http://localhost:8080/execute
   ```

#### Error Cases

1. **Missing main function:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "print(\"This script has no main function\")"}' \
        http://localhost:8080/execute
   ```

2. **Syntax error:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main() \n    return {\"message\": \"Missing colon after function definition\"}"}' \
        http://localhost:8080/execute
   ```

3. **Non-JSON-serializable return value:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    class CustomClass:\n        pass\n    return CustomClass()"}' \
        http://localhost:8080/execute
   ```

4. **Runtime error:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    1/0\n    return {\"message\": \"This won't execute\"}"}' \
        http://localhost:8080/execute
   ```

5. **Invalid JSON in request:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{script: "def main(): return {}"' \
        http://localhost:8080/execute
   ```
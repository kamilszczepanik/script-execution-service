# Safe Python Script Execution Service

A secure microservice for executing Python scripts in an isolated environment.

## Local development

  **Build & run the Docker image (local mode):**
    ```bash
    docker compose up --build 
    ```
    
## API Usage

### Live Service

The service is deployed at: https://script-execution-service-94204096560.us-west2.run.app/

You can test it using the following curl commands:

1. **Using stdout and returning results:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    print(\"Processing data...\")\n    data = [1, 2, 3, 4, 5]\n    print(f\"Sum: {sum(data)}\")\n    return {\"result\": sum(data), \"length\": len(data)}"}' \
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

### Local Service

#### Successful Cases

1. **Basic script execution with stdout:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    print(\"Output to stdout\")\n    return {\"message\": \"Hello from script!\"}"}' \
        http://localhost:8080/execute
   ```


2. **Using numpy library:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    import numpy as np\n    arr = np.array([1, 2, 3])\n    return {\"sum\": int(np.sum(arr)), \"mean\": float(np.mean(arr))}"}' \
        http://localhost:8080/execute
   ```

3. **Using pandas library:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    import pandas as pd\n    df = pd.DataFrame({\"A\": [1, 2, 3], \"B\": [4, 5, 6]})\n    return {\"columns\": list(df.columns), \"shape\": list(df.shape)}"}' \
        http://localhost:8080/execute
   ```

#### Error Cases

1. **Missing main function:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "print(\"This script has no main function\")"}' \
        http://localhost:8080/execute
   ```


2. **Non-JSON-serializable return value:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    class CustomClass:\n        pass\n    return CustomClass()"}' \
        http://localhost:8080/execute
   ```

3. **Runtime error:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"script": "def main():\n    1/0\n    return {\"message\": \"This won't execute\"}"}' \
        http://localhost:8080/execute
   ```

4. **Invalid JSON in request:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{script: "def main(): return {}"' \
        http://localhost:8080/execute
   ```

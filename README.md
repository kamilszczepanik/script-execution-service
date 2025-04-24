# Safe Python Script Execution Service

A Flask-based API service to execute arbitrary Python scripts safely using nsjail.

## Local Development

1.  **Build & run the Docker image:**
    ```bash
    docker build -t safe-script-runner . && docker run -p 8080:8080 safe-script-runner
    ```

    Or to run in detached mode:
    ```bash
    docker build -t safe-script-runner . && docker run -d -p 8080:8080 --name script-executor safe-script-runner
    ```


## Testing the Improvements

### Successful Cases

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

### Error Cases

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

## Cloud Run Deployment

*(Instructions to be added later)*

## TODO

- Implement actual script execution using nsjail.
- Configure nsjail for security.
- Handle script output (stdout, return value).
- Add pandas/numpy dependencies.
- Deploy to Cloud Run.
- Add Cloud Run URL and updated curl command here. 
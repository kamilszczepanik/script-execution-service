import json
import os
import subprocess
import tempfile

from flask import Flask, jsonify, request

app = Flask(__name__)

NSJAIL_PATH = "/usr/bin/nsjail"
PYTHON_PATH = "/usr/local/bin/python3"
NSJAIL_CONFIG_PATH = "/app/nsjail.config"
SCRIPTS_DIR = "/tmp/scripts"


def execute_script_in_jail(script):
    """Execute a Python script in an nsjail environment."""
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        suffix=".py", delete=False, dir=SCRIPTS_DIR
    ) as tmp:
        tmp_path = tmp.name
        wrapper_script = f"""
import io
import json
import sys
import os
import numpy as np
import pandas as pd
from contextlib import redirect_stdout

# The user script
{script}

if 'main' not in locals() and 'main' not in globals():
    error_msg = "Function 'main' is not defined in the script"
    print(json.dumps({{"error": error_msg}}))
    sys.exit(1)

# Execute the main function and capture stdout
stdout_capture = io.StringIO()
try:
    with redirect_stdout(stdout_capture):
        result = main()
    # Validate JSON serialization
    json.dumps(result)
    print(json.dumps({{"result": result, 
                     "stdout": stdout_capture.getvalue()}}))
    sys.exit(0)
except Exception as e:
    error_msg = str(e)
    print(json.dumps({{"error": error_msg, 
                     "stdout": stdout_capture.getvalue()}}))
    sys.exit(1)
"""
        tmp.write(wrapper_script.encode("utf-8"))

    try:
        cmd = [
            NSJAIL_PATH,
            "--config",
            NSJAIL_CONFIG_PATH,
            "--",
            PYTHON_PATH,
            tmp_path,
        ]

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
        )

        os.unlink(tmp_path)

        try:
            output = process.stdout.strip()
            if output:
                return json.loads(output)
            else:
                stderr = process.stderr.strip()
                return {"error": f"Script execution failed. Error: {stderr}"}
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse script output as JSON",
                "stdout": process.stdout,
                "stderr": process.stderr,
            }

    except subprocess.TimeoutExpired:
        os.unlink(tmp_path)
        return {"error": "Script execution timed out"}
    except Exception as e:
        os.unlink(tmp_path)
        return {"error": f"Error executing script: {str(e)}"}


@app.route("/execute", methods=["POST"])
def execute_script():
    """Execute a Python script in a sandboxed environment."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    script = data.get("script")

    if not script or not isinstance(script, str):
        err_msg = "Missing or invalid 'script' key in JSON body"
        return jsonify({"error": err_msg}), 400

    if "def main" not in script:
        return jsonify({"error": "Script must contain a 'main' function"}), 400

    result = execute_script_in_jail(script)

    if "error" in result:
        return jsonify({"error": result["error"]}), 400

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

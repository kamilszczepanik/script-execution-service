import io
import json
import sys
from contextlib import redirect_stdout

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/execute", methods=["POST"])
def execute_script():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    script = data.get("script")

    if not script or not isinstance(script, str):
        error_msg = "Missing or invalid 'script' key in JSON body"
        return jsonify({"error": error_msg}), 400

    # Create a new namespace for script execution
    namespace = {}

    # Capture stdout
    stdout_capture = io.StringIO()

    try:
        # Execute the script and capture stdout
        with redirect_stdout(stdout_capture):
            exec(script, namespace)

        # Check if main function exists
        if "main" not in namespace:
            return jsonify({"error": "Script must contain a main() function"}), 400

        # Execute main function and get its return value
        main_result = namespace["main"]()

        # Verify that the result is JSON serializable
        try:
            json.dumps(main_result)
        except (TypeError, ValueError):
            return jsonify(
                {"error": "main() function must return a JSON-serializable value"}
            ), 400

        return jsonify({"result": main_result, "stdout": stdout_capture.getvalue()})

    except Exception as e:
        return jsonify(
            {
                "error": f"Script execution failed: {str(e)}",
                "stdout": stdout_capture.getvalue(),
            }
        ), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

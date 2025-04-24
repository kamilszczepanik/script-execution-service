import io
import json
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
        return jsonify({"error": "Missing or invalid 'script' key in JSON body"}), 400

    stdout_capture = io.StringIO()
    namespace = {"__builtins__": __builtins__}

    try:
        compiled_code = compile(script, "<string>", "exec")

        with redirect_stdout(stdout_capture):
            exec(compiled_code, namespace)

        if "main" not in namespace or not callable(namespace["main"]):
            return jsonify({"error": "Script must contain a main() function"}), 400

        with redirect_stdout(stdout_capture):
            main_result = namespace["main"]()

        try:
            json.dumps(main_result)
        except (TypeError, ValueError):
            return jsonify(
                {
                    "error": "main() function must return a JSON-serializable value",
                    "stdout": stdout_capture.getvalue(),
                }
            ), 400

        return jsonify({"result": main_result, "stdout": stdout_capture.getvalue()})

    except SyntaxError as e:
        return jsonify(
            {"error": f"Syntax error: {str(e)}", "stdout": stdout_capture.getvalue()}
        ), 400
    except Exception as e:
        return jsonify(
            {
                "error": f"Script execution failed: {str(e)}",
                "stdout": stdout_capture.getvalue(),
            }
        ), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

#!/bin/bash

echo "Running security tests against the script execution service..."

echo -e "\n1. Attempting to read /etc/passwd file:"
curl -X POST -H "Content-Type: application/json" \
     -d '{"script": "def main():\n    try:\n        with open(\"/etc/passwd\", \"r\") as f:\n            data = f.read()\n            return {\"data\": data}\n    except Exception as e:\n        return {\"error\": str(e)}"}' \
     http://localhost:8080/execute

echo -e "\n\n2. Attempting to execute system command (ls -la):"
curl -X POST -H "Content-Type: application/json" \
     -d '{"script": "def main():\n    import subprocess\n    try:\n        output = subprocess.check_output([\"ls\", \"-la\"], text=True)\n        return {\"output\": output}\n    except Exception as e:\n        return {\"error\": str(e)}"}' \
     http://localhost:8080/execute

echo -e "\n\n3. Attempting to open a network connection:"
curl -X POST -H "Content-Type: application/json" \
     -d '{"script": "def main():\n    import socket\n    try:\n        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n        s.connect((\"google.com\", 80))\n        s.close()\n        return {\"result\": \"Connected to google.com:80\"}\n    except Exception as e:\n        return {\"error\": str(e)}"}' \
     http://localhost:8080/execute

echo -e "\n\n4. Attempting to write to a system directory:"
curl -X POST -H "Content-Type: application/json" \
     -d '{"script": "def main():\n    try:\n        with open(\"/etc/new_file.txt\", \"w\") as f:\n            f.write(\"This is a test\")\n        return {\"result\": \"File created successfully\"}\n    except Exception as e:\n        return {\"error\": str(e)}"}' \
     http://localhost:8080/execute

echo -e "\n\n5. Attempting to access system process information:"
curl -X POST -H "Content-Type: application/json" \
     -d '{"script": "def main():\n    import os\n    try:\n        os_info = {\n            \"pid\": os.getpid(),\n            \"parent_pid\": os.getppid(),\n            \"uid\": os.getuid(),\n            \"gid\": os.getgid(),\n            \"cwd\": os.getcwd(),\n        }\n        return os_info\n    except Exception as e:\n        return {\"error\": str(e)}"}' \
     http://localhost:8080/execute

echo -e "\n\nSecurity tests completed!" 
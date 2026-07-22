import os
import requests
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

# Target service base URLs
COURSE_SERVICE_URL = os.environ.get("COURSE_SERVICE_URL", "http://localhost:5001")
STUDENT_SERVICE_URL = os.environ.get("STUDENT_SERVICE_URL", "http://localhost:5002")

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    req_path = request.path
    
    # Route matching
    if req_path.startswith('/api/courses') or req_path.startswith('/api/departments'):
        target_url = f"{COURSE_SERVICE_URL}{req_path}"
    elif req_path.startswith('/api/students'):
        target_url = f"{STUDENT_SERVICE_URL}{req_path}"
    else:
        return jsonify({"error": "API Gateway: Route not found"}), 404

    # Append query string if present
    if request.query_string:
        target_url += f"?{request.query_string.decode('utf-8')}"

    try:
        # Forward request to target service
        response = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for key, value in request.headers if key.lower() != 'host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=10
        )

        # Re-construct response to return to client
        # Filter out hop-by-hop headers to prevent proxy issues
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [
            (name, value) for name, value in response.raw.headers.items()
            if name.lower() not in excluded_headers
        ]

        return Response(response.content, response.status_code, headers)

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "API Gateway: Target service is unreachable"}), 502
    except requests.exceptions.Timeout:
        return jsonify({"error": "API Gateway: Target service request timed out"}), 504
    except Exception as e:
        return jsonify({"error": f"API Gateway: Internal error: {str(e)}"}), 500

if __name__ == '__main__':
    # Gateway runs on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

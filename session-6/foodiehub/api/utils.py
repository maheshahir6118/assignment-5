from rest_framework.response import Response

def standardized_response(status_str="success", message="", data=None, http_status=200, headers=None):
    """
    Helper function to generate a standardized API response.
    Returns a JSON payload with standard schema:
    {
        "status": "success" or "error",
        "message": "User-facing descriptive message.",
        "data": JSON payload object or null
    }
    """
    payload = {
        "status": status_str,
        "message": message,
        "data": data
    }
    return Response(payload, status=http_status, headers=headers)

from rest_framework.views import exception_handler
from rest_framework import status
from .utils import standardized_response

def custom_exception_handler(exc, context):
    """
    Global exception handler that intercepts DRF errors and formats them into
    our standardized error schema.
    """
    # Call default handler to parse DRF exceptions
    response = exception_handler(exc, context)

    if response is not None:
        # For HTTP 400 Bad Request (typically validation errors)
        if response.status_code == 400:
            response.data = {
                "status": "error",
                "message": "Validation failed",
                "data": response.data
            }
        else:
            # Extract error details
            error_detail = response.data
            if isinstance(response.data, dict) and 'detail' in response.data:
                error_detail = response.data['detail']
                
            # Reformat response body
            response.data = {
                "status": "error",
                "message": str(error_detail),
                "data": None
            }
    else:
        # For unhandled server-side exceptions (database crash, syntax error, etc.)
        # Return a standardized 500 error response instead of HTML crash page
        return standardized_response(
            status_str="error",
            message=f"Internal Server Error: {str(exc)}",
            data=None,
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response

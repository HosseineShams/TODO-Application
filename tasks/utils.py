from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF to ensure consistent error responses.
    """
    # Let DRF handle the default exception response
    response = exception_handler(exc, context)

    # If a DRF-generated response exists, structure it
    if response is not None:
        logger.error(f"Error occurred: {exc} in {context['view']}")
        return Response({
            "error": {
                "message": response.data.get("detail", "An error occurred."),
                "status_code": response.status_code
            }
        }, status=response.status_code)

    # Handle non-DRF exceptions (like unhandled server errors)
    logger.critical(f"Unhandled exception: {exc}", exc_info=True)
    return Response({
        "error": {
            "message": "An unexpected error occurred. Please try again later.",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

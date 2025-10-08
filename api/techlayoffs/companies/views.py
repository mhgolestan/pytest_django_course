from django.core.mail import send_mail
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Company
from .serializers import CompanySerializer
from fibonacci.dynamic import fibonacci_dynamic
from typing import Union

DEFAULT_EMAIL_SENDER = "golestan1369@gmail.com"
DEFAULT_EMAIL_RECIPIENTS = ["golestan1369@gmail.com"]


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination


@api_view(http_method_names=["POST"])
def send_company_email(request: Request) -> Response:
    send_mail(
        subject=request.data.get("subject"),
        message=request.data.get("message"),
        from_email=DEFAULT_EMAIL_SENDER,
        recipient_list=DEFAULT_EMAIL_RECIPIENTS,
    )
    return Response(
        {"status": "success", "info": "email sent successfully"}, status=200
    )


def _get_validated_fibonacci_n(request: Request) -> Union[tuple[int, None], tuple[None, Response]]:
    """
    Parses and validates the 'n' query parameter for the Fibonacci view.

    Returns:
        A tuple: (n_int, None) if valid, or (None, Response) if an error occurred.
    """
    n_str = request.query_params.get("n")

    if n_str is None:
        return None, Response({"error": "Query parameter 'n' is required."}, status=400)

    try:
        n_int = int(n_str)
        if n_int < 0:
            return None, Response(
                {"error": "Fibonacci sequence is not defined for negative numbers"},
                status=400,
            )
    except ValueError:
        return None, Response(
            {"error": f"Invalid input '{n_str}'. Parameter 'n' must be an integer."},
            status=400,
        )
    return n_int, None


@api_view(http_method_names=["GET"])
def fibonacci_view(request: Request) -> Response:
    n_int, error_response = _get_validated_fibonacci_n(request)

    if error_response:
        return error_response

    try:
        result = fibonacci_dynamic(n_int)
        return Response({"result": result}, status=200)
    except ValueError as e:
        return Response({"error": str(e)}, status=400)

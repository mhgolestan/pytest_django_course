from django.core.mail import send_mail
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination

@api_view(http_method_names=['POST'])
def send_company_email(request: Request) -> Response:
    send_mail(
        subject=request.data["subject"],
        message=request.data["message"],
        from_email="golestan1369@gmail.com",
        recipient_list=["golestan1369@gmail.com"]
    )
    return Response({"status": "success", "info": "email sent successfully"}, status=200)
import json

from django.shortcuts import render
from datetime import datetime
# Create your views here.
from .models import PaymentTransaction, FileUpload
from .serializers import InitiatePaymentSerializer, FileUploadSerializer
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
import requests

#Basic class to check if user is authenticated
class HelloView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}! You are authenticated."})


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        user = request.user
        now_str = datetime.now().strftime('%Y%m%d%H%M%S')
        print(now_str)
        # serializer=InitiatePaymentSerializer(
        #     data=request.data
        # )
        url = "https://sandbox.aamarpay.com/jsonpost.php"

        payload = json.dumps({
            "store_id": "aamarpaytest",
            "tran_id": now_str,
            "success_url": "http://www.merchantdomain.com/suc esspage.html",
            "fail_url": "http://www.merchantdomain.com/faile dpage.html",
            "cancel_url": "http://www.merchantdomain.com/can cellpage.html",
            "amount": "10.0",
            "currency": "BDT",
            "signature_key": "dbb74894e82415a2f7ff0ec3a97e4183",
            "desc": "Merchant Registration Payment",
            "cus_name": "Name",
            "cus_email": "payer@merchantcusomter.com",
            "cus_add1": "House B-158 Road 22",
            "cus_add2": "Mohakhali DOHS",
            "cus_city": "Dhaka",
            "cus_state": "Dhaka",
            "cus_postcode": "1206",
            "cus_country": "Bangladesh",
            "cus_phone": "+8801704",
            "type": "json"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            print(f'Response is: {response.text}')
            response_json = json.loads(response.text)
            redirect_url = response_json.get("payment_url")
            if not redirect_url:
                return Response({"error": "Failed to get redirect URL from AmarPay"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"redirect_url": redirect_url})
        except requests.RequestException as e:
            return Response({"error": "Payment initiation failed", "details": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # if serializer.is_valid():
        #     return Response({
        #         "redirect_url": "https://sandbox.aamarpay.com/payment-page-dummy"
        #     })
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PaymentSuccessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):

        user = request.user

        transaction_id = "TXN12345"
        amount = 100.00
        status = "success"
        gateway_response = {
            "message": "Payment confirmed by Aamarpay sandbox"
        }

        PaymentTransaction.objects.create(
            user=user,
            transaction_id=transaction_id,
            amount=amount,
            status=status,
            gateway_response=gateway_response,
            timestamp=timezone.now(),
        )

        return Response({
            "message":"Payment successful. Lets upload your file"
        })

class FileUploadView(APIView):
    permission_classes = [
        IsAuthenticated
    ]
    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def post(self, request):
        user = request.user

        if not PaymentTransaction.objects.filter(user=user, status='success').exists():
            return Response({"detail": "Payment required before uploading files."}, status=status.HTTP_403_FORBIDDEN)

        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            filename = uploaded_file.name

            if not (filename.endswith('.txt') or filename.endswith('.docx')):
                return Response({
                    "error":"Only .txt and .docx file are allowed to be uploaded"
                })

            file_upload = FileUpload.objects.create(
                user=user,
                file=uploaded_file,
                filename=filename,
                status='processing'
            )

            # Trigger Celery
            from .tasks import process_file_word_count
            process_file_word_count.delay(file_upload.id)

            return Response({
                "message":"File uploaded successfully, processing started"
            },status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






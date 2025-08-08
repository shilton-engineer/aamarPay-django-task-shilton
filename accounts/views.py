from django.shortcuts import render

# Create your views here.
from .models import PaymentTransaction, FileUpload
from .serializers import InitiatePaymentSerializer, FileUploadSerializer
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

#Basic class to check if user is authenticated
class HelloView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}! You are authenticated."})


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer=InitiatePaymentSerializer(
            data=request.data
        )

        if serializer.is_valid():
            return Response({
                "redirect_url": "https://sandbox.aamarpay.com/payment-page-dummy"
            })
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


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
            # from .tasks import process_file_word_count
            # process_file_word_count.delay(file_upload.id)

            return Response({
                "message":"File uploaded successfully, processing started"
            },status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






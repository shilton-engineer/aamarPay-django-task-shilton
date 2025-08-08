from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import InitiatePaymentSerializer

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
        return Response({
            "message":"Payment successful. Lets upload your file"
        })




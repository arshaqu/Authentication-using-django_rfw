from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from .Seriliazers import UserSerializer
from rest_framework.response import Response
from .Seriliazers import LoginSerializer
from .utils import get_tokens_for_user
from rest_framework.permissions import AllowAny
import random ,string 
from rest_framework import status
from django.core.cache import cache 
from .emails import *
from .Seriliazers import OtpVerificationSerializer


# view for registering users
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            name,email,password = (serializer.validated_data[key] for key in ['name','email','password'])
            user = UserData.objects.create_user(name=name,email=email,password=password)
            otp = ''.join(random.choices(string.digits,k=4))
            print(otp)
            cache_key = f'otp_{email}'
            send_otp_via_email(email,otp)
            cache.set(cache_key,otp,timeout=30000)
            return Response({'status':200,'message':'OTP is send to your Mail'})
           
        except Exception as e:
            return Response({'status':400, 'message':str(e), 'data':None})
            
    
class OtpVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = OtpVerificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.validated_data['email']
            otp_entered = serializer.validated_data['otp']
            print(f'Looking for user with email:{email}')
            user=UserData.objects.filter(email=email).first()
            if user:
                print("User is found")
            else:
                print('user is not found')
            if not user:
                return Response({'status':400,'message':'User does not exist with this Email.'},status=status.HTTP_400_BAD_REQUEST)
            cache_key = f'otp_{email}'
            cached_otp = cache.get(cache_key)
            print(f'Cached OTP: {cached_otp}, Entered OTP: {otp_entered}')

            if cached_otp == otp_entered:
                user.is_verified = True
                user.save()
                cache.delete(cache_key)
                return Response({'message':'Registration Successfull..'},status=status.HTTP_200_OK)
            else:
                return Response({'message':'OTP Sending is Fail'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Invalid Data'},status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        data = request.data
        serializer = LoginSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = get_tokens_for_user(user)

        return Response(
            {
                'status' : 200,
                'msg' : 'login successful',
                'token' : token
       })
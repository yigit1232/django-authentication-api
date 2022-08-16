from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User,Recovery
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer,MyTokenObtainPairSerializer,ForgotPasswordSerializer,ResetPasswordSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def index(request):
    if request.method == 'GET':
        return Response(
        {
            'Signup': 'http://127.0.0.1:8000/api/auth/signup/',
            'Login':'http://127.0.0.1:8000/api/auth/login/',
            'Forgot Password': 'http://127.0.0.1:8000/api/auth/reset/password/',
            'Reset Password': 'http://127.0.0.1:8000/api/auth/reset/password/<token>/'
        },
        status=status.HTTP_200_OK
        )
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def signup(request):
    if request.method=='POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def forgot_password(request):
    if request.method=='POST':
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':'send email'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def reset_password(request,token):
    if not Recovery.objects.filter(token=token).first():
        return Response({'error':'Token is invalid'},status=status.HTTP_400_BAD_REQUEST)
    if request.method=='POST':
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            repassword = serializer.validated_data['repassword']
            if password != repassword:
                return Response({'error':'passwords do not match'})
            elif len(password) < 6:
                return Response({'error': 'password must be 6 digits'})
            recovery = Recovery.objects.get(token=token)
            try:
                user = User.objects.get(id=recovery.user_id)
                user.set_password(password)
                user.save()
                recovery.delete()
            except User.DoesNotExist:
                return Response({'error':'User not found.'})
            return Response({'success':'Change password.'},status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
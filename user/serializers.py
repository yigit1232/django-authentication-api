from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.core.mail import send_mail
from .models import User,Recovery
import secrets

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        token['username'] = user.username
        token['email'] = user.email
        return token

class RegisterSerializer(serializers.ModelSerializer):
    repassword = serializers.CharField(write_only=True)
    username = serializers.CharField(error_messages=None)

    class Meta:
        model = User
        fields = ['name','username','email','password','repassword']

    def validate(self, data):
        if data['name'] == '' or data['username'] == '' or data['email'] =='' or data['password'] == '':
            raise serializers.ValidationError({'error':'All fields are required'})
        elif User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'error':'Username already taken'})
        elif User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error':'E-mail already taken'})
        elif data['password'] != data['repassword']:
            raise serializers.ValidationError({'error':'passwords do not match'})
        elif len(data['password']) < 6:
            raise serializers.ValidationError({'error':'password must be 6 digits'})
        return data

    def create(self, validated_data):
        name = validated_data.pop('name')
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User(name=name,username=username,email=email)
        user.set_password(password)
        user.save()
        return user

class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

    def validate(self, data):
        email = data['email']
        user = User.objects.filter(email=email).first()
        recovery = Recovery.objects.filter(user=user).first()
        if not user:
            raise serializers.ValidationError({'error':'User not found'})
        if recovery:
            recovery.delete()
        return data

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.filter(email=email).first()
        token = secrets.token_urlsafe(16)
        recovery = Recovery(user=user,token=token)
        recovery.save()
        send = send_mail(
            'Reset Password',
            f'Click the link below to change the password \n http://127.0.0.1:8000/api/auth/reset/password/{token}/',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email,]
        )
        return recovery

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    repassword = serializers.CharField()